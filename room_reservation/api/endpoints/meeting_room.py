from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from room_reservation.api.validators import check_meeting_room_exists, check_name_duplicate
from room_reservation.core.db import get_async_session
from room_reservation.crud.meeting_room import meeting_room_crud
from room_reservation.crud.reservation import reservation_crud
from room_reservation.schemas.meeting_room import (
    MeetingRoomCreate,
    MeetingRoomDB,
    MeetingRoomUpdate,
)
from room_reservation.schemas.reservation import ReservationDB


router = APIRouter()


@router.post(
    '/',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def create_new_meeting_room(
    meeting_room: MeetingRoomCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(meeting_room.name, session)
    new_room = await meeting_room_crud.create(session, meeting_room)
    return new_room


@router.get(
    '/',
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True,
)
async def get_all_meeting_rooms(session: AsyncSession = Depends(get_async_session)):
    rooms = await meeting_room_crud.get_multi(session)

    return rooms


@router.patch(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def partially_update_meeting_room(
    meeting_room_id: int,
    obj_in: MeetingRoomUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    meeting_room = await check_meeting_room_exists(meeting_room_id, session)

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    meeting_room = await meeting_room_crud.update(session, meeting_room, obj_in)

    return meeting_room


@router.delete(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def remove_meeting_room(
    meeting_room_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    meeting_room = await check_meeting_room_exists(meeting_room_id, session)
    meeting_room = await meeting_room_crud.remove(session, meeting_room)

    return meeting_room


@router.get(
    '/{meeting_room_id}/reservations',
    response_model=list[ReservationDB],
)
async def get_reservations_for_room(
    meeting_room_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    await check_meeting_room_exists(meeting_room_id, session)
    return await reservation_crud.get_future_reservations_for_room(session, meeting_room_id)
