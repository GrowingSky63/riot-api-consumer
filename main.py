import uvicorn
from fastapi import FastAPI
from lol_router import lol_router

api = FastAPI()

api.include_router(lol_router)


if __name__ == "__main__":
  uvicorn.run(api, host="0.0.0.0")