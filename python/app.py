import ast
from copy import deepcopy
from datetime import date, datetime
from dateutil.parser import parse
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from operator import itemgetter
import requests


app = Flask(__name__)
CORS(app)


def main(argv):
    global chosen_times
    global unavailable


@app.route("/today", methods=["GET"])
def today():
    return jsonify({"today": date.today().isoformat()})


@app.route("/availability", methods=["GET"])
def availability():
    availability_by_id_dict = {}
    response = requests.get('https://www.thinkful.com/api/advisors/availability')
    availability_by_date = response.json()
    global unavailable
    try:
        unavailable = unavailable
    except NameError:
        unavailable = []
    for day in availability_by_date:
        for timestamp in availability_by_date[day]:
            opentime = parse(timestamp)
            opentime = datetime.strftime(opentime, '%m/%d/%Y %I:%M %p')
            advisor_id = availability_by_date[day][timestamp]
            if (opentime, advisor_id) not in unavailable:
                try:
                    availability_by_id_dict[advisor_id]['opentimes'].append(opentime)
                    availability_by_id_dict[advisor_id]['opentimes'].sort()
                except KeyError:
                    availability_by_id_dict[availability_by_date[day][timestamp]] = {
                        'id': advisor_id,
                        'opentimes': [opentime]
                    }
    availability_by_id = sorted(list(availability_by_id_dict.values()), key=itemgetter('id'))

    return jsonify({'availability': availability_by_id})


@app.route("/selected", methods=["POST"])
def selected():
    data = ast.literal_eval(request.data.decode())
    student_name = data.get('student_name')
    chosen_time = data.get('chosen_time')
    advisor_id = data.get('advisor_id')

    chosen_time_dict = {
        'student_name': student_name,
        'chosen_time': chosen_time,
        'advisor_id': advisor_id
    }
    unavailable_time = (chosen_time, advisor_id)

    global unavailable
    try:
        unavailable.append(unavailable_time)
    except NameError:
        unavailable = [unavailable_time]

    global chosen_times
    try:
        chosen_times.append(chosen_time_dict)
    except NameError:
        chosen_times = [chosen_time_dict]
    
    return 'Success'


@app.route("/booked", methods=["GET"])
def booked():
    try:
        global chosen_times
        booked = chosen_times
    except NameError:
        booked = []

    return jsonify({'booked': booked})
