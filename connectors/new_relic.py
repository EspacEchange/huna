#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Huna
# new_relic.py

from __future__ import unicode_literals

from flask import current_app as app
from newrelic_api import Applications, Servers

import utils


class NewRelic():

    def __init__(self, api_key=None):
        self.api_key = api_key if api_key else app.config.get('NEWRELIC_KEY', None)

    def get_servers_statuses(self):
        return [{'host': s['host'], 'health_status': s['health_status']}
                for s in Servers(api_key=self.api_key).list()['servers']]

    def get_apps_statuses(self):
        return [{'name': s['name'], 'health_status': s['health_status']}
                for s in Applications(api_key=self.api_key).list()]

    def health_stats(self):
        return utils.list_of_d_stats(self.get_servers_statuses(), 'health_status')
