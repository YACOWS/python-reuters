
from __future__ import absolute_import
from mock import MagicMock

from base import ReutersTestCase

class StoriesTest(ReutersTestCase):

    def setUp(self):
        super(StoriesTest, self).setUp()
        self.reuters.token_is_valid = MagicMock(return_value=True)
        story_id = 'urn:newsml:onlinereport.com:20121113:nRTROPT20121113133403SPE8AC01P'

        with open(self.get_datafile('story_response.xml')) as response_file:
            self.reuters._request.return_value = response_file.read()

        self.story = self.reuters.get_story(story_id)

    def test_title(self):
        assert self.story['title'] == 'Vendas no varejo brasileiro sobem 0,3% em setembro--IBGE'

    def test_content(self):
        assert self.story['content'] == 'My test content...'

    def test_creation_time(self):
        assert self.story['creation_time'] == '2012-11-13T13:34:03-00:00'

    def test_revision_time(self):
        assert self.story['revision_time'] == '2012-11-13T13:34:03-00:00'

    def test_local_time(self):
        assert self.story['local_time'] == '2012-11-14T11:20:07-00:00'

    def test_thumbnail(self):
        assert self.story['thumbnail'] == 'http://thumbnail_url'
