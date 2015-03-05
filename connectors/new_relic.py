#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Huna
# new_relic.py

from __future__ import unicode_literals

from flask import current_app as app
from newrelic_api import Applications, Servers
from requests.exceptions import ConnectionError

from base_connector import BaseConnector


class NewRelic(BaseConnector):

    def __init__(self, api_key=None):
        self.success = False
        try:
            self.api_key = api_key if api_key else app.config.get('NEWRELIC_KEY', None)
            Servers(api_key=self.api_key).list()
            self.success = True
        except ConnectionError:
            pass
        app.logger.info('NewRelic.success: %s' % self.success)

    def get_servers_statuses(self):
        return [{'host': s['host'], 'health': s['health_status']}
                for s in Servers(api_key=self.api_key).list()['servers']]

    def get_apps_statuses(self):
        return [{'name': s['name'], 'health': s['health_status']}
                for s in Applications(api_key=self.api_key).list()['applications']]

    def groupby_archi_stats(self, stats=None):
        stats = stats if stats else self.get_apps_statuses()

        app.logger.info(stats)
        grouped_stats = {}

        for s in stats:
            if 'Prod'.upper() in s['name'].upper():
                grouped_stats.update({'Production': s})
            elif 'Inte'.upper() in s['name'].upper():
                grouped_stats.update({'Integration': s})
            elif 'Develop'.upper() in s['name'].upper():
                grouped_stats.update({'Develop': s})

        return grouped_stats

    def health_stats(self):
        return self.list_of_dict_stats(self.get_servers_statuses(), 'health')
