from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from room_reservation.crud.base import CRUDBase
from room_reservation.models.reservation import Reservation
from room_reservation.schemas.reservation import ReservationCreate, ReservationUpdate


class CRUDReservation(CRUDBase[
    Reservation,
    ReservationCreate,
    ReservationUpdate,
]):
    async def get_reservations_at_the_same_time(
        self,
        session: AsyncSession,
        from_reserve: datetime,
        to_reserve: datetime,
        meetingroom_id: int,
    ) -> list[Reservation]:
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == meetingroom_id,
                and_(
                    from_reserve <= Reservation.to_reserve,
                    to_reserve >= Reservation.from_reserve,
                ),
            )
        )
        reservations = reservations.scalars().all()
        return reservations


reservation_crud = CRUDReservation(Reservation)
