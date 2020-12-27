from unittest.mock import patch, MagicMock

from app.decorators import require_same_user_id, require_jwt_token
from app.jwt_utils import encode_token


class TestRequiresSameUserIdDecorator:
    @patch("app.decorators.request")
    def test_same_user_id_should_return_the_decorated_function(self, mock_request):
        user_id = "testID"

        with patch(
            "app.decorators.extract_header_data", return_value={"user_id": user_id}
        ):
            mock_function = MagicMock()
            decorated = require_same_user_id(mock_function)

            # Make sure that the returned function is the same as the mocked function
            assert decorated(user_id=user_id) == mock_function(user_id=user_id)

    @patch("app.decorators.request")
    @patch("app.decorators.jsonify")
    def test_different_user_id_should_return_401(self, mock_request, mock_jsonify):
        with patch(
            "app.decorators.extract_header_data", return_value={"user_id": "testID"}
        ):
            mock_function = MagicMock()
            decorated = require_same_user_id(mock_function)

            assert decorated(user_id="1234")[-1] == 401


class TestRequireJWTTokenDecorator:
    @patch("app.decorators.request")
    @patch("app.decorators.jsonify")
    def test_no_token_in_header_should_return_401(self, mock_request, mock_jsonify):
        mock_request.headers.return_value = {}

        mock_function = MagicMock()
        decorated = require_jwt_token(mock_function)

        assert decorated()[-1] == 401

    @patch("app.jwt_utils.app")
    @patch("app.decorators.request")
    def test_token_in_header_should_return_the_decorated_function(
        self, mock_request, mock_app
    ):
        mock_app.config = {"SECRET_KEY": "secret"}
        token = encode_token({"data": "SomeData"})
        mock_request.headers = {"Authorization": f"JWT {token}"}

        mock_function = MagicMock()
        decorated = require_jwt_token(mock_function)

        assert decorated() == mock_function()
