import click
import questionary
from rich.console import Console
from rich.table import Table
from .api import MockAPIClient
from .auth import AuthHandler
from .models import Task

console = Console()
auth_handler = AuthHandler()
client = MockAPIClient()

# Common styles
SUCCESS_STYLE = "bold green"
ERROR_STYLE = "bold red"
WARNING_STYLE = "bold yellow"
INFO_STYLE = "bold cyan"

# Helper functions
def print_success(message):
    console.print(f"✅ {message}", style=SUCCESS_STYLE)

def print_error(message):
    console.print(f"❌ {message}", style=ERROR_STYLE)

def select_task_interactive():
    tasks = client.get_tasks()
    if not tasks:
        print_error("No tasks available")
        return None
        
    choice = questionary.select(
        "Select a task to modify:",
        choices=[
            questionary.Choice(
                f"{t['id']}: {t['title'][:30]}...",
                value=t['id']
            ) for t in tasks
        ]
    ).ask()
    return choice

# Auth commands
@click.group()
def cli():
    """Todo List CLI with Authentication"""
    pass

@cli.command()
def signup():
    """Create a new account"""
    email = questionary.text("Email:").ask()
    password = questionary.password("Password:").ask()
    confirm_password = questionary.password("Confirm Password:").ask()
    
    if password != confirm_password:
        print_error("Passwords do not match")
        return
        
    response = client.signup({
        "email": email,
        "password": password
    })
    
    if "token" in response:
        auth_handler.save_auth_token(response["token"], response["user_id"])
        print_success("Account created successfully!")
    else:
        print_error("Account creation failed")

@cli.command()
def login():
    """Log in to your account"""
    email = questionary.text("Email:").ask()
    password = questionary.password("Password:").ask()
    
    response = client.login({
        "email": email,
        "password": password
    })
    
    if "token" in response:
        auth_handler.save_auth_token(response["token"], response["user_id"])
        print_success("Logged in successfully!")
    else:
        print_error("Login failed")

@cli.command()
def logout():
    """Log out from current session"""
    auth_handler.clear_auth()
    print_success("Logged out successfully")

# Task commands
@cli.command()
def remove():
    """Delete a task interactively"""
    task_id = select_task_interactive()
    if not task_id:
        return
        
    if questionary.confirm("Are you sure you want to delete this task?").ask():
        success = client.delete_task(task_id)
        if success:
            print_success("Task deleted successfully")
        else:
            print_error("Failed to delete task")

@cli.command()
def update():
    """Update a task interactively"""
    task_id = select_task_interactive()
    if not task_id:
        return
        
    current_task = next((t for t in client.get_tasks() if t["id"] == task_id), None)
    
    new_title = questionary.text(
        "New title (press Enter to keep current):",
        default=current_task["title"]
    ).ask()
    
    new_description = questionary.text(
        "New description (press Enter to keep current):",
        default=current_task.get("description", "")
    ).ask()
    
    new_status = questionary.select(
        "Update status:",
        choices=["pending", "completed"],
        default=current_task.get("status", "pending")
    ).ask()
    
    update_data = {
        "title": new_title or current_task["title"],
        "description": new_description or current_task.get("description", ""),
        "status": new_status
    }
    
    response = client.update_task(task_id, update_data)
    if "message" in response:
        print_success(response["message"])
    else:
        print_error(response.get("error", "Unknown error"))

@cli.command()
def list():
    """Show all tasks in a table"""
    tasks = client.get_tasks()
    table = Table(title="Your Tasks", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="green")
    table.add_column("Description")
    table.add_column("Status", justify="right")
    
    for task in tasks:
        status_style = "green" if task.get("status") == "completed" else "yellow"
        table.add_row(
            task["id"],
            task["title"],
            task.get("description", ""),
            f"[{status_style}]{task.get('status', 'pending')}[/]"
        )
    
    console.print(table)

@cli.command()
def create():
    """Create a new task interactively"""
    # Check if user is authenticated
    auth_token = auth_handler.get_auth_token()
    if not auth_token:
        print_error("You need to be logged in to create tasks")
        if questionary.confirm("Do you want to log in now?").ask():
            login()
            auth_token = auth_handler.get_auth_token()
            if not auth_token:
                return
        else:
            return

    # Get task details interactively
    title = questionary.text(
        "Enter task title:",
        validate=lambda text: len(text) > 0 or "Title cannot be empty"
    ).ask()

    description = questionary.text(
        "Enter task description (optional):"
    ).ask()

    due_date = questionary.text(
        "Enter due date (optional, format YYYY-MM-DD):",
        validate=lambda text: True if not text or is_valid_date(text) else "Invalid date format"
    ).ask()

    priority = questionary.select(
        "Select task priority:",
        choices=["low", "medium", "high"],
        default="medium"
    ).ask()

    # Prepare task data
    task_data = {
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date if due_date else None,
        "status": "pending"
    }

    # Send to API
    try:
        response = client.create_task(task_data)
        if "id" in response:
            print_success(f"Task created successfully! ID: {response['id']}")
            if questionary.confirm("Do you want to view all tasks now?").ask():
                list()
        else:
            print_error("Failed to create task")
    except Exception as e:
        print_error(f"Error creating task: {str(e)}")

def is_valid_date(date_string):
    """Helper function to validate date format"""
    from datetime import datetime
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    cli()