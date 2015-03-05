#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Huna

from __future__ import unicode_literals
import time
import datetime
import urllib2

from cm_api.api_client import ApiResource
from flask import current_app as app

import utils


class ClouderaManager():
    def __init__(self, host, port, username, password):
        self.host = host
        self.success = False
        try:
            self.api = ApiResource(host, port, username, password)
            self.api.get_all_clusters()
            self.success = True
        except urllib2.URLError:
            pass
        app.logger.info('ClouderaManager.success: %s' % self.success)

    def cpu_usage(self):
        from_time = datetime.datetime.fromtimestamp(time.time() - 3 * 3600)
        to_time = datetime.datetime.fromtimestamp(time.time())
        query = 'SELECT cpu_percent'
        result = self.api.query_timeseries(query, from_time, to_time)
        d = {}
        for ts in result[0].timeSeries:
            server = ts.metadata.entityName
            d[server] = []
            for val in ts.data:
                d[server].append(val.value)

        return d

    def mem_usage(self):
        from_time = datetime.datetime.fromtimestamp(time.time() - 3 * 3600)
        to_time = datetime.datetime.fromtimestamp(time.time())
        query = 'SELECT physical_memory_used'
        result = self.api.query_timeseries(query, from_time, to_time)
        d = {}
        for ts in result[0].timeSeries:
            server = ts.metadata.entityName
            d[server] = []
            for val in ts.data:
                d[server].append(val.value)

        return d

    def server_status(self):
        return [{'group': self.convert_health(s.healthSummary),
                 'cluster': c.name,
                 'service': s.name,
                 'health': s.healthSummary,
                 'state': s.serviceState}
                for c in self.api.get_all_clusters()
                for s in c.get_all_services()]

    def convert_health(self, health):
        if health not in ['GOOD', 'BAD']:
            return 'OTHER'
        return health

    def server_stats(self):
        return utils.list_of_dict_stats(self.server_status(), 'group')

    def server_bad(self):
        return filter(lambda x: x['group'] == 'OTHER', self.server_status())
