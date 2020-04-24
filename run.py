import datetime
import os

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
from data.DevelopersDiaryApi.DevelopersDiaryResource import DevelopersDiaryResourceUser, \
    DevelopersDiaryListResourceAdmin, DevelopersDiaryResourceAdmin, CreateDevelopersDiaryResource
from data.PublicationsApi.PublicationsResource import PublicationsResourceUser, PublicationsListResourceAdmin, \
    PublicationsResourceAdmin, CreatePublicationsResource

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key_by_rjkzavr_1920"
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/Followers_Rjkzavrs.sqlite")
api = Api(app)
api.add_resource(CreateUserResource, '/api/user')
api.add_resource(UserResource, '/api/user/<string:email>/<string:password>')
api.add_resource(UserResourceAdmin, '/api/user/<string:email>/<string:password>/<int:user_id>')
api.add_resource(UserListResourceAdmin, '/api/users/<string:email>/<string:password>')
api.add_resource(DevelopersDiaryResourceUser,
                 '/api/developers_diary/<string:email>/<string:password>/<int:publication_id>')
api.add_resource(DevelopersDiaryResourceAdmin,
                 '/api/developers_diary_admin/<string:email>/<string:password>/<int:publication_id>')
api.add_resource(DevelopersDiaryListResourceAdmin, '/api/developers_diary_admin_list/<string:email>/<string:password>')
api.add_resource(CreateDevelopersDiaryResource, '/api/developers_diary_admin_create/<string:email>/<string:password>')
api.add_resource(PublicationsResourceUser, '/api/publication/<string:email>/<string:password>/<int:publication_id>')
api.add_resource(PublicationsResourceAdmin,
                 '/api/publication_admin/<string:email>/<string:password>/<int:publication_id>')
api.add_resource(PublicationsListResourceAdmin, '/api/publication_admin_list/<string:email>/<string:password>')
api.add_resource(CreatePublicationsResource, '/api/publication_create/<string:email>/<string:password>')


def check_password(password):
    errors = {0: 'Ok', 1: 'The password length must be 8 or more', 2: 'The password must contain at least 1 letter',
              3: 'The password must contain at least 1 digit'}
    if not len(password) >= 8:
        return False, errors[1]
    if password.isdigit():
        return False, errors[2]
    if password.isalpha():
        return False, errors[3]
    return True, errors[0]


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
        res = check_password(form.password.data)
        if not res[0]:
            return render_template('register.html', title='Регистрация', form=form, message=res[1],
                                   style=url_for('static', filename='css/style.css'),
                                   bgimg=url_for('static', filename='img/background_img_1.png'))
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


@app.route('/delete_account/', methods=['GET', 'POST'])
@login_required
def delete_account():
    form = DeleteForm()
    if form.submit.data:
        if current_user.check_password(form.password.data):
            session = db_session.create_session()
            user = session.query(User).get(current_user.id)
            logout_user()
            session.delete(user)
            session.commit()
            return redirect('/')
        return render_template("Delete_User.html", title=f'Аккаунт {current_user.nickname}', message='Пароль неверный',
                               style=url_for('static', filename='css/style.css'), user=current_user, form=form,
                               bgimg=url_for('static', filename='img/background_img_1.png'))
    return render_template("Delete_User.html", title=f'Аккаунт {current_user.nickname}', form=form,
                           style=url_for('static', filename='css/style.css'), user=current_user,
                           bgimg=url_for('static', filename='img/background_img_1.png'))


