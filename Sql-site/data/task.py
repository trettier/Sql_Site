import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FileField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm, SerializerMixin):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Задание")
    answer = StringField("Ответ")
    difficult = IntegerField("Сложность")
    submit = SubmitField('Применить')
    file = FileField("Файл (Не обязательно)")


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    answer = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    difficult = sqlalchemy.Column(sqlalchemy.String)
    is_solved = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    file = sqlalchemy.Column(sqlalchemy.String, nullable=True)





