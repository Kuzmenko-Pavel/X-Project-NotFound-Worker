from .views import ApiView
from aiohttp import web


async def handler_404(request):
    raise web.HTTPNotFound()


def setup_routes(app):
    app.router.add_route('*', '/example.cache', handler_404)
    app.router.add_route('*', '/{tail:.*}', ApiView)