@app.route('/edit_account/', methods=['GET', 'POST'])
@login_required
def edit_account():
    form = EditAccountForm()
    if request.method == "GET":
        form.email.data = current_user.email
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.nickname.data = current_user.nickname
        form.age.data = current_user.age
    if form.submit.data:
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first() and current_user.email != form.email.data:
            return render_template("Edit_Account.html", form=form, style=url_for('static', filename='css/style.css'),
                                   bgimg=url_for('static', filename='img/background_img_1.png'),
                                   message='Этот email уже занят')
        if session.query(User).filter(User.nickname == form.nickname.data).first() and \
                current_user.nickname != form.nickname.data:
            return render_template("Edit_Account.html", form=form, style=url_for('static', filename='css/style.css'),
                                   bgimg=url_for('static', filename='img/background_img_1.png'),
                                   message='Этот nickname уже занят')
        user = session.query(User).filter(User.email == current_user.email).first()
        user.email = form.email.data
        user.name = form.name.data
        user.surname = form.surname.data
        user.nickname = form.nickname.data
        user.age = form.age.data
        user.background_image_id = form.background_image_id.data[0]
        session.commit()
        return redirect('/account/')
    return render_template("Edit_Account.html", form=form, style=url_for('static', filename='css/style.css'),
                           bgimg=url_for('static', filename='img/background_img_1.png'))


@app.route("/delete_comment/<int:id>/<type>/<id_public>/")
def delete_comment(id, type, id_public):
    session = db_session.create_session()
    comment = session.query(Comments).get(id)
    if current_user.is_authenticated and (comment.author_id == current_user.id or current_user.status >= 2):
        session.delete(comment)
        session.commit()
        return redirect(f"/{type}/{id_public}/")
    else:
        session.close()
        return redirect(f"/{type}/{id_public}/")


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
def developers_diary_edit(id):
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


@app.route("/DevelopersDiaryPublication/<int:public_id>/<int:comment_id>/", methods=['GET', 'POST'])
def change_comment_developers_diary(public_id, comment_id):
    form = CommentsForm()
    if form.submit.data:
        session = db_session.create_session()
        comment = session.query(Comments).get(comment_id)
        if current_user.is_authenticated and (comment.author_id == current_user.id or current_user.status >= 2):
            comment.text = form.text.data
            form.text.data = ""
            session.commit()
            return redirect(f"/DevelopersDiaryPublication/{public_id}/")
        else:
            session.close()
            return redirect(f"/DevelopersDiaryPublication/{public_id}/")
    else:
        session = db_session.create_session()
        comment = session.query(Comments).get(comment_id)
        session.close()
        if current_user.is_authenticated and (comment.author_id == current_user.id or current_user.status >= 2):
            session = db_session.create_session()
            comments = session.query(Comments).filter(Comments.developers_diary_publication_id == public_id).order_by(Comments.created_date.desc()).all()
            form.text.data = comment.text
            ds_diary = session.query(DevelopersDiary).filter(DevelopersDiary.id == public_id).first()
            status = current_user.status + 1
            templ = render_template("/DevelopersDiary.html", publication=ds_diary, status=status, user=current_user,
                                    style=url_for('static', filename='css/style.css'), form=form, comments=comments,
                                    count_commentaries=len(comments), base_href=f"DevelopersDiaryPublication/{public_id}/",
                                    bgimg=get_image_profile(current_user))
            session.close()
            return templ
        abort(400, message="Отказао в доступе")


@app.route("/DevelopersDiaryPublication/<int:id>/", methods=['GET', 'POST'])
def developers_diary(id):
    status = 0
    if current_user.is_authenticated:
        status = current_user.status + 1
    session = db_session.create_session()
    ds_diary = session.query(DevelopersDiary).filter(DevelopersDiary.id == id).first()
    session.close()
    ds_diary.created_date = ":".join(str(ds_diary.created_date).split(":")[:-1])
    if status >= ds_diary.availability_status:
        form = CommentsForm()
        if form.submit.data:
            if current_user.is_authenticated:
                session = db_session.create_session()
                user = session.query(User).get(current_user.id)
                diary = session.query(DevelopersDiary).get(id)
                comment = Comments()
                comment.text = form.text.data
                comment.created_date = datetime.datetime.now()
                form.text.data = ""
                user.comments.append(comment)
                session.merge(user)
                diary.comments.append(comment)
                session.merge(diary)
                session.commit()
                session = db_session.create_session()
                comments = session.query(Comments).filter(Comments.developers_diary_publication_id == id).order_by(
                    Comments.created_date.desc()).all()
                templ = render_template("/DevelopersDiary.html", publication=ds_diary, status=status, user=current_user,
                                        style=url_for('static', filename='css/style.css'), form=form, comments=comments,
                                        count_commentaries=len(comments), base_href=f"DevelopersDiaryPublication/{id}/",
                                        bgimg=get_image_profile(current_user))
                session.close()
                return templ
        else:
            comments = session.query(Comments).filter(Comments.developers_diary_publication_id == id).order_by(Comments.created_date.desc()).all()
            templ = render_template("/DevelopersDiary.html", publication=ds_diary, status=status, user=current_user,
                                    style=url_for('static', filename='css/style.css'), form=form, comments=comments,
                                    count_commentaries=len(comments), base_href=f"DevelopersDiaryPublication/{id}/",
                                    bgimg=get_image_profile(current_user))
            session.close()
            return templ
    return redirect('/DevelopersDiary')


