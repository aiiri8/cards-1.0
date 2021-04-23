from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms import StringField, validators
from wtforms import SubmitField
from wtforms.validators import DataRequired, Length


class CardForm(FlaskForm):
    word = StringField('Слово (одно!!!)',
                       validators=[DataRequired(),
                                   Length(min=1, max=50,
                                          message='Карточке должно соответствовать слово длинной от 1 до 50 символов')])
    img = FileField('Изображение',
                    validators=[FileRequired(),
                                FileAllowed(['jpg', 'png'],
                                            'Пожалуйста, прикрепите изображение в формате .jpg или .png!'                                                                                          '')])
    submit = SubmitField('Опубликовать')
