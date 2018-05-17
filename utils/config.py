import json
import sys
from collections import namedtuple
sys.path.append("..")
from module.password import InvalidPasswordError, dumpsPassword, loadsPassword

Config = namedtuple('Config', 'serverAddr serverPort localAddr localPort webPort password')


def loadjson(f):
    data = json.load(f)
    config = Config(**data)
    config = config._replace(password=loadsPassword(config.password))
    return config
