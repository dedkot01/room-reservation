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
        *,
        session: AsyncSession,
        from_reserve: datetime,
        to_reserve: datetime,
        meetingroom_id: int,
        reservation_id: int | None = None,
    ) -> list[Reservation]:
        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve,
            ),
        )
        if reservation_id is not None:
            select_stmt = select_stmt.where(
                Reservation.id != reservation_id
            )
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations


reservation_crud = CRUDReservation(Reservation)
