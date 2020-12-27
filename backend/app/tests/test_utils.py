from unittest.mock import MagicMock

import pytest
from flask import Flask

from app.jwt_utils import decode_token, encode_token
from app.utils import (
    generate_token,
    extract_header_data,
    get_user_id,
    process_sso_profile,
)


class TestGenerateToken:
    def test_generate_token_should_return_token_containing_encoded_user_id_and_major_id(
        self,
    ):
        app = Flask(__name__)
        app.config.update(SECRET_KEY="secret")
        user_id = 1010123
        major_id = 100

        with app.test_request_context():
            generated_token = generate_token(user_id, major_id)

            assert generated_token is not None
            assert type(generated_token) == str

            decoded_token = decode_token(generated_token)

            assert decoded_token is not None
            assert "user_id" in decoded_token.keys()
            assert "major_id" in decoded_token.keys()
            assert decoded_token["user_id"] == str(user_id)
            assert decoded_token["major_id"] == str(major_id)


class TestExtractHeaderData:
    def test_extract_valid_header_data(self):
        app = Flask(__name__)
        app.config.update(SECRET_KEY="secret")
        data = {"user": "testuser"}

        with app.test_request_context():
            token = encode_token(data)
            header = {"Authorization": f"JWT {token}"}

            extracted_header_data = extract_header_data(header)

            assert extracted_header_data is not None
            assert extracted_header_data == data

    def test_header_has_no_authorization_key(self):
        app = Flask(__name__)
        app.config.update(SECRET_KEY="secret")
        header = {"Cookie": "some-cookie"}

        with app.test_request_context():
            extracted_header_data = extract_header_data(header)

            assert extracted_header_data is None

    def test_header_authorization_has_incorrect_format(self):
        app = Flask(__name__)
        app.config.update(SECRET_KEY="secret")
        header = {"Authorization": "some-token"}

        with app.test_request_context():
            extracted_header_data = extract_header_data(header)

            assert extracted_header_data is None

    def test_header_authorization_header_type_and_value_switched(self):
        app = Flask(__name__)
        app.config.update(SECRET_KEY="secret")
        data = {"user": "testuser"}

        with app.test_request_context():
            token = encode_token(data)
            header = {"Authorization": f"{token} JWT"}

            extracted_header_data = extract_header_data(header)

            assert extracted_header_data is None

    def test_header_authorization_value_is_an_invalid_token(self):
        app = Flask(__name__)
        app.config.update(SECRET_KEY="secret")
        header = {"Authorization": f"JWT random-token"}

        with app.test_request_context():
            extracted_header_data = extract_header_data(header)

            assert extracted_header_data is None


class TestGetUserId:
    def test_given_extracted_header_data_with_user_id_should_return_user_id(self):
        app = Flask(__name__)
        app.config.update(SECRET_KEY="secret")
        data = {"user_id": "testuserid"}

        with app.test_request_context():
            token = encode_token(data)
            header = {"Authorization": f"JWT {token}"}
            mock_request = MagicMock()
            mock_request.headers = header

            user_id = get_user_id(mock_request)

            assert user_id is not None
            assert user_id == data["user_id"]

    def test_given_extracted_header_data_without_user_id_should_return_none(self):
        app = Flask(__name__)
        app.config.update(SECRET_KEY="secret")
        data = {"some_data": "testuserid"}

        with app.test_request_context():
            token = encode_token(data)
            header = {"Authorization": f"JWT {token}"}
            mock_request = MagicMock()
            mock_request.headers = header

            user_id = get_user_id(mock_request)

            assert user_id is None

    def test_given_invalid_request_header_should_return_none(self):
        app = Flask(__name__)
        app.config.update(SECRET_KEY="secret")
        header = {"Authorization": f"JWT invalid-token"}

        with app.test_request_context():
            mock_request = MagicMock()
            mock_request.headers = header

            user_id = get_user_id(mock_request)

            assert user_id is None


@pytest.mark.usefixtures("mongo")
class TestProcessSSOProfile:
    def test_update_course_with_invalid_sso_profile_return_result(self):
        app = Flask(__name__)
        with app.test_request_context():
            app.config.update(ACTIVE_PERIOD="2020-2")
            sso_profile = {
                "attributes": {
                    "npm": 123456789,
                    "study_program": "Ilmu Komputer (Computer Science)",
                    "kd_org": "01.00.12.01",
                    "ldap_cn": "randomldap",
                },
                "username": "testuser",
            }

            result = process_sso_profile(sso_profile)

            assert result is not None
            assert "err" in result.keys()
            assert "major_name" in result.keys()
            assert result["err"]
            assert result["major_name"] == sso_profile["attributes"]["study_program"]
