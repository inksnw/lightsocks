import argparse
import asyncio
import sys

sys.path.append("..")
from core.server import LsServer
from utils import config as lsConfig
from utils import net


def run_server(config: lsConfig.Config):
    loop = asyncio.get_event_loop()

    listenAddr = net.Address(config.serverAddr, config.serverPort)
    server = LsServer(loop=loop, password=config.password, listenAddr=listenAddr)

    asyncio.ensure_future(server.listen())
    loop.run_forever()


def main():

    with open('config_server.json', encoding='utf-8') as f:
        file_config = lsConfig.loadjson(f)

    run_server(file_config)


if __name__ == '__main__':
    main()
