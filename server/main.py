# -*- coding: utf-8 -*-

from fastapi import FastAPI
import uvicorn
from app.router import router

app = FastAPI()

app.include_router(router)


def main():
    uvicorn.run(app=app, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
