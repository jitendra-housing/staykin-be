from fastapi import FastAPI

from app.core.logging import ErrorLoggingMiddleware, configure_logging
from app.routers import (
    flatmates,
    health,
    lifestyle_tags,
    listings,
    localities,
    occupations,
    profile,
    requests,
    rooms,
    teams,
    uploads,
)

configure_logging()

app = FastAPI(title="Staykin BE", version="0.1.0")
app.add_middleware(ErrorLoggingMiddleware)

app.include_router(health.router)
app.include_router(profile.router)
app.include_router(localities.router)
app.include_router(lifestyle_tags.router)
app.include_router(occupations.router)
app.include_router(listings.router)
app.include_router(uploads.router)
app.include_router(teams.router)
app.include_router(flatmates.router)
app.include_router(requests.router)
app.include_router(rooms.router)
