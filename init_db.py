#!.venv/bin/python
from flask import Flask

from app import create_app
from app.models import db
from app.models.user import User

GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
RESET = "\033[0m"
app: Flask = create_app()


def main() -> None:
    with app.app_context():
        db.create_all()

        if User.query.first():
            print(
                f"[{YELLOW}*{RESET}] {YELLOW}Database already exists. Skipping...{RESET}"
            )
            exit(0)

        db.add_roles(["Admin", "Patient", "Doctor"])
        print(f"[{GREEN}+{RESET}] {GREEN}Database created.{RESET}")
        db.add_admin()
        print(f"[{GREEN}+{RESET}] {GREEN}Admin account added.{RESET}")


if __name__ == "__main__":
    main()
