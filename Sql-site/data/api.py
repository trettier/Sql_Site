import flask
from flask import jsonify, request
import json
from . import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, url_for, redirect, request, send_from_directory, send_file
from flask import render_template
import sys
from flask_wtf import FlaskForm
from wtforms import  PasswordField, SelectField, StringField
from wtforms import BooleanField, SubmitField
from wtforms.fields import FieldList
from wtforms.validators import DataRequired, Required
sys.path.insert(0, "E:\[t-_-t]\Sql-site")
from .task import Task, TaskForm




blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder='templates'
)