# -*- coding: utf-8 -*-

from __future__ import absolute_import

from operator import itemgetter

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

    def assertFieldEqual(self, field, value, index=0):
        assert self.headlines[index][field] == value

    def test_id(self):
        self.assertFieldEqual('id', 'urn:newsml:onlinereport.com:20121126:nRTROPT20121126175040SPE8AP07R')

    def test_headline_short(self):
        self.assertFieldEqual('headline_short', u'Oposi\xe7\xe3o quer ouvir envolvidos na opera\xe7\xe3o Porto Seguro no Congresso')

    def test_headline_long(self):
        self.assertFieldEqual('headline_long', u'BRAS\xcdLIA, 26 Nov (Reuters) - Os partidos de oposi\xe7\xe3o ao governo se articulam no Congresso para ouvir os servidores federais que est\xe3o sendo investigados pela opera\xe7\xe3o Porto Seguro, da Pol\xedcia Federal, mesmo ap\xf3s a determina\xe7\xe3o da presidente Dilma Rousseff para exonerar e afastar os envolvidos.')

    def test_thumbnail(self):
        self.assertFieldEqual('thumbnail', '2012-11-26T155415Z_1_BSPE8AP186H00_RTROPTP_1_MANCHETES-ENERGIA-SET-PETROBRAS.JPG', index=-2)

    def test_date(self):
        self.assertFieldEqual('date', '20121126T175040+0000')

    def test_image_ref(self):
        self.assertFieldEqual('image_ref', 'urn:newsml:onlinereport.com:20121126:nRTROPT20121126155415BSPE8AP186H00', index=-2)

    def test_image_title(self):
        self.assertFieldEqual('image_title', u'Produção do pré-sal evitou queda maior na extração da Petrobras', index=-2)

    def test_image_date(self):
        self.assertFieldEqual('image_date', '20121126T155415+0000', index=-2)
