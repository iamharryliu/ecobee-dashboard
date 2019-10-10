# Ecobee Dashboard
Dashboard to view and interact with your Ecobee thermostats.

## Screenshots
![Screenshot](images/demo.png)

### 

### Installing
Steps to get a development environment running:

Clone project and make logs folder for API logging.
```
git clone https://github.com/iamharryliu/ecobee-dashboard.git
mkdir ~/logs
```

Start back-end server.
```
# Change directory to preferred back-end (Flask/Django).
cd ~/ecobee-dashboard/back-end-flask #or back-end-django

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# If using Flask back-end.
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

# If using Django back-end.
python manage.py migrate --run-syncdb

python manage.py runserver
```

Start front-end server.
```
cd ~/ecobee-dashboard/front-end-angular #or front-end-react

# If using Angular front-end.
npm install --save-dev @angular-devkit/build-angular

npm start
```