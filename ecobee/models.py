from ecobee import db


class apis(db.Model):
    name = db.Column(db.String(20), unique=True, nullable=False)
    api_key = db.Column(db.String(32), primary_key=True, unique=True, nullable=False)
    authorization_code = db.Column(db.String(32), nullable=False)
    access_token = db.Column(db.String(32), nullable=False)
    refresh_token = db.Column(db.String(32), nullable=False)

#     thermostats = db.relationship('Thermostat', backref='api', cascade='all,delete', lazy=True)


# class Thermostat(db.Model):
#     app_api_key = db.Column(db.String(32), db.ForeignKey('apis.api_key'), nullable=False)
#     identifier = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
#     set_temperature = db.Column(db.Float)
#     actual_temperature = db.Column(db.Float)
#     sensors = db.relationship('Sensor', backref='thermostat', cascade='all,delete', lazy=True)


# class Sensor(db.Model):
#     thermostat_identifier = db.Column(db.Integer, db.ForeignKey('thermostat.identifier'), primary_key=True, nullable=False)
#     id = db.Column(db.String(6))
#     temperature = db.Column(db.Float)
#     humidity = db.Column(db.Integer)
#     occupancy = db.relationship('Sensor_Occupancy_Data', backref='thermostat', cascade='all,delete', lazy=True)
#     temperature = db.relationship('Sensor_Temperature_Data', backref='thermostat', cascade='all,delete', lazy=True)
#     humidity = db.relationship('Sensor_Humidity_Data', backref='thermostat', cascade='all,delete', lazy=True)


# class Sensor_Temperature_Data(db.Model):
#     sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.thermostat_identifier'), primary_key=True, nullable=False)
#     start_time = db.Column(db.DateTime, nullable=False)


# class Sensor_Humidity_Data(db.Model):
#     sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.thermostat_identifier'), primary_key=True, nullable=False)
#     start_time = db.Column(db.DateTime, nullable=False)


# class Sensor_Occupancy_Data(db.Model):
#     sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.thermostat_identifier'), primary_key=True, nullable=False)
#     start_time = db.Column(db.DateTime, nullable=False)
#     end_time = db.Column(db.DateTime)
