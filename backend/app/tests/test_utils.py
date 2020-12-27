from unittest.mock import patch, MagicMock

from app.utils import generate_token, extract_header_data, get_user_id
from app.jwt_utils import decode_token, encode_token


class TestGenerateToken:
    @patch("app.jwt_utils.app")
    def test_generate_token_should_return_token_containing_encoded_user_id_and_major_id(
        self, mock_app
    ):
        mock_app.config = {"SECRET_KEY": "secret"}

        user_id = 1010123
        major_id = 100
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
    @patch("app.jwt_utils.app")
    def test_extract_valid_header_data(self, mock_app):
        mock_app.config = {"SECRET_KEY": "secret"}
        data = {"user": "testuser"}
        token = encode_token(data)
        header = {"Authorization": f"JWT {token}"}

        extracted_header_data = extract_header_data(header)

        assert extracted_header_data is not None
        assert extracted_header_data == data

    @patch("app.jwt_utils.app")
    def test_header_has_no_authorization_key(self, mock_app):
        mock_app.config = {"SECRET_KEY": "secret"}
        header = {"Cookie": "some-cookie"}

        extracted_header_data = extract_header_data(header)

        assert extracted_header_data is None

    @patch("app.jwt_utils.app")
    def test_header_authorization_has_incorrect_format(self, mock_app):
        mock_app.config = {"SECRET_KEY": "secret"}
        header = {"Authorization": "some-token"}

        extracted_header_data = extract_header_data(header)

        assert extracted_header_data is None

    @patch("app.jwt_utils.app")
    def test_header_authorization_header_type_and_value_switched(self, mock_app):
        mock_app.config = {"SECRET_KEY": "secret"}
        data = {"user": "testuser"}
        token = encode_token(data)
        header = {"Authorization": f"{token} JWT"}

        extracted_header_data = extract_header_data(header)

        assert extracted_header_data is None

    @patch("app.jwt_utils.app")
    def test_header_authorization_value_is_an_invalid_token(self, mock_app):
        mock_app.config = {"SECRET_KEY": "secret"}
        header = {"Authorization": f"JWT random-token"}

        extracted_header_data = extract_header_data(header)

        assert extracted_header_data is None


class TestGetUserId:
    @patch("app.jwt_utils.app")
    def test_given_extracted_header_data_with_user_id_should_return_user_id(
        self, mock_app
    ):
        mock_app.config = {"SECRET_KEY": "secret"}
        data = {"user_id": "testuserid"}
        token = encode_token(data)
        header = {"Authorization": f"JWT {token}"}
        mock_request = MagicMock()
        mock_request.headers = header

        user_id = get_user_id(mock_request)

        assert user_id is not None
        assert user_id == data["user_id"]

    @patch("app.jwt_utils.app")
    def test_given_extracted_header_data_without_user_id_should_return_none(
        self, mock_app
    ):
        mock_app.config = {"SECRET_KEY": "secret"}
        data = {"some_data": "testuserid"}
        token = encode_token(data)
        header = {"Authorization": f"JWT {token}"}
        mock_request = MagicMock()
        mock_request.headers = header

        user_id = get_user_id(mock_request)

        assert user_id is None

    @patch("app.jwt_utils.app")
    def test_given_invalid_request_header_should_return_none(self, mock_app):
        mock_app.config = {"SECRET_KEY": "secret"}
        header = {"Authorization": f"JWT invalid-token"}
        mock_request = MagicMock()
        mock_request.headers = header

        user_id = get_user_id(mock_request)

        assert user_id is None
