from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.exc import OperationalError
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from forms import MyForm, EditRatingForm

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db.init_app(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

# with app.app_context():
#     db.create_all()


@app.route('/')
def home():
    books_in_db = db.session.query(Books).all()
    return render_template('index.html', books=books_in_db)


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = MyForm()
    if form.validate_on_submit():
        try:
            max_book_id = db.session.query(db.func.max(Books.id)).scalar()
        except OperationalError:
            new_book_id = 1
        else:
            new_book_id = (max_book_id or 0) + 1

        book = Books(
            id=new_book_id,
            title=request.form["book_name"],
            author=request.form["book_author"],
            rating=request.form["book_rating"]
        )

        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


@app.route("/edit/<int:book_id>", methods=['GET', 'POST'])
def edit_rating(book_id):
    form = EditRatingForm()
    selected_book = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
    if form.validate_on_submit():
        selected_book.rating = request.form["new_book_rating"]
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit_rating.html', book=selected_book, form=form)


@app.route("/delete/<int:book_id>")
def delete_book(book_id):
    book_to_delete = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
