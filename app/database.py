from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Usa la URL de tu base de datos
DATABASE_URL = "postgresql://postgres:p%40ssw0rd%21@localhost:5432/qr"


# Configuración del motor y la sesión
try:
    # Crear el motor y la sesión
    engine = create_engine(DATABASE_URL)
    # Intenta conectarte para verificar que la conexión es exitosa
    with engine.connect() as connection:
        print("Conexión exitosa a la base de datos.")
except Exception as e:
    print(f"Ocurrió un error al conectar a la base de datos: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
