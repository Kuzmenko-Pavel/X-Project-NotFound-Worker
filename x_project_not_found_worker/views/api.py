from aiohttp import web
import re
import ujson
import aiohttp_jinja2
from x_project_not_found_worker.logger import logger, exception_message

@aiohttp_jinja2.template('block.html')
class ApiView(web.View):
    async def get_data(self):
        host = '127.0.0.1'
        ip_regex = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        method = self.request.method
        headers = self.request.headers

        x_real_ip = headers.get('X-Real-IP', headers.get('X-Forwarded-For', ''))
        x_real_ip_check = ip_regex.match(x_real_ip)
        if x_real_ip_check:
            x_real_ip = x_real_ip_check.group()
        else:
            x_real_ip = None

        if x_real_ip is not None:
            host = x_real_ip
        else:
            try:
                peername = self.request.transport.get_extra_info('peername')
                if peername is not None and isinstance(peername, tuple):
                    host, _ = peername
            except Exception as ex:
                logger.error(exception_message(exc=str(ex), request=str(self.request._message)))

        analytics_id = self.request.app['config']['analytics']['default']
        status = self.request.headers.get('Status', 200)
        if status == '404':
            analytics_id = self.request.app['config']['analytics'][404]
        elif status == '500':
            analytics_id = self.request.app['config']['analytics'][500]
        data = {
            'analytics_id': analytics_id,
            'req_type': method,
            'ip': host
        }
        return data

    async def get(self):
        return await self.get_data()

    async def post(self):
        return await self.get_data()

    async def put(self):
        return await self.get_data()

    async def head(self):
        return await self.get_data()

    async def delete(self):
        return await self.get_data()

    async def patch(self):
        return await self.get_data()

    async def options(self):
        return await self.get_data()
