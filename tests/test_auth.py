
from __future__ import absolute_import

from base import ReutersTestCase

class AuthenticationTest(ReutersTestCase):

    def test_not_authed(self):
        assert self.reuters._token is None

    def test_create_token(self):
        with open(self.get_datafile('create_token_response.xml')) as response:
            self.reuters._request.return_value = response.read()
        assert self.reuters._create_service_token() == True

        with open(self.get_datafile('token')) as token_file:
            token = token_file.read().strip()
        assert self.reuters._token == token

    def test_before_token_validation(self):
        assert self.reuters.token_is_valid() == False

    def test_token_validation_false(self):
        with open(self.get_datafile('token')) as token_file:
            self.reuters._token = token_file.read().strip()

        with open(self.get_datafile('validatetoken_false.xml')) as response:
            self.reuters._request.return_value = response.read()
        assert self.reuters.token_is_valid() == False

    def test_token_validation_true(self):
        with open(self.get_datafile('token')) as token_file:
            self.reuters._token = token_file.read().strip()

        with open(self.get_datafile('validatetoken_true.xml')) as response:
            self.reuters._request.return_value = response.read()
        assert self.reuters.token_is_valid() == True
