#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 HomeWork Inc. All Rights Reserved.
# Author: shookuooo@gmail.com

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import flask as f

import log
import kid_edu_bp
import kid_game_bp


def create_app(config_filename):
    app = f.Flask(__name__)
    app.config.from_pyfile(config_filename)

    # Enables logging. Put it right after app.
    if not os.path.exists('logs'):
        os.mkdir('logs')
    log.setup(app, log_file='logs/error.log')

    app.register_blueprint(kid_edu_bp.bp, url_prefix='/kid/edu/')
    app.register_blueprint(kid_game_bp.bp, url_prefix='/kid/game/')

    @app.route('/healthz', methods=['GET'])
    def healthz():
        return f.jsonify(status='ok')

    return app
