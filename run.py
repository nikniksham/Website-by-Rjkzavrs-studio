from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "admin123"
login_manager = LoginManager()
login_manager.init_app(app)


# открывают наш сайт
@app.route("/")
def hello():
    return "<h1>Welcome to my web site.<h1>"


def main():
    app.run()


if __name__ == '__main__':
    main()