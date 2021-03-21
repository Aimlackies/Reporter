# reporter

## Setup

### Docker
1. sudo docker build -t reporter_app:latest .
2. sudo docker run --name reporter_app -d -p 8000:5000 --rm reporter_app:latest


### No Docker
1. `conda create -n aimlacReporter python=3.8`
2. set up mySQL, create database table, mySQL user, update config with details (remane configExample to config)
3. `pip install -r requirements.txt`
4. `export FLASK_APP=reporter.py`
5. `export FLASK_ENV=development`
6. `flask db init`
7. `flask db migrate`
8. `flask db upgrade`
9. `flask seed`

### Before working on something new

1. `git pull`
2. unix: `export FLASK_APP=reporter.py`, Windows: `set FLASK_APP=reporter.py`
3. unix: `export FLASK_ENV=development`, Windows: `set FLASK_ENV=development`
4. `flask db upgrade`
5. `flask run`

### Deploying

* compile scss into css https://sass.github.io/libsass-python/frameworks/flask.html#building-sass-scss-for-each-request
