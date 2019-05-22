from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class EcobeeAppForm(FlaskForm):
    name = StringField('Name (whatever you want)', validators=[DataRequired()])
    api_key = StringField('API Key', validators=[DataRequired()])
    authorization_code = StringField('Authorization Code', validators=[DataRequired()])
    access_token = StringField('Access Token', validators=[DataRequired()])
    refresh_token = StringField('Refresh Token', validators=[DataRequired()])
    submit = SubmitField('Submit')
