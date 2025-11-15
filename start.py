"""
Script de inicio para desarrollo local
Crea las tablas de la base de datos antes de iniciar el servidor
"""
from database import Base, engine

if __name__ == "__main__":
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas exitosamente")
    print("\nPara iniciar el servidor, ejecuta:")
    print("uvicorn main:app --reload")

