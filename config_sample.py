#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Huna
# config.py

from __future__ import unicode_literals

# Flask
DEBUG = True
LOG_FILE = 'huna_dashboard.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s :: %(message)s'
HOST = '0.0.0.0'
PORT = 5000 if DEBUG else 8000
STATIC_FOLDER = '/static'

# Huna
SITE_NAME = 'Huna Dashboard'

# New Relic
NEWRELIC_KEY = '87cc8e42ea238a1b3fb6448cecd53f1126ac83e0'

# Cloudera
CLOUDERA_HOST = 'http://clouderaurl.fr'
CLOUDERA_PORT = 7180
CLOUDERA_USERNAME = 'admin'
CLOUDERA_PASSWORD = 'password'

# Jenkins
JENKINS_URL = 'http://jenkinsurl.fr'
JENKINS_KEY = '87cc8e42ea238a1b3fb6448cecd53f1126ac83e0'
