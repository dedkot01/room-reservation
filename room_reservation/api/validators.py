from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from room_reservation.crud.meeting_room import meeting_room_crud
from room_reservation.models.meeting_room import MeetingRoom


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
