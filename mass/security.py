from flask_login import current_user
from flask_principal import RoleNeed, identity_loaded


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    identity.user = current_user

    if hasattr(current_user, "get_roles"):
        for role in current_user.get_roles():
            identity.provides.add(RoleNeed(role))
