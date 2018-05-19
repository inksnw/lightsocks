import os
import asyncio
from aiohttp import web

from core.local import client
from core.utils.xlog import getLogger
from webui.web import webserver


def main():
    loop = asyncio.get_event_loop()
    # 代理
    asyncio.ensure_future(client.listen())
    # web
    asyncio.ensure_future(webserver)
    loop.run_forever()


if __name__ == '__main__':
    main()
