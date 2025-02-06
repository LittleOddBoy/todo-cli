# todo-cli

➕ An additional tool as the UI-like client for project [todo-api](https://github.com/LittleOddBoy/todo-api)
I developed this CLI to test the API for the mentioned project with [DeepSeek-R1](https://deepseek.com), all coded in Python.

## Requirements

You might need the following in order to run the project:

- Python 3.x

To load the requirements for the project itself, run:

```bash
pip install -r requirements.txt
```

You must have the [todo-api](https://github.com/LittleOddBoy/todo-api) sat up.

## Installation

After meeting the requirements, it's time to set-up the project, which you might do it by cloning the project locally:

```bash
git clone https://github.com/LittleOddBoy/todo-cli.git .
```

**the command will clone the project in your cwd**

If you don't have an account, you must run the `signup` command, in order to create an account and sync your data.

```bash
python -m todo_cli.cli signup
```

## Usage

There is a variety of things you can do with this CLI—all about to-do list things.

- `create`: to create a new task.
- `list`: prints a list of your tasks.
- `update`: select a task and update it.
- `remove`: remove a task among a list of items.
- `logout`: log-in to your account.
- `signup`: sign-in to your account.

To run them, go ahead and:

```bash
python -m todo_cli.cli <command>
```

## Contribute

I welcome pull requests:)

## Credits and Licenses

This program is under [MIT License](LICENSE).
