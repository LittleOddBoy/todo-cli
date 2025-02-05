import click
from .api import APIClient
from .models import Task

# Initialize the CLI group first
@click.group()
def cli():
    """Simple CLI for managing tasks"""
    pass

# Color constants
SUCCESS_COLOR = "green"
ERROR_COLOR = "red"
WARNING_COLOR = "yellow"
INFO_COLOR = "cyan"

def display_message(message, message_type="info"):
    """Display colored messages with emojis"""
    colors = {
        "success": SUCCESS_COLOR,
        "error": ERROR_COLOR,
        "warning": WARNING_COLOR,
        "info": INFO_COLOR
    }
    emojis = {
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
        "info": "ℹ️"
    }
    
    click.echo(
        click.style(
            f"{emojis.get(message_type, '')} {message}",
            fg=colors.get(message_type, INFO_COLOR),
            bold=True
        )
    )

@cli.command()
@click.option("--title", help="Task title")
@click.option("--description", help="Task description")
def create(title, description):
    """Create a new task with interactive prompts"""
    try:
        # Debugging output
        click.echo("Starting task creation process...")
        
        # Interactive prompt if title not provided
        if not title:
            title = click.prompt(
                click.style("📝 Enter task title", fg=INFO_COLOR, bold=True),
                type=str
            )
        
        # Prompt for description if not provided
        if not description and click.confirm(
            click.style("➕ Add description?", fg=INFO_COLOR)
        ):
            description = click.prompt(
                click.style("📝 Enter task description", fg=INFO_COLOR),
                type=str
            )

        # Create and validate task
        task = Task(title=title, description=description)
        task.validate()
        
        # Debugging output
        click.echo("Creating task with data:", nl=False)
        click.echo(f" Title: {task.title}")
        click.echo(f" Description: {task.description}")
        
        # Send to API
        client = APIClient()
        click.echo("Sending request to API...")
        result = client.create_task({
            "title": task.title,
            "description": task.description
        })
        
        # Display results
        display_message(
            f"Task created successfully! ID: {result.get('id', '')}\n"
            f"Message: {result.get('message', 'No status message')}",
            "success"
        )
        
    except ValueError as e:
        display_message(f"Validation error: {str(e)}", "error")
    except Exception as e:
        display_message(f"API Error: {str(e)}", "error")

# Main entry point
if __name__ == "__main__":
    cli()