from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    nickname = StringField('Никнейм', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class PublicationsForm(FlaskForm):
    header = StringField('Заголовок публикации', validators=[DataRequired()])
    body = TextAreaField('Содержание публикации', validators=[DataRequired()])
    availability_status = BooleanField("только для зарегистрированных пользователей")
    submit = SubmitField("Готово")


class DevelopersDiaryForm(FlaskForm):
    header = StringField('Заголовок публикации', validators=[DataRequired()])
    body = TextAreaField('Содержание публикации', validators=[DataRequired()])
    choices = [(0, 'Все пользователи'), (1, 'Только зарегестрированные и выше'), (2, 'Только разработчики')]
    availability_status = SelectField('Доступ к публикации', choices=choices, validators=[DataRequired()], default=choices[0])
    submit = SubmitField("Готово")


class EditAccountForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    nickname = StringField('Никнейм', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    choices = [(0, 'Герои на первом плане'), (1, '"Логотип" Обои'), (2, 'Гг'), (3, 'Игра')]
    background_image_id = SelectField('Доступ к публикации', choices=choices, validators=[DataRequired()], default=choices[0])


class DeleteForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
