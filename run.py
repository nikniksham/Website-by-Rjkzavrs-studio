from flask import Flask, render_template, url_for
from flask_login import LoginManager, login_required, logout_user
from werkzeug.utils import redirect
from data import db_session
from data.users import User
from data.publications import Publications
from data.developers_diary import DevelopersDiary
from data.products import Products

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key_by_rjkzavr_1920"
login_manager = LoginManager()
login_manager.init_app(app)


def main(port=8000):
    db_session.global_init("db/Followers_Rjkzavrs.sqlite")
    app.run(port=port)


# Получение последователя великих Rjkzavrs
@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


# Выйти с профиля на сайте
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect("/")


# Стартовая страница
@app.route("/")
def website_main():
    return render_template('main.html', title='Главная страница', style=url_for('static', filename='css/style.css'), bgimg=url_for('static', filename='img/background_img_1.png'))


if __name__ == '__main__':
    main()
    create_new_db = False
    if create_new_db:
        db_session.global_init("db/Followers_Rjkzavrs.sqlite")
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
        session.commit()
        print('Успех!')
