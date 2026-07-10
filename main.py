from fastapi import FastAPI
from lol_router import lol_router

api = FastAPI()

api.include_router(lol_router)
