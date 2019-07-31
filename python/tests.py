from app import app
from datetime import date


def test_today():
    with app.test_client() as cli:
        resp = cli.get('/today')
        assert resp.status_code == 200
        assert resp.json == {"today": "{}".format(date.today())}


def test_availability():
    with app.test_client() as cli:
        resp = cli.get('/availability')
        assert resp.status_code == 200
        assert 'availability' in resp.json
        assert 'id' in resp.json['availability'][0]
        assert 'opentimes' in resp.json['availability'][0]


def test_selected():
    with app.test_client() as cli:
        resp = cli.post(
            '/selected',
            headers = {
                'Content-Type': 'application/json'
            },
            data = "{'student_name': 'Crystal Arnspiger','chosen_time': '08/04/2019 10:30 AM','advisor_id': '319369'}"
        )
        assert resp.status_code == 200
        assert b'Success' in resp.data


def test_booked():
    with app.test_client() as cli:
        resp = cli.get('/booked')
        assert resp.status_code == 200
        assert 'Crystal Arnspiger' in resp.json['booked'][0].values()
