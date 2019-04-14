from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
	
	app = Flask(__name__)

	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1/ecobee_db'

	db.init_app(app)

	with app.app_context():
		db.create_all()

	from ecobee.main.routes import main

	app.register_blueprint(main)

	return app