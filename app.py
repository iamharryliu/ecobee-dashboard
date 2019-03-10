from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1/mydb'
db = SQLAlchemy(app)

class Ecobee(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	api_key = db.Column(db.String(32), nullable=False)
	authorization_code = db.Column(db.String(32), nullable=False)
	access_token = db.Column(db.String(32), nullable=False)
	refresh_token = db.Column(db.String(32), nullable=False)

@app.route('/')
def main():
	return render_template('thermostat.html')

@app.route('/apps/')
def apps():
	apps = Ecobee.query.all()
	return render_template('apps.html', apps=apps)

@app.route('/thermostats/')
def thermostats():
	return render_template('thermostats.html')

@app.route('/thermostat/')
def thermostat():
	return render_template('thermostat.html')

if __name__ == '__main__':
	app.run(debug=True)