#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import logging
import logzero
from logzero import logger

current_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(current_path, os.pardir, 'data')
os.makedirs(log_path, exist_ok=True)


loggerDict = {}


def getLogger(name):
    if not name.endswith('.log'):
        name = name + '.log'

    global loggerDict

    if name in loggerDict:
        return loggerDict[name]
    else:
        logzero.logfile(os.path.join(log_path, name), maxBytes=1e6, backupCount=3)
        fmt = logging.Formatter('%(asctime)s%(levelname)8s [%(filename)s:%(lineno)d] %(message)s')
        logzero.formatter(fmt)
        loggerDict[name] = logger

        return loggerDict[name]
