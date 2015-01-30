#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Huna
# new_relic.py

from __future__ import unicode_literals

from flask import current_app as app
from newrelic_api import Applications

app = Applications(api_key=app.config['NEWRELIC_KEY'])
