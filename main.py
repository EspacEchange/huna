#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Huna

from __future__ import unicode_literals
import logging
from logging.handlers import RotatingFileHandler
from collections import Counter

from flask import Flask, render_template

from connectors.cloudera_manager import ClouderaManager

# Build Flask instance with its config
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Getting a rotating log
handler = RotatingFileHandler(filename=app.config['LOG_FILE'],
                              backupCount=10, mode='a', maxBytes=1000000)
if app.debug:
    handler.setLevel(logging.DEBUG)
else:
    handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
app.logger.addHandler(handler)


# Homepage
@app.route('/')
def index():
    cm = ClouderaManager(app.config['CLOUDERA_HOST'], app.config['CLOUDERA_PORT'], app.config['CLOUDERA_USERNAME'], app.config['CLOUDERA_PASSWORD'])
    return render_template('layout.html', cm=cm)

# Favicon route
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('img/favicon.ico')

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])