@app.route("/documentation/<resource>/")
def documentation(resource):
    documentation = ['UserApi-UserApiUser', 'UserApi-UserApiAdmin', 'UserApi-UserApiErrors', 'Documentation_main',
                     'WebsiteHelp', 'UserApi-UserApiErrorsAdmin', 'DevelopersDiaryApi-DevelopersDiaryUserApi',
                     'DevelopersDiaryApi-DevelopersDiaryAdminApi', 'DevelopersDiaryApi-DevelopersDiaryErrorsApi',
                     'PublicationApi-PublicationUserApi', 'PublicationApi-PublicationAdminApi',
                     'PublicationApi-PublicationErrorsApi']
    errors_dict = {'UserApiErrors': [[{'message': 'Id already exists'}, "Желаемый Id уже занят"],
                                     [{'message': 'This email already exists'}, "Желаемый email уже занят"],
                                     [{'message': "This nickname already exists"}, "Желаемый nickname уже занят"],
                                     [{'message': 'The password length must be 8 or more'}, "Длина пароля должна "
                                     "быть 8 символов и больше"],
                                     [{'message': 'The password must contain at least 1 digit'}, "Пароль должен "
                                     "содержать хотя бы 1 цифру"],
                                     [{'message': 'The password must contain at least 1 letter'}, "Пароль должен "
                                     "содержать хотя бы 1 букву"],
                                     [{'message': "Password don't match"}, "Пароль от User/Admin, и пароль, который вы "
                                                                           "вводите, не совпадают"],
                                     [{'message': 'Empty edit request'}, "Пустой словарь, в запросе на изменение, "
                                                                         "или несуществующие аргументы"],
                                     [{'message': "You don't have permissions for this"},
                                      "У вас нет прав, так могло произойти, если вы пытаетесь выполнить функции, "
                                      "которые недоступны с вашими правами. Вы можете узнать свои права заглянув "
                                      "в личный профиль, или спросив у админа"],
                                     [{'message': "User not found"}, "User, которого вы ищете, не найден"],
                                     [{'message': "Admin not found"}, "Admin, которого вы ищете, не найден"]],
                   'DevelopersDiaryErrorsApi': [[{'message': 'Id already exists'}, "Желаемый Id уже занят"],
                                                [{'message': 'This header already exists'},
                                                 "Желаемый header уже занят"],
                                                [{'message': "Password don't match"},
                                                 "Пароль от User/Admin, и пароль, который вы "
                                                 "вводите, не совпадают"],
                                                [{'message': 'Empty edit request'},
                                                 "Пустой словарь, в запросе на изменение, "
                                                 "или несуществующие аргументы"],
                                                [{'message': "You don't have permissions for this"},
                                                 "У вас нет прав, так могло произойти, если вы пытаетесь "
                                                 "выполнить функции, которые недоступны с вашими правами. Вы можете "
                                                 "узнать свои права заглянув в личный профиль, или спросив у админа"],
                                                [{'message': "User not found"}, "User, которого вы ищете, не найден"],
                                                [{'message': "Admin not found"},
                                                 "Admin, которого вы ищете, не найден"],
                                                [{'message': 'Publication not found'}, "Публикации с таким Id не "
                                                 "существует"]]}
    if resource not in documentation:
        abort(404, message="Документация не найдена")
    errors = None
    navigation_for_documentation = {'UserApi': 'UserApi/UserApiNavigation', 'Documentation_main':
                                    'DocumentationNavigation', 'WebsiteHelp': 'DocumentationNavigation',
                                    'DevelopersDiaryApi': 'DevelopersDiaryApi/DevelopersDiaryNavigation',
                                    'PublicationApi': 'PublicationApi/PublicationNavigation'}
    nav = resource.split('/')[0]
    if len(resource.split('-')) == 2:
        nav = resource.split('-')[0]
        if resource.split('-')[1] in list(errors_dict.keys()):
            errors = errors_dict[resource.split('-')[1]]
        else:
            if resource.split('-')[1] == 'PublicationErrorsApi':
                errors = errors_dict['DevelopersDiaryErrorsApi']
    return render_template(f"Documentation/{resource.replace('-', '/')}.html", navigation=True, errors=errors,
                           content_navigation=f"Documentation/{navigation_for_documentation[nav]}.html",
                           style=url_for('static', filename='css/style.css'), title=f'Документация по {resource}')


