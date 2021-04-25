import speech_recognition as sr
from Assistant import Nataly
import sys
from data import db_session
from PyQt5 import uic
from PyQt5.QtWidgets import *
from playsound import playsound
from data.users import User

nat = Nataly()


def auth():
    db_session.global_init("../db/blogs.db")
    db_sess = db_session.create_session()
    print('Введите почту')
    email = input()
    while db_sess.query(User).filter(User.email == email).first() == None:
        print('Данный пользователь не существует, повторите попытку')
        email = input()
    user = db_sess.query(User).filter(User.email == email).first()
    print('Введите пароль')
    password = input()
    while not (user and user.check_password(password)):
        print('Неправильный пароль, повторите попытку')
        password = input()
    nat.admin = user.admin

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('Interface/interface_natasha.ui', self)
        self.setWindowTitle('VoiceAssistant')
        self.run_voice.clicked.connect(self.record_volume)
        self.running = False

    def aswer(self,number):
        answer_list = {
            1: "Привет",
            2: "Открываю",
            3: "Запускаю",
            4: "Ищу",
        }
        return f'Наташа:{answer_list[number]}'

    def record_volume(self):
        r = sr.Recognizer()
        flag = False
        with sr.Microphone(device_index=1) as source:
            r.adjust_for_ambient_noise(source, duration=1)  # настройка посторонних шумов
            audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='ru-RU')
            Text = query.lower().split(' ')
            if nat.name in Text:
                self.plainTextEdit.appendPlainText('Вы:')
                self.plainTextEdit.appendPlainText(' '.join(Text).capitalize())
                del Text[Text.index(nat.name)]
                flag = True
            if flag:
                if Text[0] == 'привет':
                    print(nat.aswer(1))
                    playsound('Files\Voice Answers\Hi.mp3')
                elif Text[0] == 'открой':
                    self.plainTextEdit.appendPlainText(f'{nat.name.capitalize()}:')
                    self.plainTextEdit.appendPlainText(nat.open(Text[-1]))
                elif Text[0] == 'покажи':
                    self.plainTextEdit.appendPlainText(f'{nat.name.capitalize()}:')
                    self.plainTextEdit.appendPlainText(nat.show_user(Text[-1]))
                elif Text[0] == 'удали' or Text[0] == 'удалить':
                    self.plainTextEdit.appendPlainText(f'{nat.name.capitalize()}:')
                    self.plainTextEdit.appendPlainText(nat.delete_user(Text[-1]))
                elif Text == ['что', 'ты', 'умеешь']:
                    self.plainTextEdit.clear()
                    self.plainTextEdit.appendPlainText(f'{nat.name.capitalize()}:')
                    self.plainTextEdit.appendPlainText(nat.function())
                elif Text[:-1] == ['смени', 'имя', 'на']:
                    nat.change_name(Text[-1])
                elif Text[0] == 'очисть' or Text[0] == 'очистить':
                    self.plainTextEdit.clear()
                    self.plainTextEdit.appendPlainText('Чат очищен....')
                else:
                    self.plainTextEdit.appendPlainText('Неизвестная команда')
        except:
            pass


if __name__ == '__main__':
    auth()
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    # if ex.running:
    #     # record_volume()
    #     print(1)
    # print(ex.running)
    sys.exit(app.exec())
