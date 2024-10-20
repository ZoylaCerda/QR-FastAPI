from pydantic import BaseModel
from typing import List

class AttendeeBase(BaseModel):
    name: str
    email: str

class AttendeeCreate(AttendeeBase):
    pass

class Attendee(AttendeeBase):
    id: int
    qr_code: str
    present: bool

    class Config:
        orm_mode = True

class EventBase(BaseModel):
    name: str
    description: str

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    attendees: List[Attendee] = []

    class Config:
        orm_mode = True
