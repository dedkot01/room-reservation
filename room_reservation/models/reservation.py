from sqlalchemy import Column, DateTime, ForeignKey, Integer

from room_reservation.core.db import Base, PreBase


class Reservation(Base, PreBase):
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)

    meetingroom_id = Column(Integer, ForeignKey('meetingroom.id'))
