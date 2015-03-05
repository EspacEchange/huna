#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Huna

from __future__ import unicode_literals
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template

from connectors.cloudera_manager import ClouderaManager
from connectors.new_relic import NewRelic

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
    cm_test = ClouderaManager(app.config.get('CLOUDERA_TEST_HOST', '127.0.0.1'),
                         app.config.get('CLOUDERA_TEST_PORT', 7180),
                         app.config.get('CLOUDERA_TEST_USERNAME', 'admin'),
                         app.config.get('CLOUDERA_TEST_PASSWORD', 'password'))
    cm_prod = ClouderaManager(app.config.get('CLOUDERA_PROD_HOST', '127.0.0.1'),
                         app.config.get('CLOUDERA_PROD_PORT', 7180),
                         app.config.get('CLOUDERA_PROD_USERNAME', 'admin'),
                         app.config.get('CLOUDERA_PROD_PASSWORD', 'password'))
    nr = NewRelic()
    return render_template('layout.html', cm_test=cm_test, cm_prod=cm_prod, nr=nr)


# Favicon route
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('img/favicon.ico')

if __name__ == '__main__':
    app.run(host=app.config.get('HOST', '0.0.0.0'),
            port=app.config.get('PORT', 5000))
