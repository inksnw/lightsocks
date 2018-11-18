import os
import asyncio
import json
from core.local import LsLocal
from collections import namedtuple
Config = namedtuple('Config', 'serverAddr serverPort localAddr localPort')


def main():

    current_path = os.path.dirname(os.path.abspath(__file__))
    file_config = os.path.join(current_path, 'data', 'config_local.json')
    with open(file_config, encoding='utf-8') as f:
        data = json.load(f)
        config = Config(**data)

    loop = asyncio.get_event_loop()
    listenAddr = (config.localAddr, config.localPort)
    remoteAddr = (config.serverAddr, config.serverPort)

    client = LsLocal(loop=loop, listenAddr=listenAddr, remoteAddr=remoteAddr)
    asyncio.ensure_future(client.listen())
    loop.run_forever()


if __name__ == '__main__':
    main()
