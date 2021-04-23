from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, SelectField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from data import db_session
db_session.global_init("db/ege_db.db")
db_sess = db_session.create_session()


class RegisterForm(FlaskForm):
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])

    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])

    about = TextAreaField("Немного о себе")

    submit = SubmitField('Регистрация')
