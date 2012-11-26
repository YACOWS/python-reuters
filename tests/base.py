
import os
import unittest

from mock import MagicMock

from reuters import Reuters

class ReutersTestCase(unittest.TestCase):

    def setUp(self):
        application_id = 'MyFakeApplicationID'
        username = 'fakeusername'
        password = 'FakePassword'
        self.reuters = Reuters(application_id, username, password)
        self.reuters._request = MagicMock()

    def get_datafile(self, filename):
        cwd = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(cwd, 'data', filename)