# Стартовая страница
@app.route("/")
def website_main():
    return render_template('main.html', title='Главная страница', style=url_for('static', filename='css/style.css'),
                           bgimg=get_image_profile(current_user), navigation=True)


# О нас
@app.route("/about/")
def about():
    return render_template("about.html", title="О RJKZAVRS STUDIO", style=url_for('static', filename='css/style.css'),
                           bgimg=get_image_profile(current_user))


# всё что связано с публикацией
@app.route('/PublicationsAdd/', methods=['GET', 'POST'])
@login_required
def publication_add():
    form = PublicationsForm()
    if form.submit.data:
        session = db_session.create_session()
        if session.query(Publications).filter(Publications.header == form.header.data).first():
            return render_template('PublicationsAdd.html', title='Создание записи', form=form,
                                   message="Запись с таким же названием уже существует",
                                   style=url_for('static', filename='css/style.css'),
                                   bgimg=get_image_profile(current_user))
        session.commit()
        session = db_session.create_session()
        publication = Publications()
        publication.header = form.header.data
        publication.body = form.body.data
        publication.created_date = datetime.datetime.now()
        current_user.publications.append(publication)
        session.merge(current_user)
        session.commit()
        return redirect('/Publications')
    return render_template('PublicationsAdd.html', title='Создание записи', form=form,
                           style=url_for('static', filename='css/style.css'),
                           bgimg=get_image_profile(current_user))


@app.route('/PublicationEdit/<int:id>/', methods=['GET', 'POST'])
@login_required
def publication_edit(id):
    session = db_session.create_session()
    publication = session.query(Publications).get(id)
    if publication and (current_user.status >= 1 or publication.author_id == current_user.id):
        form = PublicationsForm()
        if request.method == "GET":
            session.close()
            if publication:
                form.header.data = publication.header
                form.body.data = publication.body
            else:
                abort(404)
        if form.submit.data:
            publication.header = form.header.data
            publication.body = form.body.data
            session.commit()
            return redirect('/Publications')
        else:
            return render_template('PublicationsAdd.html', title='Редактирование записи',
                                   form=form, style=url_for('static', filename='css/style.css'),
                                   bgimg=get_image_profile(current_user))
    else:
        session.close()
        abort(404)


@app.route('/PublicationDelete/<int:id>/', methods=['GET', 'POST'])
@login_required
def publication_delete(id):
    session = db_session.create_session()
    publication = session.query(Publications).get(id)
    if publication and (current_user.status >= 1 or publication.author_id == current_user.id):
        session.delete(publication)
        session.commit()
        return redirect("/Publications")
    else:
        session.close()
        abort(404)


@app.route("/Publications/")
def publication_list():
    status = 0
    if current_user.is_authenticated:
        status = current_user.status + 1
    session = db_session.create_session()
    publication = session.query(Publications).all()
    session.close()
    return render_template("/Publications.html", publications=publication, status=status, user=current_user,
                           style=url_for('static', filename='css/style.css'),
                           bgimg=get_image_profile(current_user))


