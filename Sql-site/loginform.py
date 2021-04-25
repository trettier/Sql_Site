from flask_wtf import FlaskForm
from wtforms import  PasswordField, SelectField, StringField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Required
from wtforms.fields.html5 import EmailField
from data import db_session
from data.users import User
from wtforms.fields import FieldList
from forms.user import RegisterForm
from data import db_session, api
from data.task import Task, TaskForm
import json_check
import os

class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

# Форма для создания турнира
class Inputs(FlaskForm):
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    offers = db_sess.query(Task).all()
    n = len(offers)
    files = FieldList(BooleanField(), min_entries=n)
    submit = SubmitField('Создать')
    name = StringField('Название турнира')

# Форма для решения задач
class answer(FlaskForm):
    answer = StringField('Нажмите дать ответ и впишите ответ')
    submit = SubmitField('Проверить')