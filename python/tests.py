import json
import requests

from datetime import date
from operator import itemgetter
from pytest import fixture

import app


class TestNonApiFunctions(object):
    def setup_class(self):
        app.booked_times = [
            {
                'student_name': 'Crystal Arnspiger',
                'chosen_time': '08/04/2019 11:30 AM',
                'advisor_id': '319444'
            }
        ]
        app.unavailable = [('08/24/2019 10:30 AM', '319500')]
        self.booked_times = app.booked_times
        self.unavailable = app.unavailable

    def teardown_class(self):
        app.booked_times = []
        app.unavailable = []
        self.booked_times = app.booked_times
        self.unavailable = app.unavailable

    def test_get_unavailable(self):
        unavailable = app.get_unavailable()
        assert unavailable == self.unavailable

    def test_get_booked_times(self):
        booked_times = app.get_booked_times()
        assert booked_times == self.booked_times

    def test_update_unavailable(self):
        unavailable_time = ('888888', '08/19/2019 12:00 PM')
        app.update_unavailable(unavailable_time)
        assert unavailable_time in app.unavailable

    def test_update_booked_times(self):
        booked_time = {
            'student_name': 'Stephen Pouncey',
            'chosen_time': '08/04/2019 10:30 AM',
            'advisor_id': '319370'
        }
        app.update_booked_times(booked_time)
        assert booked_time in app.booked_times

    def test_check_available(self):
        open_time = '08/19/2019 12:00 PM'
        advisor_id = '888888'
        check_available = app.check_available(open_time, advisor_id)
        assert check_available == True

    def test_check_available_none(self):
        open_time = '08/24/2019 10:30 AM'
        advisor_id = '319500'
        check_available = app.check_available(open_time, advisor_id)
        assert check_available == None

    def test_book_time(self):
        selection_data  = {
            'student_name': 'Stephen Pouncey',
            'chosen_time': '08/04/2019 10:30 AM',
            'advisor_id': '319370'
        }
        app.book_time(selection_data)
        assert selection_data in app.booked_times
        assert ('08/04/2019 10:30 AM', '319370') in app.unavailable


class TestCallExternalApiFunctions(object):
    def setup_class(self):
        response = requests.get('https://www.thinkful.com/api/advisors/availability')
        self.date_availability = response.json()
        self.date_key = list(self.date_availability.keys())[0]
        print (self.date_key)

    def test_call_availabilty_api(self):
        availability = app.call_availability_api('GET')
        assert isinstance(availability, dict) == True

    def test_availability_by_time(self):
        test_available_times = self.date_availability[self.date_key]
        available_times = app.availability_by_time(self.date_availability)
        for test_time in test_available_times:
            assert test_available_times[test_time] == available_times[test_time]

    def test_availability_by_advisor(self):
        test_available_times = self.date_availability[self.date_key]
        availability_by_id = app.availability_by_advisor(self.date_availability)
        test_availability_ids = []
        for availability in availability_by_id:
            test_availability_ids.append(availability['id'])
        for test_time in test_available_times:
            advisor = test_available_times[test_time]
            assert advisor in test_availability_ids

    def test_availability_by_advisor(self):
        test_date = '99/99/9999'
        test_time = '06/10/2000 10:00 AM'
        test_advisor = 99999999999
        self.date_availability[test_date] = {
            test_time: test_advisor
        }
        app.unavailable = [(test_time, test_advisor)]
        availability_by_id = app.availability_by_advisor(self.date_availability)
        test_availability_ids = []
        for availability in availability_by_id:
            test_availability_ids.append(availability['id'])
            print (availability['id'])
        assert test_advisor not in  test_availability_ids


class TestApis(object):
    def setup_class(self):
        app.booked_times = [
            {
                'student_name': 'Crystal Arnspiger',
                'chosen_time': '08/04/2019 11:30 AM',
                'advisor_id': '319444'
            }
        ]
        app.unavailable = [('08/24/2019 10:30 AM', '319500')]

    def teardown_class(self):
        app.booked_times = []
        app.unavailable = []

    def test_today(self):
        with app.app.test_client() as cli:
            resp = cli.get('/today')
            assert resp.status_code == 200
            assert resp.json == {"today": "{}".format(date.today())}

    def test_availability(self):
        with app.app.test_client() as cli:
            resp = cli.get('/availability')
            assert resp.status_code == 200
            assert 'availability' in resp.json
            assert 'id' in resp.json['availability'][0]
            assert 'open_times' in resp.json['availability'][0]

    def test_booked(booked_times):
        with app.app.test_client() as cli:
            resp = cli.get('/booked')
            print (resp.json)
            assert resp.status_code == 200
            assert 'Crystal Arnspiger' in resp.json['booked'][0].values()

    def test_selected(self):
        with app.app.test_client() as cli:
            data = {
                'student_name': 'Stephen Pouncey',
                'chosen_time': '08/04/2019 10:30 AM',
                'advisor_id': '319370'
            }
            resp = cli.post(
                '/selected',
                headers = {
                    'Content-Type': 'application/json'
                },
                data = json.dumps(data)
            )
            assert resp.status_code == 200
            assert b'Success' in resp.data
