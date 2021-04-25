import os
import psutil

from data import db_session
from data.users import User


class Nataly():
    def __init__(self):
        self.name = 'наташа'
        self.answer_list = {
            1: "Привет",
            2: "Открываю",
            3: "Запускаю",
            4: "Ищу",
        }
        self.admin = False
        self.error_list = {
            1: "-----------ОШИБКА-----------\n Не указанно название сайта\n---------------------------"

        }

    def aswer(self, number):
        # playsound(self.answer_list_audio[number])
        return f'{self.name.title()} : {self.answer_list[number]}'

    def function(self):
        return (f'Список команд\n'
        ' ------------------------------------------------------- \n' \
        f'Показ гороскопа. Пример : "{self.name.capitalize()} открой гороскоп на сегодня"\n' \
        f' Запуск магического шара: Пример : "{self.name.capitalize()} открой магический шар"\n' \
        ' --------------Команды для Админа-----------------------\n' \
        f' Информация о пользователях : Пример : "{self.name.capitalize()} покажи информацию пользователя с id 1"\n' \
        f' Удаление пользователей : Пример : "{self.name.capitalize()} удали пользователя с id 1"\n' \
        '-------------------------------------------------------')

    def open(self, text):
        if text == 'сегодня':
            os.startfile(f"http://127.0.0.1:5000/today")
            return 'Открываю...'
        elif text == 'завтра':
            os.startfile(f"http://127.0.0.1:5000/tomorrow")
            return 'Открываю...'

    def show_user(self, id):
        if self.admin:
            os.startfile(f'http://127.0.0.1:5000/api/users_data/{id}')
            return f'Информация о пользователе с id "{id}" показана'
        else:
            return 'У вас недостаточно прав'

    def delete_user(self, id):
        if self.admin:
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.id == id).first():
                user = db_sess.query(User).filter(User.id == id).first()
                db_sess.delete(user)
                db_sess.commit()
                return f'Пользователь с id "{id}" удален'
            else:
                return 'Данного пользователя не существует'
        else:
            return 'У вас недостаточно прав'

    def close(self, text):
        for process in (process for process in psutil.process_iter() if
                        process.name() == f'{text[0]}.exe'):
            process.kill()

    def change_name(self, name):
        self.name = name
