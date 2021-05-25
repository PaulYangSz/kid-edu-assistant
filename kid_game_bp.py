#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 HomeWork Inc. All Rights Reserved.
# Author: shookuooo@gmail.com
import json
import random

import flask as f
from flask import render_template, request

import log

bp = f.Blueprint('kid_game_v1', __name__)


@bp.route('/', methods=['GET'])
def main_page():
    return render_template('kid_game.html')
