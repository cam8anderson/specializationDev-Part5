"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/movies')
def all_movies():
    movies = crud.get_movies()

    return render_template('all_movies.html', movies=movies)

@app.route('/movies/<movie_id>', methods=['GET' ,'POST'])
def show_movie(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    
    if request.method == 'POST':

        email = request.form.get('email')

        user = crud.get_user_by_email(email)

        if user is None:
            flash('User does not exist')
            return redirect('/')

        rating_score = int(request.form.get('rating_score'))

        rating = crud.create_rating(user, movie, rating_score)
        db.session.add(rating)
        db.session.commit()

        flash('Rating added successfully!')
        return redirect('/movies')
    else:
        return render_template('movie_details.html', movie=movie)

@app.route('/users')
def all_users():
    users = crud.get_users()

    return render_template('users.html', users=users)

@app.route('/users/<user_id>')
def show_user(user_id):
    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)

@app.route('/users', methods=['POST'])
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:
        flash("this email already exists")

    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("account created! log in")
    
    return redirect('/')

@app.route('/login', methods=['POST'])
def user_login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:
        check = crud.get_user_password(password, email)
        if check:
            flash("you have logged in!")
        else:
            flash('password was wrong. try again')
    else:
        flash("user doesn't exist please register.")

    return redirect('/')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0")
