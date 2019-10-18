# Ecobee Dashboard
Dashboard to view and interact with your Ecobee thermostats.

## Screenshots
![Screenshot](images/demo.png)

## Installing
Steps to get a development environment running on Mac/Linux:

Clone project and set up log folder.
```
cd ~
git clone https://github.com/iamharryliu/ecobee-dashboard.git
mkdir ~/logs
```

###Run back end server
Choose either Flask or Django to run as the back-end server and either Angular or React to run as the front-end server. If you are using Flask as the back-end, make sure to use commands for the correct Python environment for your machine.

Setup and run Django back-end server.
```
cd ~/ecobee-dashboard/back-end-django
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --run-syncdb
python manage.py runserver
```

Setup and run Flask back-end server on Linux.
```
cd ~/ecobee-dashboard/back-end-flask
python3 -m venv venv
source venv/bin/activate
pip install -r linux-requirements.txt
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
python manage.py runserver
```

Setup and run Flask back-end server on Mac.
```
cd ~/ecobee-dashboard/back-end-flask
python3 -m venv venv
source venv/bin/activate
pip install -r mac-requirements.txt
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
python manage.py runserver
```

Setup and run Angular front-end server.
```
cd ~/ecobee-dashboard/front-end-angular
npm i
npm start
```

Setup and run React front-end server.
```
cd ~/ecobee-dashboard/front-end-react
npm i
npm start
```