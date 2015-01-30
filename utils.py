#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Huna
# utils.py

from collections import Counter


def list_of_dict_stats(list_of_dict, key):
    return Counter(map(lambda x: x[key], list_of_dict))
