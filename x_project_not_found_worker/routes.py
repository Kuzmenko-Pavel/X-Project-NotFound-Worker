from .views import ApiView


def setup_routes(app):
    app.router.add_route('*', '/{tail:.*}', ApiView)
