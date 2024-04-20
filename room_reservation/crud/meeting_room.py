from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from room_reservation.crud.base import CRUDBase
from room_reservation.models.meeting_room import MeetingRoom
from room_reservation.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


class CRUDMeetingRoom(CRUDBase[
    MeetingRoom,
    MeetingRoomCreate,
    MeetingRoomUpdate,
]):
    async def get_room_id_by_name(self, session: AsyncSession, room_name: str) -> int | None:
        db_room_id = await session.execute(
            select(MeetingRoom.id).where(
                MeetingRoom.name == room_name
            )
        )
        db_room_id = db_room_id.scalars().first()

        return db_room_id


meeting_room_crud = CRUDMeetingRoom(MeetingRoom)
