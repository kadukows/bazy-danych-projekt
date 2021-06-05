from flask import Flask, flash, render_template, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from bazy_danych.db.helpers import get_first_lesson_instance_for_lesson_id, get_grades_for_student_for_lesson, get_lesson_id_for_lesson_instance_id, get_lesson_instances_for_teacher_id, get_student_for_student_id, get_students_for_class_id, get_students_for_lesson_id, get_students_with_attendance_for_lesson_instance_id

from .forms import AddAGradeForm, AttendanceForm, LoginForm
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

    @app.route('/lesson/<int:lesson_instance_id>', methods=['GET', 'POST'])
    @login_required
    def lesson(lesson_instance_id: int):
        lesson_id = get_lesson_id_for_lesson_instance_id(lesson_instance_id)
        students = [*get_students_for_lesson_id(lesson_id)]

        form = AttendanceForm()
        form.lesson_instance.data = str(lesson_instance_id)

        if form.validate_on_submit():
            flash("Updated attendance")
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM attendance WHERE lesson_instance_id = :lesson_instance_id
            """, lesson_instance_id=lesson_instance_id)

            attendance = [(student_id, lesson_instance_id) for student_id in form.attendance.data.split(',') if student_id]
            if len(attendance) > 0:
                cursor.executemany("INSERT INTO attendance VALUES (:1, :2)", attendance)

            conn.commit()

            return redirect(url_for('lesson', lesson_instance_id=lesson_instance_id))

        return render_template("lesson.html",
            form=form,
            students=students,
            lesson_id=lesson_id,
            lesson_instance_id=lesson_instance_id,
            lesson_instance=get_first_lesson_instance_for_lesson_id(lesson_id))

    @app.route('/lesson/<int:lesson_instance_id>/get')
    @login_required
    def lesson_get(lesson_instance_id: int):
        return {'rows': [{
            'id': student.id,
            'name': student.name,
            'state': True if student.lesson_instance_id is not None else False
        } for student in get_students_with_attendance_for_lesson_instance_id(lesson_instance_id)]}

    @app.route('/edit_student/<int:lesson_id>/<int:student_id>')
    @login_required
    def edit_student(student_id: int, lesson_id: int):
        return render_template('edit_student.html',
            grades=get_grades_for_student_for_lesson(student_id, lesson_id),
            student_id=student_id,
            lesson_id=lesson_id,
            student=get_student_for_student_id(student_id))

    @app.route('/add_grade/<int:lesson_id>/<int:student_id>', methods=['GET', 'POST'])
    def add_grade(lesson_id, student_id):
        form = AddAGradeForm()

        if form.validate_on_submit():
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO grades (student_id, lesson_id, grade, mycomment)
                VALUES (:student_id, :lesson_id, :grade, :mycomment)
            """, student_id=student_id, lesson_id=lesson_id, grade=form.grade.data, mycomment=form.comment.data)

            conn.commit()

            return redirect(url_for('edit_student', lesson_id=lesson_id, student_id=student_id))


        return render_template("add_grade.html", form=form, student=get_student_for_student_id(student_id))
