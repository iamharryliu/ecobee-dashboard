from flask import Blueprint, render_template, flash
from ecobee import db
from ecobee.models import apis


main = Blueprint("main", __name__, template_folder="templates")


def format_file_data_as_array(f):
    data = f.read().splitlines()[0]
    data = data.split(',')
    array = [int(value) if value != '' else 'null' for value in data if value][-30:]
    return array


def get_series(sensors):
    series = []
    for sensor in sensors:
        with open(f'ecobee/logs/temperature/{sensor}', 'r') as f:
            data = format_file_data_as_array(f)
        sensor = {"name": sensor, "data": data}
        series.append(sensor)
    return series


def get_time_axis():
    with open('ecobee/logs/time', 'r') as f:
        time = format_file_data_as_array(f)
    return time


@main.route("/graph")
def graph(chartID='chart_ID', chart_type='line'):
    sensors = ['s1', 's2', 's3']
    time = get_time_axis()
    chart = {"renderTo": chartID, "type": chart_type}
    series = get_series(sensors)
    title = {"text": 'Thermostat'}
    xAxis = {"categories": time}
    yAxis = {"title": {"text": 'Temperature'}}
    return render_template('main/graph.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)


@main.route("/")
def home():
    return render_template("main/view.html")
