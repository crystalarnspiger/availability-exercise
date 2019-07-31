from datetime import date
from app import app


def test_today():
    with app.test_client() as cli:
        resp = cli.get('/today')
        assert resp.status_code == 200
        assert resp.json == {"today": "{}".format(date.today())}
