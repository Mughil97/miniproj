# Overview

This is a prototype RESTFul API  using Python and Flask web framework with PostgreSQL as backend. This example structuring API following best practices including logging, authentication, classes, unit testing and dockerizing the application. 

<b>Softwares</b>

* Python
* PostgreSQL
* Docker

<b>Libraries</b>
* Flask
* Flask RestFul
* SQLAlchemy - SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
* Flask BCrypt
* Flask JWT Extended
* Psycopg2 - a Python adapter for Postgres
* Flask-SQLAlchemy - Flask extension that provides SQLAlchemy support
* Flask-Migrate - Extension that supports SQLAlchemy database migrations via Alembic

# Python
Python is an interpreted, high-level, general-purpose programming language.

# Flask
Flask is a lightweight web application framework designed to make getting started quick and easy, with the ability to scale up to complex applications. 

# Development Environment Setup
## Prerequisites
* `Python` -  Install a python Operating system specific interpreter to be able to execute your code. If you don't have Python then Download and install [Python] operating system specific.

Make sure you already have Python or you have installed correctly.
```
> python --version
```
> The above command shows the Python version.

Upgrade the Pip to latest version with the following command
On Linux or MacOS
```
$ python install -U pip
```
On Windows
```
> python -m pip install -U pip
```

* `pip` - pip is a very popular python package installer. pip is installed with Python version greater than 3.4. Make sure the pip is installed or not. If not go to the [pip] page to install.
```
> pip --version
```
> The above command shows the Pip version.

* `Visual Studio code` - A python code editor which has support of formatting the code, terminal to execute and debug etc., if you don't have editor Download and install [Visual Studio Code] operating system specific


### Virtual Environment
Python applications will often use packages and modules that don't come as part of the standard library. Applications will sometimes need a specific version of a library. It means that there might be multiple applications with different versions of python and/or modules required to run the application. Having one global version being used by all application will not suffice the needs.

To solve this issue by create a virtual environment, a self-contained directory tree that contains a Python installation for a particular version of Python, plus a number of additional packages.

Installing the virtual environment
```
> pip install virtualenv
```
Make sure the virtualenv is installed correctly
```
> virtualenv --version
```
> The above command shows the Virtualenv version.  

## Setup a Project
Clone the existing project from git repository to a folder or create folder to setup a new python project.

* <b>Project Workspace</b>

Create a project workspace folder from command line / shell prompt
On Linux or MacOS
```
$ mkdir <project_name>
```
On Windows
```
> md <project_name>
```
* <b>Virtual Environment</b>

Navigate to the project folder to setup the virtual environment. Create a virtual environment for this project run the following command
```
> python -m venv env
```

* <b>Visual Studio Code Editor</b> 

To open the project in Visual Studio code editor run the following command from the project folder.

```
> code .
```

1. From the visual studio code editor install the python extension.
2. To configure the virtual environment in visual studio code editor. 
* Go to the editor navigation menu `View -> Command Palatte`. 
* Type the <b>Python: Select Interpreter</b> command from the <b>Command Palette</b>. 
* The <b>Python: Select Interpreter</b> command displays a list of available global environments, virtual environments. Choose the virtual environment prefix with `env` located in project workspace folder.
3. Create a new terminal from `Terminal -> New Terminal` the VS code automatically select the activated environment in the project workspace folder.

### Managing Dependency Libraries
Install the required libraries using `pip install <library>` from the VS Code terminal.

```
> pip install flask flask-restful flask-sqlalchemy flask-migrate alembic psycopg2 flask-script flask-bcrypt flask-jwt-extended
```

For existing projects installing the each required libraries used in project has to be identified from the runtime error. So managing all the dependencies in a file will help build the application or other team members who are all working on a project can be installed the required dependency libraries easily. Dependencies can be managed in `Pipfile` or in a plain text file called `requirements.txt`. Install the dependencies from `requirements.txt` on the terminal.

```
> pip install -r requirements.txt
```

Export the dependency libraries to `requirements.txt` from the terminal
```
> pip freeze > requirements.txt
```

## PostgreSQL DB in Container
Please find how to setup the [PostgreSQL DB in Docker] here.

### Database Setup
Create a database using PostgreSQL interactive terminal or PgAdmin UI interface.

* Launch the PostgreSQL terminal
```
> docker exec -it postgresdb bash
```

* Start the PostgreSQL shell by typing psql in the interactive terminal
```
$ psql -U postgres --password
```
> The PostgreSQL shell launches psql and the prompt the password to access the databases.

