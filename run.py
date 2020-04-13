from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key_by_rjkzavr_1920"
login_manager = LoginManager()
login_manager.init_app(app)


# открывают наш сайт
@app.route("/")
def hello():
    return '''<!DOCTYPE html>
            <html lang="en">
            <head>
               <meta charset="UTF-8">
                   <title>Марс</title>
               </head>
               <body>
                   <h1>Миссия Колонизация Марса</h1>
                   <h1>И на марсе будут яблони цвести!</h1>
               </body>
            </html>'''


def main(port=8000):
    app.run(port=port)


if __name__ == '__main__':
    main()
