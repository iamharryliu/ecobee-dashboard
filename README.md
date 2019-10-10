# Ecobee Dashboard
Dashboard to view and interact with your Ecobee thermostats.

## Built With
* Angular - front-end framework
* Bootstrap - front-end templating
* Flask - back-end framework
* SQL - database
* [Ecobee App](https://github.com/iamharryliu/ecobeeApp)

## Screenshots
![Screenshot](images/demo.png)

### Requirements
* Python3.6+ and pip3
* Angular

### Installation
Steps to get a development environment running:

Setup your SQL configuration for storing API credentials inside the ecobee-dashboard/back-end/ecobee/config.py file.

Open a Terminal for the back-end:

```
cd ~
git clone https://github.com/iamharryliu/ecobee-dashboard.git
mkdir ~/logs
cd ecobee-dashboard/back-end-flask
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Open another Terminal for the front-end:

```
cd ecobee-dashboard/front-end-angular
ng serve
```
