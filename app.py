import random

from PIL import Image
from flask import Flask, render_template, request, make_response, jsonify
from werkzeug.exceptions import abort
from werkzeug.utils import redirect, secure_filename

from data import db_session, news_api
from data.cards import Card
from data.news import News
from data.results import Res
from data.users import User
from data.users_cards import Users_Card
from forms.cards import CardForm
from forms.news import NewsForm

from forms.user_login import LoginForm
from forms.user_register import RegisterForm

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


login_manager = LoginManager()
login_manager.init_app(app)

PORT = 8080
HOST = '127.0.0.1'


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)

    return render_template("index.html", title='Главная',
                           news=news)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form, message="Пароли не совпадают")

        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form, message="Такой пользователь уже есть")

        user = User(surname=form.surname.data,
                    name=form.name.data,
                    email=form.email.data,
                    about=form.about.data)
        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()

        return redirect('/login')

    return render_template('register.html', title='Регистрация',
                           form=form)


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

        return render_template('login.html', message="Неправильный логин или пароль",
                               form=form)

    return render_template('login.html', title='Авторизация',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect("/")


# @app.route('/only_for_users')
# def only_for_users():
#     if current_user.is_authenticated:
#         return redirect("/")
#
#     return render_template("only_for_users.html", title='Ошибка!')


@app.route('/blog')
@login_required
def blog():
    db_sess = db_session.create_session()

    if current_user.is_authenticated:
        news = db_sess.query(News).filter(News.user == current_user)
    # else:
    #     return redirect("/only_for_users")

    return render_template("blog.html", title='Ваш блог',
                           news=news)


@app.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    # if not current_user.is_authenticated:
    #     return redirect("/only_for_users")

    form = NewsForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data

        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()

        return redirect('/blog')

    return render_template('news.html', title='Добавление новости',
                           form=form)


@app.route('/edit_news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    # if not current_user.is_authenticated:
    #     return redirect("/only_for_users")

    form = NewsForm()

    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()

        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private

        else:
            abort(404)

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()

        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/blog')

        else:
            abort(404)

    return render_template('news.html', title='Редактирование новости',
                           form=form)


@app.route('/delete_news/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    # if not current_user.is_authenticated:
    #     return redirect("/only_for_users")

    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()

    if news:
        db_sess.delete(news)
        db_sess.commit()

    else:
        abort(404)

    return redirect('/blog')


@app.route('/cards')
def show_cards():
    db_sess = db_session.create_session()

    cards = db_sess.query(Card)

    users_cards = []
    if current_user.is_authenticated:
        users_cards = db_sess.query(Users_Card).filter(Users_Card.user == current_user)

    return render_template("cards.html", title='Карточки',
                           cards=cards, users_cards=users_cards)


@app.route('/my_cards')
@login_required
def my_cards():
    db_sess = db_session.create_session()

    if current_user.is_authenticated:
        cards = db_sess.query(Users_Card).filter(Users_Card.user == current_user)
    # else:
    #     return redirect("/only_for_users")

    return render_template("my_cards.html", title='Ваши карточки',
                           cards=cards)


@app.route('/add_card', methods=['GET', 'POST'])
@login_required
def add_card():
    # if not current_user.is_authenticated:
    #     return redirect("/only_for_users")

    SIZE = (1200, 800)

    form = CardForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        db_sess.expire_on_commit = False

        card = Users_Card()
        card.word = form.word.data
        card.user_id = current_user.id

        filename = secure_filename(form.img.data.filename).split('/')[-1]
        print(filename)
        way = filename.split('.')[0] + str(card.user_id) + '.' + filename.split('.')[-1]
        way = './static/img/users_cards/' + way
        form.img.data.save(way)

        im = Image.open(way)
        im = im.resize(SIZE)
        im.save(way)

        card.img = way

        current_user.card.append(card)
        db_sess.merge(current_user)
        db_sess.commit()

        return redirect('/my_cards')

    return render_template('change_card.html', title='Добавление карточки',
                           form=form)


@app.route('/delete_card/<int:id>', methods=['GET', 'POST'])
@login_required
def card_delete(id):
    # if not current_user.is_authenticated:
    #     return redirect("/only_for_users")

    db_sess = db_session.create_session()
    card = db_sess.query(Users_Card).filter(Users_Card.id == id, Users_Card.user == current_user).first()

    if card:
        db_sess.delete(card)
        db_sess.commit()

    else:
        abort(404)

    return redirect('/my_cards')


@app.route('/testing', methods=['POST', 'GET'])
@app.route('/testing/<color>', methods=['POST', 'GET'])
def testing(color="light"):
    print(request.method)
    if request.method == 'GET':
        db_sess = db_session.create_session()

        all_cards = list(map(lambda x: (x.word, x.img), db_sess.query(Card)))
        if current_user.is_authenticated:
            u_cards = db_sess.query(Users_Card).filter(Users_Card.user == current_user)
            all_cards += list(map(lambda x: (x.word, x.img), u_cards))

        card = random.choice(all_cards)
        print(card[1])

        return render_template('test.html', title='Тестирование', card=card, color=color)


@app.route('/test/<word>', methods=['POST', 'GET'])
def check_ans(word):
    if current_user.is_authenticated:
        res = Res()
        res.word = word
        res.answer = request.form['answer']
        res.is_right = bool(res.word.lower() == res.answer.lower())
        res.user_id = current_user.id

        db_sess = db_session.create_session()
        db_sess.add(res)
        db_sess.commit()

    if word.lower() == request.form['answer'].lower():
        color = "success"
    else:
        color = "danger"

    return redirect(f"/testing/{color}")


@app.route('/stats')
@login_required
def stats():
    db_sess = db_session.create_session()
    results = db_sess.query(Res).filter(Res.user == current_user)
    print(results)

    return render_template('stats.html', title='Добавление карточки',
                           results=results)


def main():
    db_session.global_init("ege_db.db")
    app.register_blueprint(news_api.blueprint)
    app.run(port=PORT, host=HOST)


if __name__ == '__main__':
    main()
