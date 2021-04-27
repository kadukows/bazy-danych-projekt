from dataclasses import dataclass
from typing import Optional

from flask import Flask
from flask_login import login_user, UserMixin, LoginManager

from .db import get_db

login_manager = LoginManager()

@dataclass(frozen=True)
class BogusUser(UserMixin):
    id: int
    username: str
    password_hash: str
    student_id: Optional[int] = None
    teacher_id: Optional[int] = None

    def is_student(self):
        return self.student_id is not None

    def is_teacher(self):
        return self.teacher_id is not None

def init_app(app: Flask):
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id: int):
        db = get_db()
        cursor = db.cursor()
        user = cursor.execute('SELECT id, username, password_hash, student_id, teacher_id FROM user_account WHERE id = :id', id=id).fetchone()

        if user:
            return BogusUser(*user)

        return None

    # endpoint to 'Login' page, same value that is passed to 'url_for' function
    login_manager.login_view = 'login'
