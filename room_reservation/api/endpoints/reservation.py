from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from room_reservation.api.validators import (
    check_meeting_room_exists,
    check_reservation_before_edit,
    check_reservation_intersections,
)
from room_reservation.core.db import get_async_session
from room_reservation.crud.reservation import reservation_crud
from room_reservation.schemas.reservation import ReservationCreate, ReservationDB, ReservationUpdate


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


@router.get(
    '/',
    response_model=list[ReservationDB],
)
async def get_all_reservations(
    session: AsyncSession = Depends(get_async_session),
):
    return await reservation_crud.get_multi(session)


@router.patch(
    '/{reservation_id}',
    response_model=ReservationDB,
)
async def update_reservation(
    reservation_id: int,
    obj_in: ReservationUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    reservation = await check_reservation_before_edit(session, reservation_id)
    await check_reservation_intersections(
        **obj_in.dict(),
        reservation_id=reservation_id,
        meetingroom_id=reservation.meetingroom_id,
        session=session,
    )
    reservation = await reservation_crud.update(session, reservation, obj_in)
    return reservation


@router.delete(
    '/{reservation_id}',
    response_model=ReservationDB,
)
async def delete_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    reservation = await check_reservation_before_edit(session, reservation_id)
    return await reservation_crud.remove(session, reservation)
