import sys
sys.path.append("..")
from utils.xlog import getLogger
logger = getLogger('web')


from aiohttp import web


def index(request):
    return web.Response(body='{}'.format('sssss').encode(), content_type='text/html')


async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logger.info('server started at http://127.0.0.1:9000...')
    return srv
