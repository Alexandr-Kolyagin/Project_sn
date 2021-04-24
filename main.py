import random

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, Blueprint, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import flask_ngrok
from checl import zodiac_serch, eng_zodiac, rus_zodiac
from data import db_session
from data.users import User
from data.friends import Friend
from forms.loginform import LoginForm
from forms.user import RegisterForm

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['JSON_AS_ASCII'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# flask_ngrok.run_with_ngrok(app)
symbols = 'qwertyuipasdfghjkzxcvbnm23456789QWERTYUPASDFGHJKLZXCVBNM'
blueprint = Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route('/today')
def today():
    zodiac = eng_zodiac(current_user.zodiac)
    today, tomorrow = get_content_html(zodiac)
    print(today)
    return render_template("today.html", img=f'static/img/zodiac/{zodiac}.png',
                           astronomy_today=today,
                           zodiac=str(current_user.zodiac).capitalize(),
                           title='Гороскоп на сегодня')


@app.route('/tomorrow')
def tomorrow():
    zodiac = eng_zodiac(current_user.zodiac)
    today, tomorrow = get_content_html(zodiac)
    return render_template("tomorrow.html", img=f'static/img/zodiac/{zodiac}.png',
                           astronomy_tomorrow=tomorrow,
                           zodiac=str(current_user.zodiac).capitalize(), title='Гороскоп на завтра')


@app.route("/")
def index():
    db_sess = db_session.create_session()
    # if current_user.is_authenticated:
    #    news = db_sess.query(News).filter(
    #       (News.user == current_user) | (News.is_private != True))
    # else:
    #   news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html")


@app.route("/magic")
def magic():
    zodiac = eng_zodiac(current_user.zodiac)

    return render_template('magic.html', title='Магия', img=f'static/img/zodiac/{zodiac}.png')


@app.route("/magicball")
def magic_ball():
    return render_template('magic_ball.html', title='Магический шар')


@app.route("/<int:id>")
def profile(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    zodiac = eng_zodiac(user.zodiac)
    return render_template("profile.html", zodiac=str(user.zodiac).capitalize(),
                           img=f'static/img/zodiac/{zodiac}.png',
                           title=user.name + " " + user.surname, user=user)


@app.route('/add_friend/<int:id>', methods=['GET', 'POST'])
@login_required
def product_add_basket(id):
    db_sess = db_session.create_session()
    friend = Friend()
    friend.user_friend_id = id
    current_user.friends.append(friend)
    db_sess.merge(current_user)
    db_sess.commit()
    return redirect(f'/{id}')


# @app.route("/messenger")
# def messenger():
#     form = MessageForm()
#     if form.validate_on_submit():
#         pass
#
#     username = current_user.name
#     return render_template('message.html', username=username)


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
        zodiac = zodiac_serch(form.date_birth.data)
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            sex=form.sex.data,
            zodiac=zodiac,
            date_birth=form.date_birth.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, title='Авторизация')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/api/<zodiac>')
def get_zodiac(zodiac):
    today, tomorrow = get_content_html(zodiac)
    return jsonify(
        {'zodiac_name': zodiac,
         'zodiac_today':
             today.replace('\n', ''),
         'zodiac_tommorow':
             tomorrow.replace('\n', '')
         }
    )


@app.route('/api/users_data/<user_id>')
def get_data(user_id):
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.id == user_id).first():
        user = db_sess.query(User).filter(User.id == user_id).first()
        return jsonify(
            {
                'user_id': user.id,
                'user_name': user.name,
                'user_zodiac': eng_zodiac(user.zodiac),
                'user_birth': user.date_birth,
                'user_sex': user.sex,
                'user_admin': user.admin
            }
        )
    else:
        return 'Данного пользователя не существует'

def generate_password():
    x = ''.join(random.sample(symbols, 10))
    return x


def get_content_html(zodiac):
    der = {}
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Mobile Safari/537.36',
        'accept': '*/*'}
    html = requests.get(f'https://horo.mail.ru/prediction/{zodiac}/today/', headers=HEADERS)
    html = html.text
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='text text_color_white text_large padding_10')
    for d, item in enumerate(items):
        if d != 3 and d != 4:
            text_all = str(item.get_text()).split(' ')[:4]
            for i in text_all[-1]:
                if i != i.lower():
                    what = text_all[-1][:text_all[-1].index(i)]
                    what_2 = text_all[-1][text_all[-1].index(i):]
            der[str(' '.join(text_all[:3]) + ' ' + what)] = what_2 + ' ' + ' '.join(
                str(item.get_text()).split(' ')[4:])
    return der[list(der.keys())[1]], der[list(der.keys())[2]]


if __name__ == '__main__':
    main()
