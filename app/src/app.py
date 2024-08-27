from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .routes import router

app = FastAPI()

app.include_router(router, tags=["Event"])
@app.get("/", tags=["Root"])
async def read_root():
    return RedirectResponse(url="/docs")
