import random
import string
from typing import List

from mongoengine import connect, disconnect


class TestBase:
    @classmethod
    def setup_class(cls):
        connect(db="mongoenginetest", host="mongomock://localhost")

    @classmethod
    def teardown_class(cls):
        disconnect()

    @classmethod
    def get_random_string(cls, length):
        letters = string.ascii_letters
        return "".join(random.choice(letters) for _ in range(length))

    @classmethod
    def assert_serialization_contains_keys(
        cls, keys: List[str], serialized_object: dict
    ):
        for k in keys:
            assert k in serialized_object.keys()
