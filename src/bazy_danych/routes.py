from flask import Flask, flash, render_template, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from bazy_danych.db.helpers import get_lesson_instances_for_teacher_id

from .forms import LoginForm
from .db import get_db, get_lesson_instances_for_student_id
from .auth import BogusUser

def init_app(app: Flask):
    @app.route('/')
    @app.route('/index')
    def index():
        cursor = get_db().cursor()

        if current_user.is_authenticated:
            if current_user.is_student():
                lesson_instances = get_lesson_instances_for_student_id(current_user.student_id)
                return render_template('index.html', lesson_instances=lesson_instances)
            elif current_user.is_teacher():
                lesson_instances = get_lesson_instances_for_teacher_id(current_user.teacher_id)
                return render_template('index.html', lesson_instances=lesson_instances)

        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()

        if form.validate_on_submit():
            username = form.username.data
            cursor = get_db().cursor()
            user_record = cursor.execute('SELECT id, username, password_hash, student_id, teacher_id FROM user_account WHERE username = :username', username=username).fetchone()

            if user_record is None or not check_password_hash(user_record[2], form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))

            login_user(BogusUser(*user_record))
            return redirect(url_for('index'))

        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
