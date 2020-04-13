from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    city_from = StringField('Родной город', validators=[DataRequired()])
    address = TextAreaField("Адрес", validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


class WorksForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    team_leader = StringField("Главный", validators=[DataRequired()])
    work_size = StringField("Объём работы", validators=[DataRequired()])
    collaborators = StringField('Участники', validators=[DataRequired()])
    hazard_category = StringField('Категория опасности', validators=[DataRequired()])
    is_finished = BooleanField("Завершена ли работа?")
    submit = SubmitField("Далее")


class DepartmentsForm(FlaskForm):
    title = StringField("Название департамента", validators=[DataRequired()])
    chief = StringField("Главный департамента", validators=[DataRequired()])
    members = StringField("ID работников департамента", validators=[DataRequired()])
    email = StringField("Email департамента", validators=[DataRequired()])
    submit = SubmitField("Далее")


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class LoginForm2(FlaskForm):
    id_astronaut = StringField('Id астронавта', validators=[DataRequired()])
    password_astronaut = PasswordField('Пароль астронавта', validators=[DataRequired()])
    id_captain = StringField('Id капитана', validators=[DataRequired()])
    password_captain = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')