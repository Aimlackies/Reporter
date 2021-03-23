Reporter
========

This is the web application to report on energy usage.

## Sections

* [Getting started](#getting-started)  
  * [Installation](#installation)  
  * [Application structure](#application-structure)  
  * [Routes](#routes)  
  * [Before starting a new development](#before-starting-a-new-development)  
  * [Creating a blueprint](#creating-a-blueprint)  
* [Deploying](#deploying)  

Getting started
------------

### Installation

The following instructions will set up a local instance of the reporter application for development.

1. Create a Conda environment and install Python packages. The Conda enviroemtn is set to use Python 3.8 as, at the time of creation, that was the latest version PyTorch supported. Ensure compatibility with dependencies before upgrading.

    ```sh
    conda create -n aimlacReporter python=3.8
    pip install -r requirements.txt
    ```

2. Set up local MySQL server

    Follow this guide for your operating system. You may also wish to download the workbench for easier access to the database from outside the flask application  
    https://dev.mysql.com/doc/mysql-getting-started/en/#mysql-getting-started-installing  
    i. Create a user and keep a record of its username and password  
    ii. Create a new database and give your user from step (i) permission to access and write to it.  
    **Note:** If this system is live then ensure the password for both root and the database user is strong.

3. Set system environment varables for the Flask application. The first tells the Flask command the file to run on startup and the second will cause the Flask application to start in development mode.

    **Windows**:
    ```sh
    SET FLASK_APP=reporter.py
    SET FLASK_ENV=development
    ```
    **Unix based systems**:
    ```sh
    export FLASK_APP=reporter.py
    export FLASK_ENV=development
    ```

4. Initiate, create and seed your local database with a default admin user. The commands to `migrate` and `upgrade` the database will also be used to make updates to the database schema. The default admin user will have the email `admin@aimlackies.com` and the password `password`. **The password should be changed straight away on a live Installation**.

    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    flask seed
    ```

5. Create `config.py`  
    Currently there is no `config.py` file. Copy `configExample.py` to a new file in the same directory called `config.py`. In this file you will need to add the username, password and database you created earlier for MySQL. The following line in `config.py` will be changed to include the MySQL username in place of `reporter_db_user`, the password in place of `reporter_db_Acce55` and database name in place of `local_reporter`.

    ```py
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://reporter_db_user:reporter_db_Acce55@127.0.0.1/local_reporter'
    ```

6. Start the application.

    You're done! All that is left now is to start the application and start developing!

    ```sh
    flask run
    ```

### Application structure

Here is the basic structure of the application. Some files and folders have been missed as they are automatically generated and / or can be ignored.

```
Repository root
|
|-migrations
|     |
|     |-versions
|           |
|           |-database migration files (.py)
|
|-reporter_app
|     |
|     |-blueprint folder
|     |     |
|     |     |-__init__.py
|     |     |-routes.py
|     |     |-forms.py
|     |     |-utils.py
|     |
...   ...
|     |
|     |-templates
|     |     |
|     |     |-security
|     |     |    |
|     |     |    |-template files (.html)
|     |     |
|     |     |-blueprint folders
|     |     |    |
|     |     |    |-template files (.html)
|     |     |
...   ...   ...
|     |     |
|     |     |-template_parts
|     |     |    |
|     |     |    |-template files (.html)
|     |
|     |-__init__.py
|     |-cli.py
|     |-forms.py
|     |-models.py
|     |-utils.py
|
|-config_testing.py
|
|-config.py
|
|-reporter.py
|
|-requirements.txt
|
|-setup.py
```

* All database changes are added to automatically generated files in the directory `migrations/version/`. These will contain a `up` and a `down` function which tell MySQL how to update the database for new changes and revert to older versions.
* `blueprint folder` is used in place of all blueprints the application use. These are individual sections of the application which are all responsible for a set feature (e.g. errors, dashboard or users).
* The application is defined in `__init__.py` withing `reporter_app/`.
* Any additional command line commands that should be called with `flask xxx` are defined in `cli.py`.
* Even though blueprints define individual sections of the application, any tables / columns are defined in a single `model.py` file defined in `reporter_app/`.
* Front end views are contained within templates. Security (Flask security too) has a dedicated folder and all other templates are within folders for cosponsoring blueprints or template_parts if they are shared between templates (e.g. as imports)

### Routes

```
Endpoint             Methods    Rule
-------------------  ---------  -----------------------
dashboard.dashboard  GET        /dashboard
dashboard.dashboard  GET        /
security.login       GET, POST  /login
security.logout      GET, POST  /logout
security.register    GET, POST  /register
security.verify      GET, POST  /verify
static               GET        /static/<path:filename>
users.user           GET        /user/<id>
```

### Before starting a new development

Follow these basic instructions before starting work on any new feature.

1. Get the latest changes from the repository / branch

    ```sh
    git pull
    ```

    **Note:** You should also change to a new branch before moving any further, if not already done so.

2. Set system environment varables for the Flask application. The first tells the Flask command the file to run on startup and the second will cause the Flask application to start in development mode.

    **Windows**:
    ```sh
    SET FLASK_APP=reporter.py
    SET FLASK_ENV=development
    ```
    **Unix based systems**:
    ```sh
    export FLASK_APP=reporter.py
    export FLASK_ENV=development
    ```

3. Update the database

    make sure your local database is up-to-date with the latest changes

    ```sh
    flask db upgrade
    ```

    **Note:** To generate a new migration once modifying `models.py`, run the command `flask db migrate -m "migration message"`.

4. Start the application.

    You're done! All that is left now is to start the application and start developing!

    ```sh
    flask run
    ```

### Creating a blueprint

This is a basic guide on creating a new blueprint

1. Add blueprint import to `__init__.py`

    Add the collowing to the function called `create_app()` in `reporter_app/__init__.py`. Replace `blueprint_name` with a descriptive (but short) name for the blueprint.

    ```py
    from reporter_app.blueprint_name import bp as blueprint_name_bp
    app.register_blueprint(blueprint_name_bp)
    ```

2. Create 2 folders with the name of the blueprint. The first will go at `reporter_app/blueprint_name` and the second `reporter_app/templates/blueprint_name`.

3. Create the basic blueprint files in `reporter_app/blueprint_name`
    i. Create a file called `__init__.py` and past this code (changing `blueprint_name` to the name of the blueprint)

    ```py
    from flask import Blueprint

    bp = Blueprint('blueprint_name', __name__)

    from reporter_app.blueprint_name import routes
    from reporter_app.blueprint_name import forms

    ```
    ii. Create two additional files in `reporter_app/blueprint_name`. The first will be called `routes.py` and the second `forms.py`

4. You are done! Well... kind of. Now its up to you to add the rest, but that will depend on what you are adding so the steps for doing so are down to you. From steps 1 to 3 you will have a file structure with a few new folders and files which will kind of look like this:

```
Repository root
|
|-reporter_app
|     |
|     |-blueprint folder
|     |     |
|     |     |-__init__.py
|     |     |-routes.py
|     |     |-forms.py
|     |
|     |-templates
|     |     |
|     |     |-blueprint folders
|     |
|     |-__init__.py
```

## Deploying

It's a bit lonely here. Not to worry, as soon as we have made a deployment there will be plenty to add :D

* compile scss into css https://sass.github.io/libsass-python/frameworks/flask.html#building-sass-scss-for-each-request

### Docker
1. sudo docker build -t reporter_app:latest .
2. sudo docker run --name reporter_app -d -p 8000:5000 --rm reporter_app:latest
