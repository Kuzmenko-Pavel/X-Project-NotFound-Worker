from aiohttp import web


class ApiView(web.View):
    async def get(self):
        return web.json_response(text="Hello, {}".format(self.request.match_info['tail']))

    async def post(self):
        return web.json_response({})
