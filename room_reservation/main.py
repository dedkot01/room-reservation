from fastapi import FastAPI

from room_reservation import __version__
from room_reservation.api.routers import main_router
from room_reservation.core.config import settings


app = FastAPI(
    title=settings.app_title,
    version=__version__,
)

app.include_router(main_router)
