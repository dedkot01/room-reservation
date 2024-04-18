from sqlalchemy import Column, String, Text

from room_reservation.core.db import Base, PreBase


class MeetingRoom(Base, PreBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
