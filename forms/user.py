import wtforms
from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField,DateField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = wtforms.PasswordField('Пароль', validators=[DataRequired()])
    password_again = wtforms.PasswordField('Повторите пароль', validators=[DataRequired()])
    name = wtforms.StringField('Имя пользователя', validators=[DataRequired()])
    surname = wtforms.StringField('Фамилия пользователя', validators=[DataRequired()])
    sex = wtforms.RadioField('Пол', validators=[DataRequired()], choices=['male', 'female'])
    date_birth = wtforms.DateField('Дата рождения', validators=[DataRequired()])
    submit = wtforms.SubmitField('Зарегистрироваться')
