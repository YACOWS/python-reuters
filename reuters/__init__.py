# -*- encoding: utf-8 -*-

from __future__ import absolute_import

import uuid
import logging

import jinja2

from datetime import datetime
from xml.etree import ElementTree
from reuters import httpslib as httplib
from .utils import spaceless


class Reuters(object):

    def __init__(self, application_id, username, password, token=None):
        self._username = username
        self._password = password
        self._application_id = application_id
        self.logxml = logging.getLogger('reuters.xml')
        self.logxml.addHandler(logging.StreamHandler())
        self._token = token

        self._jinja_env = jinja2.Environment(
            autoescape=True,
            loader=jinja2.PackageLoader('reuters'),
        )

        self.http_client = httplib.HTTPSConnection('api.rkd.reuters.com')

    def _create_service_token(self):
        NS = 'http://www.reuters.com/ns/2006/05/01/webservices/rkd/Common_1'
        context = {
            'password': self._password,
            'username': self._username,
        }

        xml = self._render_template('create_service_token.xml', context)
        uri = '/api/TokenManagement/TokenManagement.svc/Anonymous'
        response = self._request(uri, xml)
        root = ElementTree.fromstring(response)
        self._token = root.find('.//{{{0}}}Token'.format(NS)).text.strip()
        return True


    def _render_template(self, template_name, context=None):
        if context is None:
            context = {}

        template = self._jinja_env.get_template(template_name)
        context.update({
            'message_id': uuid.uuid4().get_hex(),
            'token': self._token,
            'application_id': self._application_id,
        })
        xml = template.render(context)
        return xml

    def _query_reuters(self, template, context, uri):
        if not self.token_is_valid():
            self._create_service_token()
            if not self.token_is_valid():
                raise Exception

        xml = self._render_template(template, context)
        return self._request(uri, xml)

    def _str_to_dt(self, dt_str):
        dt_str = dt_str[:-6].replace("T", " ")
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        return dt

    def get_headlines(self, topic):
        template = 'get_headlines.xml'
        context = {'topic': topic}
        uri = '/api/OnlineReports/OnlineReports.svc'

        response = self._query_reuters(template, context, uri)
        root = ElementTree.fromstring(response)

        stories = []
        for story in root[1][0].getchildren():
            story_dict = {
                'id': story.get('ID'),
            }

            for elem in story.iter():
                if elem.tag.endswith('}HL'):
                    headline, desc = elem.getchildren()
                    story_dict['headline_short'] = headline.text
                    story_dict['headline_long'] = desc.text

                elif elem.tag.endswith('}Thumbnail'):
                    story_dict['thumbnail'] = elem.text.strip()

                elif elem.tag.endswith('}StoryDate'):
                    story_dict['date'] = elem.text # TODO: format

                elif elem.tag.endswith('}Ref'):
                    story_dict['image_ref'] = elem.text

                elif elem.tag.endswith('}Title'):
                    story_dict['image_title'] = elem.text

                elif elem.tag.endswith('}Date'):
                    story_dict['image_date'] = elem.text

            stories.append(story_dict)
        return stories

    def get_image(self, story_id):
        template = 'get_stories.xml' # some template?!
        context = {'story_id': story_id,
                    'application_id': self._application_id,
                    'token': self._token}
        uri = '/api/OnlineReports/OnlineReports.svc'

        response = self._query_reuters(template, context, uri)
        root = ElementTree.fromstring(response)
        
        image = {}

        for elem in root[1][0][0].getchildren():
            if elem.tag.endswith('}STORYML') and len(elem) > 0:
                for story_info in elem[0].getchildren():
                    if story_info.tag.endswith('}HT'):
                        image['title'] = story_info.text
                    for img_info in story_info.getchildren():
                         if img_info.attrib['Type'] == 'BaseRef':
                             image['base_url'] = img_info.text
        return image


    def get_story(self, story_id):
        template = 'get_stories.xml'
        context = {'story_id': story_id,
                    'application_id': self._application_id,
                    'token': self._token}
        uri = '/api/OnlineReports/OnlineReports.svc'

        response = self._query_reuters(template, context, uri)
        root = ElementTree.fromstring(response)
        
        story = {}
        
        for elem in root[1][0][0].getchildren():
            if elem.tag.endswith('}STORYML') and len(elem) > 0:
                for story_info in elem[0].getchildren():
                    if story_info.tag.endswith('}HT'):
                        story['title'] = story_info.text
                    if story_info.tag.endswith('}TE'):
                        story['content'] = story_info.text
                    if story_info.tag.endswith('}CT'):
                        story['ct'] = self._str_to_dt(story_info.text)
                    if story_info.tag.endswith('}RT'):
                        story['rt'] = self._str_to_dt(story_info.text)
                    if story_info.tag.endswith('}LT'):
                        story['lt'] = self._str_to_dt(story_info.text)
                    if story_info.tag.endswith('}SR'):
                        for img_info in story_info.getchildren():
                             if img_info.attrib['Type'] == 'ImageRef':
                                 story['image_ref'] = img_info.text

        return story

    def token_is_valid(self):
        NS = 'http://www.reuters.com/ns/2006/05/01/webservices/rkd/TokenManagement_1'
        if not self._token:
            return False

        xml = self._render_template('validate_token.xml')
        uri = '/api/TokenManagement/TokenManagement.svc'

        response = self._request(uri, xml)
        root = ElementTree.fromstring(response)
        valid = root.find('.//{{{0}}}Valid'.format(NS)).text.strip()
        if valid == 'true':
            return True
        else:
            return False

    def _request(self, uri, xml):

        if isinstance(xml, unicode):
            xml = xml.encode('utf-8')

        self.logxml.info('Requesting URI: %s', uri)
        self.logxml.debug(xml)
        #self.http_client.set_debuglevel(1)
        self.http_client.request('POST', uri, body=xml, headers={
            'Content-Type': 'application/soap+xml; charset=UTF-8',
            'Expect': '100-continue',
            'Connection': 'Keep-Alive',
        })

        response = self.http_client.getresponse()
        if response.status == 200:
            response_xml = response.read()
            self.logxml.debug(response_xml)
            return response_xml
        else:
            raise Exception #TODO
