# -*- coding: utf-8 -*-
import time
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import uvicorn
from app.router import router

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(exc)
    return JSONResponse(str(exc), status_code=400)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.mount("/asset", StaticFiles(directory="asset"), name="asset")
app.mount("/cache", StaticFiles(directory="cache"), name="cache")


app.include_router(router, prefix='/api')


def main():
    uvicorn.run(app=app, host='0.0.0.0', port=8080, proxy_headers=True, forwarded_allow_ips='*')


if __name__ == '__main__':
    main()
