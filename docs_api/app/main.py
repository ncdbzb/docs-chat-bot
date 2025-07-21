from fastapi import FastAPI

from app.routers import include_routers


app = FastAPI(title="DOCS-API")

include_routers(app)

@app.get("/ping")
async def ping():
    return {"message": "pong"}
