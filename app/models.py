from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    
    attendees = relationship("Attendee", back_populates="event")

class Attendee(Base):
    __tablename__ = "attendees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    qr_code = Column(String)  # Este campo almacenará el código QR generado
    present = Column(Boolean, default=False)  # Para verificar si el asistente está presente
    event_id = Column(Integer, ForeignKey("events.id"))

    event = relationship("Event", back_populates="attendees")
