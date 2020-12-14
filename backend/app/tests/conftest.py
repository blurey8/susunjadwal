import pytest
from app import app
from flask import current_app

@pytest.fixture(scope='module')
def client():
    """Generate test client for every module"""
    with app.test_client() as client:
        with app.app_context():
            app.config.update(
                TESTING=True,
                ENV='test'
            )
            assert current_app.config["TESTING"] == True
            assert current_app.config["ENV"] == "test"
        yield client