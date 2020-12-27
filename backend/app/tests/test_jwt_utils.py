from unittest.mock import patch

from app.jwt_utils import encode_token, decode_token


class TestJWTUtils:
    @classmethod
    def setup_class(cls):
        cls.data = {"data_1": "confidential", "data_2": 123456}

    @patch("app.jwt_utils.app")
    def test_encode_token_should_produce_jwt_token(self, mock_app):
        mock_app.config = {"SECRET_KEY": "jwt-secret"}

        encoded_token = encode_token(self.data)

        assert encoded_token is not None
        assert type(encoded_token) == str

    @patch("app.jwt_utils.app")
    def test_decode_valid_token_should_return_the_decoded_data(self, mock_app):
        mock_app.config = {"SECRET_KEY": "jwt-secret"}
        encoded_token = encode_token(self.data)

        decoded_data = decode_token(encoded_token)

        assert decoded_data is not None
        assert decoded_data == self.data

    @patch("app.jwt_utils.app")
    def test_decode_invalid_token_should_return_none_type(self, mock_app):
        mock_app.config = {"SECRET_KEY": "jwt-secret"}

        invalid_tokens = [
            "",
            "random",
            1,
            0,
            -1,
            1.00,
            0.00,
            -1.00,
            b"random",
            ["token1", "token2"],
            [],
            {},
            {"token1", "token2"},
            {"key": "token"},
            ("token1", "token2"),
            (),
            True,
            False,
            None,
        ]

        for token in invalid_tokens:
            decoded_data = decode_token(token)
            assert decoded_data is None
