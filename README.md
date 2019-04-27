# ecobee
Web app to interact with ecobee API.

## What I Learned
* How to create web APIs
* How to use and implement mySQL in an API project
* How to use UPDATE and DELETE requests.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites
* Python3
* mySQL

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
virtualenv -p python3 env
```
Activate your virtual environment.
```
source env/bin/activate
```
Install the Pyhon dependencies.
```
pip install -r requirements.txt
```
To get mysqlclient to work you will need to install the Python and MySQL development headers and libraries like so for Debian distributions ([link](https://pypi.org/project/mysqlclient/) for help with mysqlclient).
```
sudo apt-get install python-dev default-libmysqlclient-dev
```
Create mySQL database and tables.
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
* Flask - micro framework
* mySQL - database

## Screenshots
![Screenshot](home-page.png)
![Screenshot](thermostat-page.png)

## Authors
* **Harry Liu**

## Acknowledgements
* Built based on [this Python Ecobee API](https://github.com/nkgilley/python-ecobee-api) from GitHub by [nkgilley](https://github.com/nkgilley/python-ecobee-api/commits?author=nkgilley).
