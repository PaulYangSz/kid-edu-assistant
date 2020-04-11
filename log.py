#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 HomeWork Inc. All Rights Reserved.
# Author: shookuooo@gmail.com

import logging
from logging import handlers

# Logging aliases. Feel free to add more.
error = logging.error
info = logging.info
warn = logging.warning
exception = logging.exception


def setup(app, log_file=False):
    global error
    global info
    global warn
    global exception

    app.logger.setLevel(logging.INFO)

    info = app.logger.info
    warn = app.logger.warn
    exception = app.logger.exception
    error = app.logger.error

    if log_file:
        if not app.debug:
            file_handler = handlers.RotatingFileHandler(
                log_file,
                maxBytes=1024 * 1024 * 100,
                backupCount=3)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s"))
            app.logger.addHandler(file_handler)
        else:
            logging.basicConfig(
                level=logging.DEBUG,  # 定义输出到文件的log级别，
                format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s:  %(message)s',  # 定义输出log的格式
                datefmt='%Y-%m-%d %A %H:%M:%S')  # 时间
                # filename=logFilename,  # log文件名
                # filemode='w')  # 写入模式“w”或“a”
