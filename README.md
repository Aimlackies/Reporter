# reporter

## Setup

### Docker
1. sudo docker build -t reporter_app:latest .
2. sudo docker run --name reporter_app -d -p 8000:5000 --rm reporter_app:latest


### No Docker
1. `conda create -n aimlacReporter python=3.8`
2. set up mySQL, create database table, mySQL user, update config with details (remane configExample to config)
2. `flask db init`
3. `flask db migrate`
3. `flask db upgrade`
