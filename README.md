# Ecobee Dashboard
Dashboard to view and interact with your Ecobee thermostats.

## Built With
* Angular - front-end framework
* Bootstrap - front-end templating
* Flask - back-end framework
* SQL - database
* [Ecobee App](https://github.com/itzliu/ecobeeApp)

## Screenshots
![Screenshot](back-end/flaskApp/static/images/README/home-view.png)
![Screenshot](back-end/flaskApp/static/images/README/thermostat-view.png)

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Requirements
* Python3.6+
* pip3
* Angular 8
* SQL (configure your SQL settings in ecobee-dashboard/back-end/ecobee/config.py file)

### Installation
Steps to get a development environment running:

Setup your SQL configuration for storing API credentials inside the ecobee-dashboard/back-end/ecobee/config.py file.

Open a Terminal for the back-end:

```
cd ~
git clone https://github.com/itzliu/ecobee-dashboard.git
mkdir ~/logs
cd ecobee-dashboard/back-end
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Open another terminal for the front-end:

```
cd ecobee-dashboard/front-end
ng serve
```
