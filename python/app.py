import ast
import logging
import requests

from copy import deepcopy
from datetime import date, datetime
from dateutil.parser import parse
from operator import itemgetter

from flask import Flask, jsonify, request, session
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def main(argv):
    global booked_times
    global unavailable


def call_availability_api(method):
    if method == 'GET':
        response = requests.get('https://www.thinkful.com/api/advisors/availability')

    try:
        return response.json()
    except Exception as exception:
        logging.error(
            'call_availability_api in availability app '
            'failed with error: {0}'
            'and response: {1}'.format(
                exception,
                response
            )
        )


def get_unavailable():
    global unavailable
    try:
        return unavailable
    except NameError:
        return []


def get_booked_times():
    global booked_times
    try:
        return booked_times
    except NameError:
        return []


def update_unavailable(unavailable_time):
    global unavailable
    try:
        unavailable = unavailable
    except NameError:
        unavailable = []

    unavailable.append(unavailable_time)


def update_booked_times(booked_time):
    global booked_times
    try:
        booked_times = booked_times
    except NameError:
        booked_times = []

    booked_times.append(booked_time)


def check_available(open_time, advisor_id):
    unavailable = get_unavailable()
    if (open_time, advisor_id) not in unavailable:
        return True


def availability_by_time(date_availability):
    availability_times = {}
    for day in date_availability:
        availability_times.update(date_availability[day])

    return availability_times


def availability_by_advisor(date_availability):
    available_times = availability_by_time(date_availability)
    availability_by_id_dict = {}
    for timestamp in available_times:
        open_time = parse(timestamp)
        open_time = datetime.strftime(open_time, '%m/%d/%Y %I:%M %p')
        advisor_id = available_times[timestamp]
        available = check_available(open_time, advisor_id)
        if available:
            try:
                availability_by_id_dict[advisor_id]['open_times'].append(open_time)
                availability_by_id_dict[advisor_id]['open_times'].sort()
            except KeyError:
                availability_by_id_dict[advisor_id] = {
                    'id': advisor_id,
                    'open_times': [open_time]
                }

    return sorted(list(availability_by_id_dict.values()), key=itemgetter('id'))


def book_time(selection_data):
    student_name = selection_data.get('student_name')
    chosen_time = selection_data.get('chosen_time')
    advisor_id = selection_data.get('advisor_id')

    chosen_time_dict = {
        'student_name': student_name,
        'chosen_time': chosen_time,
        'advisor_id': advisor_id
    }

    update_booked_times(chosen_time_dict)
    update_unavailable((chosen_time, advisor_id))


@app.route("/today", methods=["GET"])
def today():
    return jsonify({"today": date.today().isoformat()})


@app.route("/availability", methods=["GET"])
def availabile_advisor_times():
    date_availability = call_availability_api('GET')
    advisor_availability = availability_by_advisor(date_availability)

    return jsonify({'availability': advisor_availability})


@app.route("/selected", methods=["POST"])
def selected():
    selection_data = ast.literal_eval(request.data.decode())
    book_time(selection_data)

    return 'Success'


@app.route("/booked", methods=["GET"])
def booked():
    booked = get_booked_times()

    return jsonify({'booked': booked})
