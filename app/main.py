from fastapi import FastAPI
from app.routers import stable, result, stage
from app.database.connection import create_database_if_not_exists, engine, Base

app = FastAPI()

app.include_router(stable.router, prefix="/stables", tags=["Stable"])
app.include_router(result.router, prefix="/results", tags=["Result"])
app.include_router(stage.router, prefix="/stages", tags=["Stage"])


@app.on_event("startup")
async def on_startup():
    await create_database_if_not_exists()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)