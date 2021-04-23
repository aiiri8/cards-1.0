from flask import Flask, render_template
from data import db_session
from data.news import News

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

PORT = 8080
HOST = '127.0.0.1'


def main():
    db_session.global_init("db/ege_db.db")

    news = News()
    news.title = 'Новость # 3'
    news.content = 'И еще одна новость'
    news.is_private = False
    news.user_id = 3

    db_sess = db_session.create_session()
    db_sess.add(news)
    db_sess.commit()

    # app.run(port=PORT, host=HOST)


if __name__ == '__main__':
    main()
