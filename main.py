import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, send

from data import db_session
from data.chatmessege import ChatMessages
from data.users import User
from forms.loginform import LoginForm
from forms.user import RegisterForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['DEBUG'] = True
socketio = SocketIO(app)


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


def main():
    db_session.global_init("db/blogs.db")
    socketio.run(app)


@app.route('/today')
def today():
    zodiac = 'scorpio'
    today, tomorrow = get_content_html(zodiac)
    print(today)
    return render_template("today.html", img=f'static/img/zodiac/{zodiac}.png', astronomy_today=today,
                           zodiac=zodiac)


@app.route('/tomorrow')
def tomorrow():
    zodiac = 'scorpio'
    today, tomorrow = get_content_html(zodiac)
    return render_template("tomorrow.html", img=f'static/img/zodiac/{zodiac}.png',
                           astronomy_tomorrow=tomorrow, zodiac=zodiac)


@socketio.on('message')
def handleMessage(data):
    print(f"Message: {data}")
    send(data, broadcast=True)

    db_sess = db_session.create_session()
    message = ChatMessages(username=data['username'], msg=data['msg'])
    db_sess.add(message)
    db_sess.commit()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    # if current_user.is_authenticated:
    #    news = db_sess.query(News).filter(
    #       (News.user == current_user) | (News.is_private != True))
    # else:
    #   news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html")


@app.route("/profile")
def profile():
    db_sess = db_session.create_session()
    # if current_user.is_authenticated:
    #    news = db_sess.query(News).filter(
    #       (News.user == current_user) | (News.is_private != True))
    # else:
    #   news = db_sess.query(News).filter(News.is_private != True)
    return render_template("profile.html")


@app.route("/messenger")
def messenger():
    print(session)
    username = current_user.name
    return render_template('message.html', username=username)


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
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            sex=form.sex.data,
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
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
