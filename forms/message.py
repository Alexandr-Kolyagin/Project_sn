import wtforms
from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField,DateField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    text = wtforms.TextAreaField('Введите сообщение', validators=[DataRequired()])
    submit = wtforms.SubmitField('Отправить')
