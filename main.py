import asyncio
import logging

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.responses import HTMLResponse
from uvicorn import Config, Server

from qa_api import v1_check_credit

api_router = APIRouter()

app = FastAPI(docs_url='/swagger', openapi_url='/swagger.json')

PROCESSES = {}


@app.exception_handler(Exception)
async def validation_exception_handler(request, exc):
    print(str(exc))
    return JSONResponse({'error': str(exc), 'data': None}, status_code=500)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title='CreditCalc API',
        version='1.0.0',
        description='CreditCalc API',
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.get('/', include_in_schema=False, response_class=HTMLResponse)
async def dummy(request: Request):
    return (
        f'<center>'
        f'<h1>CreditCalc handlers is working!</h1>'
        f'<h5>Please call appropriate handler or visit <a href="{request.base_url}swagger">Swagger</a></h5>'
        f'</center>'
    )


def setup_routes():
    app.include_router(v1_check_credit.router, prefix='/v1', tags=['Credit'])


class MyServer(Server):

    async def run(self, sockets=None):
        self.config.setup_event_loop()
        return await self.serve(sockets=sockets)


async def run():
    apps = []
    logging.basicConfig(level=logging.INFO)
    setup_routes()
    for port in [80, 84]:
        app.openapi = custom_openapi
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
        config = Config(app, host='0.0.0.0', port=port)
        server = MyServer(config=config)
        apps.append(server.run())
    return await asyncio.gather(*apps)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
