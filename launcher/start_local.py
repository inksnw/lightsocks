import argparse
import asyncio
import sys

sys.path.append("..")
from core.local import LsLocal
from utils import config as lsConfig
from utils import net
from utils.xlog import getLogger
logger = getLogger('local')
import threading


with open('config_local.json', encoding='utf-8') as f:
    config = lsConfig.loadjson(f)

loop = asyncio.get_event_loop()
listenAddr = net.Address(config.localAddr, config.localPort)
remoteAddr = net.Address(config.serverAddr, config.serverPort)
server = LsLocal(loop=loop, password=config.password, listenAddr=listenAddr, remoteAddr=remoteAddr)


from web import init


def main():
    loop.run_until_complete(init(loop))
    asyncio.ensure_future(server.listen())
    loop.run_forever()


if __name__ == '__main__':
    main()
    print(2222)
