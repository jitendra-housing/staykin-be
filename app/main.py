from fastapi import FastAPI

from app.routers import health, lifestyle_tags, listings, localities, profile, uploads

app = FastAPI(title="Staykin BE", version="0.1.0")

app.include_router(health.router)
app.include_router(profile.router)
app.include_router(localities.router)
app.include_router(lifestyle_tags.router)
app.include_router(listings.router)
app.include_router(uploads.router)
