import os
import sys
import json
import argparse
import asyncio
from collections import namedtuple
from core.server import LsServer
Config = namedtuple('Config', 'serverAddr serverPort localAddr localPort')


def main():

    loop = asyncio.get_event_loop()

    current_path = os.path.dirname(os.path.abspath(__file__))
    file_config = os.path.join(current_path, 'data', 'config_server.json')
    with open(file_config, encoding='utf-8') as f:
        data = json.load(f)
        config = Config(**data)

    listenAddr = (config.serverAddr, config.serverPort)

    server = LsServer(loop=loop, listenAddr=listenAddr)

    asyncio.ensure_future(server.listen())
    loop.run_forever()


if __name__ == '__main__':
    main()
