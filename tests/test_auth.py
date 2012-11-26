
from __future__ import absolute_import

from base import ReutersTestCase

class AuthenticationTest(ReutersTestCase):

    def test_not_authed(self):
        assert self.reuters._token is None

    def test_auth(self):
        with open(self.get_datafile('headline_response.xml')) as response_file:
            self.reuters._request.return_value = response_file.read()
        assert self.reuters._create_service_token() == True

        with open(self.get_datafile('token')) as token_file:
            token = token_file.read().strip()
        assert self.reuters._token == token
