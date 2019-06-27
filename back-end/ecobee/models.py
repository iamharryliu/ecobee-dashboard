from ecobee import db


class apis(db.Model):
    name = db.Column(db.String(20), unique=True, nullable=False)
    api_key = db.Column(db.String(32), primary_key=True, unique=True, nullable=False)
    authorization_code = db.Column(db.String(32), nullable=False)
    access_token = db.Column(db.String(32), nullable=False)
    refresh_token = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return f'<API:{self.name}:{self.api_key}>'