@app.route("/Publication/<int:public_id>/<int:comment_id>/", methods=['GET', 'POST'])
@login_required
def publication_change_comment(public_id, comment_id):
    form = CommentsForm()
    if form.submit.data:
        session = db_session.create_session()
        comment = session.query(Comments).get(comment_id)
        if comment.author_id == current_user.id or current_user.status >= 2:
            comment.text = form.text.data
            form.text.data = ""
            session.commit()
            return redirect(f"/Publication/{public_id}/")
        else:
            session.close()
            return redirect(f"/Publication/{public_id}/")
    else:
        session = db_session.create_session()
        comment = session.query(Comments).get(comment_id)
        session.close()
        if comment.author_id == current_user.id or current_user.status >= 2:
            session = db_session.create_session()
            comments = session.query(Comments).filter(Comments.publication_id == public_id).order_by(Comments.created_date.desc()).all()
            form.text.data = comment.text
            publication = session.query(Publications).filter(Publications.id == public_id).first()
            status = current_user.status + 1
            templ = render_template("/Publication.html", publication=publication, status=status, user=current_user,
                                    style=url_for('static', filename='css/style.css'), form=form, comments=comments,
                                    count_commentaries=len(comments), base_href=f"Publication/{public_id}/",
                                    bgimg=get_image_profile(current_user))
            session.close()
            return templ
        else:
            abort(400, message="Отказао в доступе")


@app.route("/game_about")
def about_game():
    number = 0
    while True:
        if not os.path.exists(f'static/img/game_img/game_about_{number + 1}.png'):
            break
        else:
            number += 1
    numbers = []
    for i in range(1, number + 1):
        numbers.append(i)
    return render_template("Game_about.html", style=url_for('static', filename='css/style.css'),
                           bgimg=get_image_profile(current_user), numbers=numbers)


@app.route("/Publication/<int:id>/", methods=['GET', 'POST'])
def publication(id):
    status = 0
    if current_user.is_authenticated:
        status = current_user.status + 1
    session = db_session.create_session()
    publication = session.query(Publications).get(id)
    session.close()
    if publication:
        form = CommentsForm()
        if form.submit.data:
            if current_user.is_authenticated:
                session = db_session.create_session()
                user = session.query(User).get(current_user.id)
                publication = session.query(Publications).get(id)
                comment = Comments()
                comment.text = form.text.data
                comment.created_date = datetime.datetime.now()
                form.text.data = ""
                user.comments.append(comment)
                session.merge(user)
                publication.comments.append(comment)
                session.merge(publication)
                session.commit()
                session = db_session.create_session()
                comments = session.query(Comments).filter(Comments.publication_id == id).order_by(
                    Comments.created_date.desc()).all()
                templ = render_template("/Publication.html", publication=publication, status=status, user=current_user,
                                        style=url_for('static', filename='css/style.css'), form=form, comments=comments,
                                        count_commentaries=len(comments), base_href=f"Publication/{id}/",
                                        bgimg=get_image_profile(current_user))
                session.close()
                return templ
        else:
            comments = session.query(Comments).filter(Comments.publication_id == id).order_by(
                Comments.created_date.desc()).all()
            templ = render_template("/Publication.html", publication=publication, status=status, user=current_user,
                                    style=url_for('static', filename='css/style.css'), form=form, comments=comments,
                                    count_commentaries=len(comments), base_href=f"Publication/{id}/",
                                    bgimg=get_image_profile(current_user))
            session.close()
            return templ
    return redirect('/Publications')


if __name__ == '__main__':
    print('http://127.0.0.1:8000/game_about')
    main(port=8000)
    create_new_db = False
    if create_new_db:
        db_session.global_init("Followers_Rjkzavrs.sqlite")
        session = db_session.create_session()
        user = User()
        session.add(user)
        session.commit()
        session = db_session.create_session()
        session.add(Publications())
        session.add(DevelopersDiary())
        session.add(Products())
        session.commit()
        session = db_session.create_session()
        session.add(Comments())
        session.commit()
        print('Успех!')
