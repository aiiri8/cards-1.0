from flask import Flask, render_template
from data import db_session
from data.results import Res

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

PORT = 8080
HOST = '127.0.0.1'


def main():
    db_session.global_init("db/ege_db.db")

    res = Res()
    res.word = 'кремль'
    res.answer = 'Кремль'
    res.is_right = bool(res.word.lower() == res.answer.lower())
    res.user_id = 4

    db_sess = db_session.create_session()
    db_sess.add(res)
    db_sess.commit()

    # app.run(port=PORT, host=HOST)


if __name__ == '__main__':
    main()
