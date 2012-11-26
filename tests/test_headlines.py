
from __future__ import absolute_import

from mock import MagicMock

from base import ReutersTestCase


class HeadlinesTest(ReutersTestCase):
    
    def setUp(self):
        super(HeadlinesTest, self).setUp()
        self.reuters.token_is_valid = MagicMock(return_value=True)

        with open(self.get_datafile('headline_response.xml')) as response:
            self.reuters._request.return_value = response.read() 

        topic = 'OLBRTOPNEWS'
        self.headlines = self.reuters.get_headlines(topic)

    def test_id(self):
        pass

    def test_headline_short(self):
        pass

    def test_headline_long(self):
        pass
    
    def test_thumbnail(self):
        pass

    def test_date(self):
        pass
    
    def test_img_ref(self):
        pass

    def test_img_title(self):
        pass

    def test_img_date(self):
        pass
