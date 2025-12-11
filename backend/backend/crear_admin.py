"""
Script para crear/actualizar admin con contraseña hasheada
Ejecutar: python crear_admin.py
"""
import sys
sys.path.insert(0, '/root' if '/' in __file__ else '.')

from database.connection import SessionLocal, Base, engine
from database.models import Admin
from utils.password_utils import hash_password

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Verificar si existe admin
    admin = db.query(Admin).filter(Admin.email == "admin@bettsoft.com").first()
    
    if admin:
        print(f"✏️  Actualizando contraseña de {admin.email}...")
        admin.password_hash = hash_password("admin123")
        db.commit()
        print(f"✅ Admin actualizado correctamente")
    else:
        print("➕ Creando nuevo admin...")
        nuevo_admin = Admin(
            email="admin@bettsoft.com",
            password_hash=hash_password("admin123"),
            nombre="Administrador",
            es_activo=True
        )
        db.add(nuevo_admin)
        db.commit()
        print(f"✅ Admin creado correctamente")
    
    print("\n📋 Credenciales:")
    print(f"   Email: admin@bettsoft.com")
    print(f"   Contraseña: admin123")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
