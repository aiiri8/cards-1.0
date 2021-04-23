from flask import Flask, render_template
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

PORT = 8080
HOST = '127.0.0.1'


def main():
    db_session.global_init("db/ege_db.db")

    user = User()
    user.surname = 'Пользователь'
    user.name = '4'
    user.about = 'Четвертый пользователь'
    user.email = 'user4@example.ru'

    password = '444'
    user.set_password(password)

    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()

    # app.run(port=PORT, host=HOST)


if __name__ == '__main__':
    main()
