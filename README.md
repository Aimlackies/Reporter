# reporter

## Setup

### Docker
1. sudo docker build -t reporter_app:latest .
2. sudo docker run --name reporter_app -d -p 8000:5000 --rm reporter_app:latest


### No Docker
1. `conda create -n aimlacReporter python=3.8`
2. set up mySQL, create database table, mySQL user, update config with details (remane configExample to config)
3. `pip install -r requirements.txt`
4. `export FLASK_APP=reporter_app`
5. `export FLASK_ENV=development`
2. `flask db init`
3. `flask db migrate`
3. `flask db upgrade`

### Before working on something new

1. `pip pull`
2. unix: `export FLASK_APP=reporter_app`, Windows: `set FLASK_APP=reporter_app`
3. unix: `export FLASK_ENV=development`, Windows: `set FLASK_ENV=development`
4. `flask db upgrade`
5. `flask run`

### Deploying

* compile scss into css https://sass.github.io/libsass-python/frameworks/flask.html#building-sass-scss-for-each-request
