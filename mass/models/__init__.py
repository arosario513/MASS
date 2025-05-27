import logging
from os import getenv

from argon2 import PasswordHasher
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

ph: PasswordHasher = PasswordHasher()


class Database(SQLAlchemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_roles(self, roles: list[str]):
        from mass.models.role import Role

        for i in roles:
            if not self.session.execute(self.select(Role).filter_by(name=i)).first():
                self.session.add(Role(name=i))
        self.session.commit()

    def add_admin(self):
        from mass.models.user import User

        first_name: str = getenv("ADMIN_FIRSTNAME") or "Default"
        last_name: str = getenv("ADMIN_LASTNAME") or "Admin"
        email: str = getenv("ADMIN_EMAIL") or "admin@example.com"
        password: str = getenv("ADMIN_PASSWORD") or "changeme123"

        if (
            first_name == "Default"
            or last_name == "Admin"
            or email == "admin@example.com"
            or password == "changeme123"
        ):
            logging.warning(
                "[!] Admin credentials have default values. Please set all of them in the .env file."
            )

        admin = User.query.filter_by(email=email).first()
        if not admin:
            hash = ph.hash(password)
            admin = User(first_name, last_name, email, hash)

            self.session.add(admin)
            self.session.commit()

            admin.add_role("Admin")
            self.session.commit()


db: Database = Database()
