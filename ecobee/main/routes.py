from flask import Blueprint, render_template, flash
from ecobee import db
from ecobee.apps.utils import Ecobee_API
from ecobee.models import apis
import csv

main = Blueprint("main", __name__, template_folder="templates")


@main.route("/")
def home():
    return render_template("main/view.html")