* Create a database in PostgreSQL
```
$create database pyflaskpoc;
```

## Configurations
* Configuration parameters like database, keys etc., can be managed in a file, object, envrionment variables, json and mapping. 

Below is the config object ...
```
import os

class Config:
    JWT_SECRET_KEY = 'thismysecretkey'
    SQLALCHEMY_DATABASE_URI = 'postgresql://<username>:<password>@localhost:5432/pyflaskpoc'
```

> Note: Running the application and postgres db in containers then the postgres host ip should be containers private IP address. 
> To get the docker container ip address use the following command
>```
> docker network inspect bridge
>```

* Logging configuration can be managed in configuration file, json, object etc., 

* Port and Host are configured in `run.py`

> Note: This project uses configuration from object `config.py` for database and `logging.cfg` for logging.

### Database Table using Migrations
Flask-Migrate is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic. The database operations are made available through the Flask command-line interface or through the Flask-Script extension.

`manage.py` file has configured to run the migrations. Import all them models that has to be created in the database.
```
from models.user import User 
```

* Create a migration repository with the following command, will add a migrations folder to your application. The contents of this folder need to be added to version control along with your other source files

```
> python manage.py db init
```

* Generate an initial migration
```
> python manage.py db migrate
```
>Note: The migration script needs to be reviewed and edited, as Alembic currently does not detect every change you make to your models. In particular, Alembic is currently unable to detect table name changes, column name changes, or anonymously named constraints.

* Apply the migration to the database
```
> python manage.py db upgrade
```
> Each time the database models change repeat the `migrate` and `upgrade` commands.

### Run / Debug the Application
Run / Debug the application from VS Code can be either from `launch.json` or `Terminal`. 

* Run the application from the terminal
```
> python run.py
```
* Debug the application running on local from terminal
```
> python -m debugpy --listen 5678 run.py
```
For Debugging the local code, You would then use the following configuration to attach from the VS Code Python extension.  
```
{
  "name": "Python: Attach",
  "type": "python",
  "request": "attach",
  "connect": {
    "host": "localhost",
    "port": 5678
  }
}
```
* Debug the application running on remote machine or container
```
> python -m debugpy --listen 0.0.0.0:5678 run.py
```
For Debugging the remote code or code running on containers, You would then use the following configuration to attach from the VS Code Python extension. 
```
{
  "name": "Attach",
  "type": "python",
  "request": "attach",
  "host": "remote-machine-name", // replace this with remote machine name
  "port": 5678
}
```
### Testing the Application
The unit test uses a separate config object (`config_test.py`) and app(`app_test.py`) file. The initialization of the application and configuration handled through the `tests/BaseCase.py`.

Run the <b>Unit Test </b> from the VS Code or OS Terminal
```
> python -m unittest tests/test_login.py
```

### Dockerize the Application
Docker - If you don't have Docker installed then download and follow the installation manual from [Docker] hub. 

Below is the Docker File to create container image with all the required libraries to run the application.
```
FROM python:3.7-alpine 
COPY . /app
WORKDIR /app
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi libffi-dev libressl-dev \
    && pip3 install -r requirements.txt 
EXPOSE 5000 
ENTRYPOINT [ "python" ] 
CMD [ "run.py" ] 
```
> Note: The dependencies gcc musl-dev libffi libffi-dev libressl-dev are used in JWT authentication. The alpine linux is very minimal version it doesn't have the libraries installed, so installing the libraries before installing the application dependencies.

* Build the docker image from the windows command line

```
> docker build --tag python-flask-postgres-docker .
```

* List all the images in your Docker repository.
```
> docker images
```
* Run the application using docker
```
> docker run --name python-flask-postgres-docker -p 5000:5000 -d python-flask-postgres-docker

```

`-d` – Starts the container as a background process.

`--name` – Name of the container.

* To check the status 

```
> docker ps
```
* To view the application Docker logs by `name`
```
> docker logs python-flask-postgres-docker
```

* Stop the running container by name or Id
```
> docker stop python-flask-postgres-docker
```
* List the running Docker containers 
```
> docker ps
```
* Start the container by name or Id
```
> docker start python-flask-postgres-docker
```

[Python]: <https://www.python.org/downloads/>
[Visual Studio Code]: <https://code.visualstudio.com/download> 
[pip]: <https://pip.pypa.io/en/stable/installing/>
[Docker]: <https://hub.docker.com/editions/community/docker-ce-desktop-windows>
[PostgreSQL DB in Docker]: <http://git.myacies.com/poc/docker/postgresdb/-/blob/master/README.md>
