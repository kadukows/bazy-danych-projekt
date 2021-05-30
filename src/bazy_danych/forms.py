from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.core import BooleanField, DecimalField, FormField, FieldList
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired, NumberRange, Regexp
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class AddAGradeForm(FlaskForm):
    grade = DecimalField("Grade", validators=[DataRequired(), NumberRange(1, 6)])
    comment = StringField("Comment")
    submit = SubmitField("Add")


class AttendanceForm(FlaskForm):
    lesson_instance = HiddenField(
        "lesson_instance_id",
        validators=[DataRequired(), Regexp('^\d+$')])

    attendance = HiddenField(
        "attendance",
        validators=[Regexp('^\d*(,\d+)*$')],
        render_kw={'id': 'attendanceInput'})
