import json

from data import db_session
from data.task import Task, TaskForm
from data.users import User


def add_ctf(ctf_name, a, user):
    b = {ctf_name: a, "users": {user: {"now" : None, "points": 0, "tasks": {}}}}
    for i in a:
        b["users"][user]["tasks"][i] = False
    with open('list_ctf.json', 'w') as cat_file:
        json.dump(b, cat_file, ensure_ascii=False)

def add_user(user):
    with open('list_ctf.json') as cat_file:
        data = json.load(cat_file)
        if user not in data["users"]:
            data["users"][str(user)] = {"now" : None, "points": 0, "tasks": {}}
    with open('list_ctf.json', 'w') as cat_file:
        json.dump(data, cat_file, ensure_ascii=False)
