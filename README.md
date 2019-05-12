# ecobee
Dashboard to interact with ecobee API.

## What I Learned
* How to interact with IOT devices through web API
* Impletment MySQL database to Flask project.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites
* Python3.6+
* pip3
* SQL

### Installing
A step by step series of examples that tell you how to get a development environment running.

Clone the repository onto your machine.
```
git clone https://github.com/itzliu/ecobee.git
```
Change directory into the project directory folder.
```
cd ecobee
```
Create a virtual environment for the app.
```
python3 -m venv venv
```
Activate your virtual environment.
```
source venv/bin/activate
```
Install the Pyhon dependencies for MySQL or Postgres.
```
pip install -r requirements-mysql.txt
pip install -r requirements-postgres.txt
```
To get mysqlclient to work properly, go to the following ([link](https://pypi.org/project/mysqlclient/).

Create mySQL database and tables. You will also want to make changes to 'SQLALCHEMY_DATABASE_URI' in your Flask configurations to be able to access your MySQL sever.
```
CREATE DATABASE ecobee_db;
USE ecobee_db;
CREATE TABLE ecobee_api_configs(
  name VARCHAR(20) NOT NULL,
  api_key VARCHAR(32) NOT NULL,
  authorization_code VARCHAR(32) NOT NULL,
  access_token VARCHAR(32) NOT NULL,
  refresh_token VARCHAR(32) NOT NULL,
  PRIMARY KEY (api_key),
  UNIQUE (name, api_key)
);
```
Run the application.
```
python run.py
```
## Running Tests
N/a

## Built With
* Flask - framework
* mySQL - database

## Screenshots
![Screenshot](ecobee/static/home-page.png)
![Screenshot](ecobee/static/thermostat-page.png)

## Authors
* **Harry Liu**

## Acknowledgements
* Built based on [this Python Ecobee API](https://github.com/nkgilley/python-ecobee-api) from GitHub by [nkgilley](https://github.com/nkgilley/python-ecobee-api/commits?author=nkgilley).
