import argparse
import asyncio
import sys

sys.path.append("..")
from module.password import InvalidPasswordError, loadsPassword
from core.local import LsLocal
from utils import config as lsConfig
from utils import net
from utils.xlog import getLogger
logger = getLogger('local')


def run_server(config):
    loop = asyncio.get_event_loop()
    listenAddr = net.Address(config.localAddr, config.localPort)
    remoteAddr = net.Address(config.serverAddr, config.serverPort)
    server = LsLocal(
        loop=loop,
        password=config.password,
        listenAddr=listenAddr,
        remoteAddr=remoteAddr)

    asyncio.ensure_future(server.listen())
    loop.run_forever()


def main():

    config = lsConfig.Config(None, None, None, None, None)
    try:
        with open('config_local.json', encoding='utf-8') as f:
            file_config = lsConfig.load(f)
    except lsConfig.InvalidFileError:
        logger.debug(f'invalid config file')
        sys.exit(1)
    except FileNotFoundError:
        logger.debug(f'config file not found')
        sys.exit(1)
    config = config._replace(**file_config._asdict())

    run_server(config)


if __name__ == '__main__':
    main()
