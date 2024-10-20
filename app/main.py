from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear un evento
@app.post("/events/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)

# Obtener todos los eventos
@app.get("/events/", response_model=List[schemas.Event])
def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_events(db, skip=skip, limit=limit)

# Obtener un evento por ID
@app.get("/events/{event_id}", response_model=schemas.Event)
def read_event(event_id: int, db: Session = Depends(get_db)):
    event = crud.get_event(db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# Eliminar un evento
@app.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_event(db, event_id=event_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted successfully"}

# Agregar un asistente a un evento
@app.post("/events/{event_id}/attendees/", response_model=schemas.Attendee)
def create_attendee(event_id: int, attendee: schemas.AttendeeCreate, db: Session = Depends(get_db)):
    return crud.create_attendee(db=db, attendee=attendee, event_id=event_id)

# Obtener asistentes de un evento
@app.get("/events/{event_id}/attendees/", response_model=List[schemas.Attendee])
def get_attendees(event_id: int, db: Session = Depends(get_db)):
    return crud.get_attendees_by_event(db, event_id=event_id)

# Endpoint que marca al asistente como presente basado en su QR
@app.get("/attendees/mark/{attendee_id}/")
def mark_attendee_present_qr(attendee_id: int, db: Session = Depends(get_db)):
    attendee = crud.mark_attendee_present(db=db, attendee_id=attendee_id)
    if attendee is None:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return {"message": f"Attendee {attendee.name} marked as present"}

# Obtener un asistente por id
@app.get("/attendees/{attendee_id}", response_model=schemas.Attendee)
def get_attendee(attendee_id: int, db: Session = Depends(get_db)):
    attendee = db.query(models.Attendee).filter(models.Attendee.id == attendee_id).first()
    if attendee is None:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return attendee