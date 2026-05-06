from fastapi import FastAPI

from app.routers import health, localities, profile

app = FastAPI(title="Staykin BE", version="0.1.0")

app.include_router(health.router)
app.include_router(profile.router)
app.include_router(localities.router)
