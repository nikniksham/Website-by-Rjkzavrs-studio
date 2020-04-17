import datetime
import flask
from flask import Flask, render_template, url_for, request
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from flask_restful import abort, Api
from werkzeug.utils import redirect
from data import db_session
from data.comments import Comments
from data.users import User
from data.publications import Publications
from data.developers_diary import DevelopersDiary
from data.products import Products
from data.forms import *
from data.UserApi.UserResource import CreateUserResource, UserResourceAdmin, UserListResourceAdmin, UserResource

app = Flask(__name__)
db_session.global_init("Followers_Rjkzavrs.sqlite")
app.config['SECRET_KEY'] = "secret_key_by_rjkzavr_1920"
blueprint = flask.Blueprint('UserApi', __name__, template_folder='templates')
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)
api.add_resource(CreateUserResource, '/api/user')
api.add_resource(UserResource, '/api/user/<string:email>/<string:password>')
api.add_resource(UserResourceAdmin, '/api/user/<string:email>/<string:password>/<int:user_id>')
api.add_resource(UserListResourceAdmin, '/api/users/<string:email>/<string:password>')


def get_image_profile(user):
    bg_img = 1
    if user.is_authenticated:
        bg_img = user.background_image_id + 1
    return url_for('static', filename=f'img/background_img_{bg_img}.png')


def main(port=8000):
    print("http://127.0.0.1:8000/about/")
    print('http://127.0.0.1:8000/DevelopersDiary')
    print('http://127.0.0.1:8000/DevelopersDiaryAdd')
    app.run(port=port)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают",
                                   style=url_for('static', filename='css/style.css'),
                                   bgimg=get_image_profile(current_user))
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form, message="Такой rjkzavrik уже существует",
                                   style=url_for('static', filename='css/style.css'),
                                   bgimg=get_image_profile(current_user))
        if session.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('register.html', title='Регистрация', form=form, message="Nickname уже занят",
                                   style=url_for('static', filename='css/style.css'),
                                   bgimg=get_image_profile(current_user))
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.nickname = form.nickname.data
        user.surname = form.surname.data
        user.set_password(form.password.data)
        user.age = form.age.data
        user.status = 0
        user.background_image_id = 0
        user.created_date = datetime.datetime.now()
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form,
                           style=url_for('static', filename='css/style.css'),
                           bgimg=get_image_profile(current_user))


# Получение последователя великих Rjkzavrs
@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form,
                               style=url_for('static', filename='css/style.css'),
                               bgimg=get_image_profile(current_user))
    return render_template('login.html', title='Авторизация', form=form,
                           style=url_for('static', filename='css/style.css'),
                           bgimg=get_image_profile(current_user))


# Выход с аккаунта
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect("/")


# Профиль аккаунта
@app.route('/account/')
def account():
    if current_user.is_authenticated:
        return render_template("account.html", title=f'Аккаунт {current_user.nickname}',
                               style=url_for('static', filename='css/style.css'), user=current_user,
                               bgimg=get_image_profile(current_user))
    return redirect('/')


# Подтверждение удаления аккаунта
@app.route('/delete_account/')
def delete_account():
    if current_user.is_authenticated:
        return render_template("delete_account.html", title=f'Аккаунт {current_user.nickname}',
                               style=url_for('static', filename='css/style.css'), user=current_user,
                               bgimg=get_image_profile(current_user))


@app.route('/DevelopersDiaryAdd/', methods=['GET', 'POST'])
@login_required
def add_developers_diary():
    if current_user.status >= 1:
        form = DevelopersDiaryForm()
        if form.submit.data:
            session = db_session.create_session()
            if session.query(DevelopersDiary).filter(DevelopersDiary.header == form.header.data).first():
                return render_template('DevelopersDiaryAdd.html', title='Создание записи', form=form,
                                       message="Запись с таким же названием уже существует",
                                       style=url_for('static', filename='css/style.css'),
                                       bgimg=get_image_profile(current_user))
            session.commit()
            session = db_session.create_session()
            ds_diary = DevelopersDiary()
            ds_diary.header = form.header.data
            ds_diary.body = form.body.data
            ds_diary.created_date = datetime.datetime.now()
            ds_diary.availability_status = form.availability_status.data[0]
            current_user.developers_diary.append(ds_diary)
            session.merge(current_user)
            session.commit()
            return redirect('/DevelopersDiary')
        return render_template('DevelopersDiaryAdd.html', title='Создание записи', form=form,
                               style=url_for('static', filename='css/style.css'),
                               bgimg=get_image_profile(current_user))
    else:
        return redirect('/DevelopersDiary')


