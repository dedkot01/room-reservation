from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from room_reservation.crud.meeting_room import meeting_room_crud
from room_reservation.crud.reservation import reservation_crud
from room_reservation.models.meeting_room import MeetingRoom
from room_reservation.models.reservation import Reservation


async def check_name_duplicate(
    room_name: str,
    session: AsyncSession,
) -> None:
    room_id = await meeting_room_crud.get_room_id_by_name(session, room_name)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )


async def check_meeting_room_exists(
    meeting_room_id: int,
    session: AsyncSession,
) -> MeetingRoom:
    meeting_room = await meeting_room_crud.get(session, meeting_room_id)

    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорка не найдена!',
        )

    return meeting_room


async def check_reservation_intersections(**kwargs):
    reservations = await reservation_crud.get_reservations_at_the_same_time(**kwargs)
    if reservations:
        raise HTTPException(
            status_code=422,
            detail=str(reservations),
        )


async def check_reservation_before_edit(session: AsyncSession, reservation_id: int) -> Reservation:
    reservation = await reservation_crud.get(session, reservation_id)
    if reservation is None:
        raise HTTPException(
            status_code=404,
            detail='Бронь не найдена!',
        )
    return reservation
