#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Huna

from __future__ import unicode_literals
import time
import datetime

from cm_api.api_client import ApiResource

import utils

class ClouderaManager():
    def __init__(self, host, port, username, password):
        self.host = host
        self.api = ApiResource(host, port, username, password)

    def cpu_usage(self):
        from_time = datetime.datetime.fromtimestamp(time.time() - 3*3600)
        to_time = datetime.datetime.fromtimestamp(time.time())
        query = 'SELECT cpu_percent'
        result = self.api.query_timeseries(query, from_time, to_time)
        dict={}
        for ts in result[0].timeSeries:
            server = ts.metadata.entityName
            dict[server] = []
            for val in ts.data:
                dict[server].append(val.value)

        return dict

    def mem_usage(self):
        from_time = datetime.datetime.fromtimestamp(time.time() - 3*3600)
        to_time = datetime.datetime.fromtimestamp(time.time())
        query = 'SELECT physical_memory_used'
        result = self.api.query_timeseries(query, from_time, to_time)
        dict={}
        for ts in result[0].timeSeries:
            server = ts.metadata.entityName
            dict[server] = []
            for val in ts.data:
                dict[server].append(val.value)

        return dict

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