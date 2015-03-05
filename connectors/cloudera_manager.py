#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Huna
# cloudera_manager.py

from __future__ import unicode_literals
import time
import datetime
import urllib2

from cm_api.api_client import ApiResource
from flask import current_app as app

from base_connector import BaseConnector


class ClouderaManager(BaseConnector):

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

        return {'xAxis': range(180, 1, -1), 'yAxis': d}

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

        return {'xAxis': range(180, 1, -1), 'yAxis': d}

    def server_status(self):
        return [{'group': self.convert_health(s.healthSummary),
                 'cluster': c.name,
                 'service': s.name,
                 'health': s.healthSummary,
                 'state': s.serviceState}
                for c in self.api.get_all_clusters()
                for s in c.get_all_services()]

    def server_stats(self):
        return self.list_of_dict_stats(self.server_status(), 'group')

    def server_group(self, grp):
        return filter(lambda x: x['group'] == grp, self.server_status())

    def server_service_group(self, grp):
        return ' ,'.join(map(lambda x: x['service'], self.server_group(grp)))
    @staticmethod
    def hc_line(data, container, unit):
        d = {
            'chart': {'renderTo': container},
            'title': {'text': ''},
            'credits': {'enabled': False},
            'xAxis': {'categories': data['xAxis']},
            'yAxis': {
                'title': {'enabled': False},
                'plotLines': [{'value': 0, 'width': 1, 'color': '#808080'}]
            },
            'tooltip': {'valueSuffix': unit},
            'legend': {
                'enabled': False
            },
            'series': []
        }
        for key, value in data['yAxis'].iteritems():
            d['series'].append({'name': key, 'data': value})

        return d
