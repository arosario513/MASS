from flask import current_app
from flask_login import UserMixin
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy.orm import relationship
from . import db
from .role import Role, user_roles


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    roles = relationship("Role", secondary=user_roles, backref="users")

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def get_reset_token(self):
        serial: URLSafeTimedSerializer = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"]
        )
        return serial.dumps(self.email)

    @staticmethod
    def verify_reset_token(token, max_age=600):
        serial: URLSafeTimedSerializer = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"]
        )
        try:
            email = serial.loads(
                token,
                max_age=max_age
            )
        except SignatureExpired or BadSignature:
            return None
        return User.query.filter_by(email=email).first()

    def get_roles(self):
        return [r.name for r in self.roles]

    def has_role(self, name):
        return name in self.get_roles()

    def add_role(self, role_name: str) -> bool:
        role = Role.query.filter_by(name=role_name).first()
        if role and role not in self.roles:
            self.roles.append(role)
            return True
        return False

    def to_dict(self):
        return {
            "id": self.id,
            "first name": self.first_name,
            "last name": self.last_name,
            "email": self.email,
            "roles": [i.name for i in self.roles]
        }

    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"User({self.id}, {self.first_name}, {self.last_name}, {self.email}, {self.get_roles()})"
