#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Huna
# base_connector.py

from __future__ import unicode_literals
from collections import Counter


class BaseConnector():

    def __init__(self, api_key=None, host=None, port=None, username=None, password=None):
        self.success = False
        self.api_key = None
        self.host = None
        self.port = None
        self.username = None
        self.password = None

    def list_of_dict_stats(self, list_of_dict, key):
        return Counter(map(lambda x: x[key], list_of_dict))

    def convert_health(self, health):
        if health not in ['GOOD', 'BAD']:
            return 'OTHER'
        return health
