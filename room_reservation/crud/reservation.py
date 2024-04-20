from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from room_reservation.crud.base import CRUDBase
from room_reservation.models.reservation import Reservation


class CRUDReservation(CRUDBase):
    async def get_reservations_at_the_same_time(
        self,
        session: AsyncSession,
        from_reserve: datetime,
        to_reserve: datetime,
        meetingroom_id: int,
    ) -> list[Reservation]:
        ...
        return []


reservation_crud = CRUDReservation(Reservation)
