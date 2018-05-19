import sys
import json
from collections import namedtuple
from ..module.password import loadsPassword

Config = namedtuple('Config', 'serverAddr serverPort localAddr localPort webPort password')


def loadjson(f):
    data = json.load(f)
    config = Config(**data)
    config = config._replace(password=loadsPassword(config.password))
    return config
