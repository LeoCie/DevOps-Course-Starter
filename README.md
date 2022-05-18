# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Trello

This app uses [Trello](https://trello.com/) to store data. You will need to create a free account and a board of your own to use the app locally.
After creating an account you can get a key and token from [here](https://trello.com/app-key), and get the ID of your board, and add these into the `.env` file.

## Running the App

### In docker

Make sure you have [Docker](https://docs.docker.com/get-docker/) installed and running

You will first need to build the docker image, this can be done by running the following in this directory:
```bash
docker build --target development --tag todo-app:dev .
```

Now start the container using the following command:
```bash
docker run --env-file .env -p 5100:80 --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app/todo_app -d todo-app:dev
```

The site will be available at `localhost:5100`.

This uses a bind mount of the todo_app folder on your machine, so you won't need to restart the container to see any changes you make locally.

### On the command line

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Testing

The app uses pytest for unit, integration and end-to-end selenium testing.
To run the unit and integration tests from the command line run
```bash
poetry run pytest todo_app_tests
```

To run the end-to-end selenium tests you will need to:
1. download [Gecko Driver](https://github.com/mozilla/geckodriver/releases) and place the exe in the project root
1. make sure Firefox is installed
1. from the command line run
```bash
poetry run pytest todo_app_tests_e2e
```

Or you can run them from VSCode:

Click the conical flask icon on the left edge of VSCode. Click the refresh icon at the top of the panel to rediscover tests. Click the play icon at the top to run all tests. Click the play icon next to a file or test name to run that file or test individually.

## Running as a service with ansible

Make sure your managed VMs are listed in the hosts.ini file under the "webservers" group.
Copy the hosts.ini and to_do_playbook.yml files onto your control node.
On the control node run `ansible-playbook to_do_playbook.yml -i hosts.ini`