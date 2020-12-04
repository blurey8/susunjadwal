import pytest
from app import app
from app.tests.utils import SERVICE_URL, get_ticket_from_sso_ui
from utils.fixtures import mongo
import mongoengine as me

BASE_PATH = app.config["BASE_PATH"] 

@pytest.mark.usefixtures('mongo')
class TestAuth:
    """Test authentication endpoint"""

    def test_auth(self, client):
        ticket = get_ticket_from_sso_ui()
        service_url = SERVICE_URL
        assert ticket is not None

        res = client.post(BASE_PATH + '/auth/',
                        json={'ticket': ticket, 'service_url': service_url})
        assert res.status_code == 200

        res_data = res.get_json()
        assert res_data['token'] is not None
        assert res_data['major_id'] is not None
        assert res_data['user_id'] is not None
        