import pytest
from flask import Flask

from app.cron import update_courses
from models.period import Period


@pytest.mark.usefixtures("mongo")
class TestUpdateCourseCron:

    def test_without_majors_in_db(self):
        app = Flask(__name__)
        runner = app.test_cli_runner()

        runner.invoke(update_courses)

        assert len(Period.objects) == 0
