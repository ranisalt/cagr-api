from aiohttp import web
import hub
import json
from lru import lru_async


@lru_async()
async def get_result(**kwargs) -> tuple:
    items = await hub.get_items(**kwargs)
    return tuple(items)


async def handler(request: web.Request) -> web.Response:
    query = request.GET
    result = await get_result(campus=query.get('campus'),
            subject=query.get('subject'), name=query.get('name'))
    return web.json_response(result)


def create_app():
    app = web.Application()
    app.router.add_route('GET', '/', handler)
    return app


run_app = web.run_app
