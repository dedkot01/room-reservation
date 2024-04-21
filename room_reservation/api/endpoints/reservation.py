from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from room_reservation.api.validators import check_meeting_room_exists, check_reservation_intersections
from room_reservation.core.db import get_async_session
from room_reservation.crud.reservation import reservation_crud
from room_reservation.schemas.reservation import ReservationCreate, ReservationDB


router = APIRouter()


@router.post(
    '/',
    response_model=ReservationDB,
)
async def create_reservation(
    reservation: ReservationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_meeting_room_exists(reservation.meetingroom_id, session)
    await check_reservation_intersections(**reservation.dict(), session=session)
    return await reservation_crud.create(session, reservation)
