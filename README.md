[![codecov](https://codecov.io/gh/3V0L/flask-setup/branch/master/graph/badge.svg)](https://codecov.io/gh/3V0L/flask-setup) [![Build Status](https://travis-ci.org/3V0L/flask-setup.svg?branch=master)](https://travis-ci.org/3V0L/flask-setup) [![Maintainability](https://api.codeclimate.com/v1/badges/4779b3eab1272993f05d/maintainability)](https://codeclimate.com/github/3V0L/flask-setup/maintainability)

# Project Bids
A simple flask API that allows a user to create projects and get bids for funding the project. It also allows a user to bid on projects, all that is needed is an email and a user name.

The live link for the app => [https://sample-tapiwa.herokuapp.com/](https://sample-tapiwa.herokuapp.com/)

### Postman Collection
Download this JSON Collection file and import it to your Postman App. It contains endpoints and data that can be used to interact with the API
[Sample Postman Collection with data](https://github.com/3V0L/flask-setup/blob/master/SAMPLE%20API.postman_collection.json)

## How to run this app

  - Clone this repository
  ```
  https://github.com/3V0L/flask-setup.git
  ```

  - Navigate into directory
  ```
  $ cd flask-setup
  ```

  Create a virtual environment
  ```
  $ python3 -m venv venv
  ```

  - Rename the `.env-example` file to `.env` and set your environment variables as shown in the file
  - After doing the above, enter the command
  ```
  $ source .env
  ```

  - Install the apps dependencies by running 
  ```
  $ pip install -r requirements.txt
  ```

  - Run initial migrations
  ```
  $ python manage.py db init
  $ python manage.py db migrate
  $ python manage.py db upgrade
  ```

  - Run 
  ```
  $ python app.py
  ```

## API Endpoints

|Endpoint                  | Functionality              |HTTP method 
|--------------------------|----------------------------|-----------------
|/register                |register a new user                |POST        
|/project/create       |Create a project |POST
|/project/delete/      |Remove a Project               |DELETE
|/project/update                |Update a Project         |PATCH
|/project/my-projects       |Get all my projects                  |GET
|/project/get-project?id=*project_id* |Get a specific project               |GET
|/project/get-project       |Get all active projects     |GET
|/bid/create          |Creates a bid for a project             |POST
|/bid/update          |Updates a bid for a project             |PATCH
|/bid/delete  |Delete a bid for a project              |DELETE
|/bid/my-bids |Get all a user's bids              |GET


## Testing and Linting
Command for testing
```
$ pytest --cov=api
```
Linting command
```
$ pycodestyle api
```