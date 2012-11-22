#!/usr/bin/env python

import logging
from reuters import Reuters

log = logging.getLogger('reuters.xml')
log.setLevel(logging.INFO)

application_id = '...'
username = '...'
password = '...'
topic = '...'

r = Reuters(application_id, username, password)
print r.get_headlines(topic)
