import os.path

from PIL import Image

from flask import Flask, render_template
from data import db_session
from data.cards import Card

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

PORT = 8080
HOST = '127.0.0.1'

SIZE = (1200, 800)

def main():
    db_session.global_init("db/ege_db.db")

    card = Card()
    card.word = 'family'.lower()

    # полный путь к файлу
    img = 'C:/Users/<>/OneDrive/Рабочий стол/Безымянный.png'

    if 50 > len(card.word) > 0 and len(card.word.split()) == 1:

        if os.path.isfile(img):

            try:
                im = Image.open(img)
                out = im.resize(SIZE)
                way = card.word + '.' +  img.split('/')[-1].split('.')[-1]
                out.save('static/img/cards/' + way)

                card.img = './static/img/cards/' + way

                db_sess = db_session.create_session()
                db_sess.add(card)
                db_sess.commit()

                # app.run(port=PORT, host=HOST)

            except Exception as ex:
                print('Ошибка при добавлении карточки: ', ex)

        else:
            print('Такого изображения не существует')

    else:
        print('Карточке должно соответствовать слово длинной от 1 до 50 символов')


if __name__ == '__main__':
    main()
