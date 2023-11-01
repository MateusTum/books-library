from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm


class MyForm(FlaskForm):
    book_name = StringField('Book Name', validators=[DataRequired()])
    book_author = StringField('Book Author', validators=[DataRequired()])
    book_rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=0, max=10)])
    submit = SubmitField('Add Book')


class EditRatingForm(FlaskForm):
    new_book_rating = (IntegerField('New Book Rating', validators=[DataRequired(), NumberRange(min=0, max=10)]))
    submit = SubmitField('Change Rating')