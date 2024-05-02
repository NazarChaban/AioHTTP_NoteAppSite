import asyncio
import sys

from aiohttp import web
import aiohttp_jinja2
import jinja2

from src.settings import config, BASE_DIR
from src.routes import set_up_routes
from src.db import pg_context

app = web.Application(debug=True)
loader = jinja2.FileSystemLoader(str(BASE_DIR / 'src' / 'templates'))
aiohttp_jinja2.setup(app, loader=loader)
set_up_routes(app)
app['config'] = config
app.cleanup_ctx.append(pg_context)

if __name__ == '__main__':
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )
    web.run_app(app, host='localhost', port=8080)
