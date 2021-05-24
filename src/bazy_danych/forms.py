from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.core import DateTimeField, DecimalField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class AddAGradeForm(FlaskForm):
    grade = DecimalField("Grade", validators=[DataRequired(), NumberRange(1, 6)])
    comment = StringField("Comment")
    submit = SubmitField("Add")
