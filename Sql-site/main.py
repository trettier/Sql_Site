from os import abort
import werkzeug
from flask_login import LoginManager, login_user, \
    login_required, logout_user, current_user
from flask import Flask, url_for, redirect, request, \
    send_from_directory, send_file
from flask import render_template
from data import db_session
from data.users import User
from loginform import LoginForm, Inputs, answer
from forms.user import RegisterForm
from data import db_session, api
from data.task import Task, TaskForm
import json_check
import os
from json_check import add_ctf
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(api.blueprint)
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

# Главная страница
@app.route("/", methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        index = request.form['index']
        if index == "1":
            return redirect("/offer")
        if index == "2":
            json_check.add_user(current_user.id)
            return redirect("/solving")
    return render_template("mainPage.html")

# Просмотр предложенных заданий
@app.route("/look_offers", methods=['GET', 'POST'])
def indexing():
    form = Inputs()
    db_sess = db_session.create_session()
    offers = db_sess.query(Task).all()
    if form.validate_on_submit():
        n = []
        for i in range(len(offers)):
            if form.files[i].data:
                n.append(offers[i].id)
        add_ctf(form.name.data, n, current_user.id)
        return redirect("/")
    if request.method == 'POST':
        index = request.form['index']
        filename = os.path.join(r"E:\[t-_-t]\Sql-site\files", index)
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                   index, as_attachment=True)
    if current_user.is_authenticated:
        return render_template("index.html", news=offers, form=form)
    return redirect("/")

# Страница для решения задач
@app.route("/solving", methods=['GET', 'POST'])
def index():
    with open('list_ctf.json') as cat_file:
        data = json.load(cat_file)
        for key, value in data.items():
            a = key
            break
        n = data[a]
        status = data["users"][str(current_user.id)]["tasks"]
        points = data["users"][str(current_user.id)]["points"]
    form = answer()
    db_sess = db_session.create_session()
    tasks = db_sess.query(Task).filter(Task.id.in_(n))
    if form.validate_on_submit():
        with open('list_ctf.json') as cat_file:
            data = json.load(cat_file)
            index = data["users"][str(current_user.id)]["now"]
        task = db_sess.query(Task).filter(Task.id == index).first()
        if form.answer.data == task.answer:
            with open('list_ctf.json') as cat_file:
                data = json.load(cat_file)
                data["users"][str(current_user.id)]["tasks"][str(task.id)] \
                    = True
                data["users"][str(current_user.id)]["points"] \
                    += int(task.difficult)
                points = data["users"][str(current_user.id)]["points"]
            with open('list_ctf.json', 'w') as cat_file:
                json.dump(data, cat_file, ensure_ascii=False)
        status1 = {}
        for i in status:
            status1[int(i)] = status[i]
        return render_template("solving.html", tasks=tasks,
                               form=form, status=status1, points=points)
    if request.method == 'POST':
        index = request.form['index']
        with open('list_ctf.json') as cat_file:
            data = json.load(cat_file)
            data["users"][str(current_user.id)]["now"] = index
        with open('list_ctf.json', 'w') as cat_file:
            json.dump(data, cat_file, ensure_ascii=False)
    status1 = {}
    for i in status:
        status1[int(i)] = status[i]
    return render_template("solving.html", tasks=tasks,
                           form=form, status=status1, points=points)

# Страница для скачивания файла
@app.route('/solving/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email ==
                                          form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

# Страница для предложения заданий
@app.route('/offer', methods=['GET', 'POST'])
@login_required
def offer():
    form = TaskForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        task = Task()
        task.title = form.title.data
        task.answer = form.answer.data
        task.content = form.content.data
        task.difficult = form.difficult.data
        if form.file.data:
            f = form.file.data
            filename = secure_filename(f.filename)
            file_path = os.path.join(r"E:\[t-_-t]\Sql-site\files", filename)
            task.file = filename
            f.save(file_path)
        db_sess.add(task)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Предложите задание',
                           form=form)


if __name__ == '__main__':
    main()
