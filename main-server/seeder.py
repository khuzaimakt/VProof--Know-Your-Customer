from sqlalchemy.orm import Session
from models import Role
from database import SessionLocal  # Import the SessionLocal

roles_to_seed = [
    {"name": "Super Admin"},
    {"name": "Admin"},
    {"name": "User"},
    {"name": "Manager"},
    # Add other roles as needed
]

def seed_data():
    db = SessionLocal()
    try:
        existing_roles = db.query(Role.name).all()
        existing_role_names = {name[0] for name in existing_roles}

        new_roles = [Role(name=role['name']) for role in roles_to_seed if role['name'] not in existing_role_names]

        if new_roles:
            db.add_all(new_roles)
            db.commit()
    finally:
        db.close()