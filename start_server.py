import os
import sys
import argparse
import asyncio
from core.server import server


def main():

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(server.listen())
    loop.run_forever()


if __name__ == '__main__':
    main()
