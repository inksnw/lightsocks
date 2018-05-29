#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import socket
from sanic import Sanic
from core.utils.config import loadjson
app = Sanic(__name__)
from sanic.response import html
from jinja2 import Environment, FileSystemLoader
base_dir = os.path.abspath(os.path.dirname(__file__))
app.static('/static', os.path.join(base_dir, 'static'))
app.static('/', os.path.join(base_dir, 'static'))

templates_dir = os.path.join(base_dir, 'templates')
jinja_env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)


def render_template(template_name: str, **context) -> str:
    template = jinja_env.get_template(template_name)
    return html(template.render(**context))


@app.route('/')
async def index(request):
    return render_template('index.html')


file_config = os.path.join(base_dir, os.pardir, 'data', 'config_local.json')
with open(file_config, encoding='utf-8') as f:
    config = loadjson(f)

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
listener.bind(('0.0.0.0', config.webPort))
listener.listen(6)

webserver = app.create_server(sock=listener)
if __name__ == '__main__':
    app.run(sock=listener)
