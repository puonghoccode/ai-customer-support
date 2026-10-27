from getpass import getpass
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User
from app.models.enums import UserRole, UserStatus
from app.repositories.user_repository import create_user, get_user_by_email

def main():
    print("Create Admin User")
    email = input("Admin email: ").strip().lower()
    full_name = input("Full Name: ").strip()
    password = getpass("Password: ")
    print("[1] Password accespted", flush=True)

    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return

    db = SessionLocal()
    print("[2] Database session created", flush=True)

    try:
        print("[3] Checking if user already exists", flush=True)
        if get_user_by_email(db, email):
            print(f"User with email {email} already exists.")
            return

        admin = User(
            email=email,
            password_hash=hash_password(password),
            full_name=full_name,
            phone = None,
            company = None,
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )

        create_user(db, admin)
        print(f"Admin user {email} created successfully.")

    finally:
        db.close()
        
        
if __name__ == "__main__":
            main()