@app.route('/developers_diary_change/<int:id>/', methods=['GET', 'POST'])
@login_required
def developers_diary_change(id):
    a_s = {0: 'Все пользователи', 1: 'Только зарегестрированные и выше', 2: 'Только разработчики'}
    if current_user.status >= 1:
        form = DevelopersDiaryForm()
        if request.method == "GET":
            session = db_session.create_session()
            ds_diary = session.query(DevelopersDiary).filter(DevelopersDiary.id == id).first()
            session.close()
            if ds_diary:
                form.header.data = ds_diary.header
                form.body.data = ds_diary.body
                form.availability_status.data = (ds_diary.availability_status, a_s[ds_diary.availability_status])
            else:
                abort(404)
        if form.submit.data:
            session = db_session.create_session()
            ds_diary = session.query(DevelopersDiary).filter(DevelopersDiary.id == id).first()
            if ds_diary:
                ds_diary.header = form.header.data
                ds_diary.body = form.body.data
                ds_diary.availability_status = form.availability_status.data[0]
                session.commit()
                return redirect('/DevelopersDiary')
            else:
                abort(404)
        return render_template('DevelopersDiaryAdd.html', title='Редактирование записи в дневнике разработчиков',
                               form=form, style=url_for('static', filename='css/style.css'),
                               bgimg=get_image_profile(current_user))
    else:
        abort(404)


@app.route('/developers_diary_delete/<int:id>/', methods=['GET', 'POST'])
@login_required
def developers_diary_delete(id):
    if current_user.status >= 1:
        session = db_session.create_session()
        ds_diary = session.query(DevelopersDiary).filter(DevelopersDiary.id == id).first()
        if ds_diary:
            session.delete(ds_diary)
            session.commit()
        else:
            abort(404)
        return redirect('/DevelopersDiary')
    else:
        abort(404)


@app.route("/test/")
def test():
    return render_template("base_2.html", title="xnjnj", style=url_for('static', filename='css/style.css'))


@app.route("/DevelopersDiary/")
def list_developers_diary():
    status = 0
    if current_user.is_authenticated:
        status = current_user.status + 1
    session = db_session.create_session()
    ds_diary = session.query(DevelopersDiary).all()
    session.close()
    return render_template("/DevelopersDiarys.html", ds_diary=ds_diary, status=status, user=current_user,
                           style=url_for('static', filename='css/style.css'),
                           bgimg=get_image_profile(current_user))


@app.route("/DevelopersDiaryPublication/<int:id>/")
def developers_diary(id):
    status = 0
    if current_user.is_authenticated:
        status = current_user.status + 1
    session = db_session.create_session()
    ds_diary = session.query(DevelopersDiary).filter(DevelopersDiary.id == id).first()
    session.close()
    ds_diary.created_date = ":".join(str(ds_diary.created_date).split(":")[:-1])
    if status >= ds_diary.availability_status:
        return render_template("/DevelopersDiary.html", publication=ds_diary, status=status, user=current_user,
                               style=url_for('static', filename='css/style.css'),
                               bgimg=get_image_profile(current_user))
    return redirect('/DevelopersDiary')


# Стартовая страница
@app.route("/")
def website_main():
    return render_template('main.html', title='Главная страница', style=url_for('static', filename='css/style.css'),
                           bgimg=get_image_profile(current_user))


# О нас
@app.route("/about/")
def about():
    return render_template("about.html", title="О RJKZAVRS STUDIO", style=url_for('static', filename='css/style.css'),
                           bgimg=get_image_profile(current_user))


if __name__ == '__main__':
    main()
    create_new_db = False
    if create_new_db:
        db_session.global_init("Followers_Rjkzavrs.sqlite")
        session = db_session.create_session()
        user = User()
        session.add(user)
        session.commit()
        session = db_session.create_session()
        publications = Publications()
        session.add(publications)
        session.commit()
        session = db_session.create_session()
        developers_diary = DevelopersDiary()
        session.add(developers_diary)
        session.commit()
        session = db_session.create_session()
        products = Products()
        session.add(products)
        session = db_session.create_session()
        comments = Comments()
        session.add(comments)
        session.commit()
        print('Успех!')
