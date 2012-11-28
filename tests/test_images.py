
from __future__ import absolute_import
from datetime import datetime
from mock import MagicMock

from base import ReutersTestCase

class StoriesTest(ReutersTestCase):

    def setUp(self):
        super(StoriesTest, self).setUp()
        self.reuters.token_is_valid = MagicMock(return_value=True)
        story_id = 'urn:newsml:onlinereport.com:20121128:nRTROPT20121128121221BSPE8AR0XWP00'

        with open(self.get_datafile('image_response.xml')) as response_file:
            self.reuters._request.return_value = response_file.read()

        self.image = self.reuters.get_image(story_id)

    def test_image_base_url(self):
        assert self.image['base_url'] == 'http://api.rkd.reuters.com/api/onlinereports/2012-11-28T121221Z_1_BSPE8AR0XWP00_RTROPTP_3_MANCHETES-ARGENTINA-FITCH-CORTANOTA.JPG.ashx'

    def test_image_title(self):
        assert self.image['title'] == 'gasdgasdgasdgasd'
