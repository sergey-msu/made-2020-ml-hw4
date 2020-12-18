from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class DemoUser(UserMixin):
    def __init__(self, uid, name, password):
        self.id = uid
        self.name = name
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
