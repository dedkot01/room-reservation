from fastapi import FastAPI

from room_reservation import __version__
from room_reservation.core.config import settings


app = FastAPI(
    title=settings.app_title,
    version=__version__,
)
