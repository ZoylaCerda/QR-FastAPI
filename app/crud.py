from sqlalchemy.orm import Session
from . import models, schemas
import qrcode
from io import BytesIO
import base64

# Crear un evento
def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

# Obtener todos los eventos
def get_events(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Event).offset(skip).limit(limit).all()

# Obtener un evento por ID
def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

# Eliminar un evento
def delete_event(db: Session, event_id: int):
    event = get_event(db, event_id=event_id)
    if event:
        db.delete(event)
        db.commit()
        return True
    return False

# Crear un asistente con código QR
def create_attendee(db: Session, attendee: schemas.AttendeeCreate, event_id: int):
    # Crear el asistente en la base de datos para obtener su ID
    db_attendee = models.Attendee(**attendee.dict(), event_id=event_id)
    db.add(db_attendee)
    db.commit()
    db.refresh(db_attendee)

    # Generar el QR con el ID del asistente
    qr_code = generate_qr_code(db_attendee.id)
    db_attendee.qr_code = qr_code

    # Guardar el QR en la base de datos
    db.commit()
    db.refresh(db_attendee)

    return db_attendee


# Obtener asistentes de un evento
def get_attendees_by_event(db: Session, event_id: int):
    return db.query(models.Attendee).filter(models.Attendee.event_id == event_id).all()

# Marcar un asistente como presente
def mark_attendee_present(db: Session, attendee_id: int):
    attendee = db.query(models.Attendee).filter(models.Attendee.id == attendee_id).first()
    if attendee:
        attendee.present = True
        db.commit()
        return attendee
    return None

# Generar código QR
def generate_qr_code(attendee_id: int) -> str:
    url = f"http://localhost:8000/attendees/mark/{attendee_id}/"
    
    qr = qrcode.make(url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    
    qr_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return qr_base64

