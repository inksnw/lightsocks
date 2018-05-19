#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from sanic import Sanic

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

webserver = app.create_server(host="0.0.0.0", port=1081)

if __name__ == '__main__':
    app.run(port=1081)
