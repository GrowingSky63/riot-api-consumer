import types
import typing
if not hasattr(typing, 'GenericAlias'):
    typing.GenericAlias = types.GenericAlias  # type: ignore[attr-defined]

import uvicorn
from fastapi import FastAPI
from lol_router_v1 import lol_router as lol_router_v1
from lol_router_v2 import lol_router as lol_router_v2

api = FastAPI()

api.include_router(lol_router_v1)
api.include_router(lol_router_v2)


if __name__ == "__main__":
  uvicorn.run(api, host="0.0.0.0")