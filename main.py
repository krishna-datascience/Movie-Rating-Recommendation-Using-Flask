from flask import Flask, render_template, redirect, request,session,flash
from model import connect_to_db, db, User, Rating, Movie

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'some random string'

@app.route('/')
def index():

	return render_template("index.html")

@app.route('/login', methods=['GET'])
def login():
	"""This will show you the login form."""

	return render_template("login_form.html")

@app.route('/login', methods=['POST'])
def submit_login():
	"""This form will submit login information & return you to the homepage."""

	email = request.form.get('email')
	password = request.form.get('password')

	user = User.query.filter_by(email=email).first()

	if not user:
		flash("No such user!")
		return redirect("/login")

	if user.password != password:
		flash("Incorrect password")
		return redirect("/login")

	session["user_id"] = user.id

    # session["logged_in"] = user.email
	flash("You have been successfully logged in!")
	return redirect('/user-page/{}'.format(user.id))

@app.route('/logout')
def logout():
	"""Log out."""

	del session["user_id"]
	flash("Logged Out.")
	return redirect("/")

@app.route("/users")
def user_list():
	"""Show list of users."""

	users = User.query.all()
	return render_template("user_list.html", users=users)

@app.route('/user-page/<int:user_id>')
def user_page(user_id):
	""" the user's personal webpage to remind us who they are"""
    
	current_user = User.query.filter_by(id=user_id).first()
	email = current_user.email
	zipcode = current_user.zipcode
	age = current_user.age
	# thing = current_user.id

	# movie_list = db.session.query(Rating.rating,
	# 	Movie.title).join(Movie).filter(Rating.user_id==thing).all()
	rating = Rating.query.filter_by(user_id = user_id).all()
	movie_list = []
	for i in rating:
		movie = Movie.query.filter_by(id = i.movie_id).first()
		for j in movie_list:
			if movie == j[0]:
				movie_list.remove(j)
		movie_list.append([movie,i.rating])

	return render_template("user_page.html", user=current_user, email=email, user_id=user_id,
		zipcode=zipcode, age=age, movie_list=movie_list)

@app.route('/movies')
def full_list_of_movies():
	"""this returns the full list of movies in the database. Includes link
	to individual movie page."""

	movies = Movie.query.order_by(Movie.title).all()
	return render_template('movie_list.html', movies=movies)

@app.route('/movies/<int:movie_id>', methods=['GET'])
def movie_page(movie_id):
	"""Contains all of the information about a particular
	movie in our database."""
	
	movie = Movie.query.filter_by(id=movie_id).first()
	title = movie.title
	released = movie.release_date
	url = movie.imdb_url
	thing = movie.id

	# movie_rating = db.session.query(Rating.rating).join(Movie).filter(
 #        Movie.id==thing).all()

	all_ratings = Rating.query.filter_by(movie_id=movie.id).all()

	
	user_id = session.get("user_id")

	if user_id:
		user_rating = Rating.query.filter_by(
			movie_id=movie_id, user_id=user_id).first()
	else:
		user_rating = None

	rating_scores = [r.rating for r in all_ratings]
	avg_rating = float(sum(rating_scores)) / len(rating_scores)
	avg_rating = f'{avg_rating:.2f}'

	prediction = None

	# Prediction code: only predict if the user hasn't rated it.
	if (not user_rating) and user_id:
		user = User.query.get(user_id)
		if user:
			prediction = user.predict_rating(movie)

	# Either use the prediction or their real rating

	if prediction:
		# User hasn't scored; use our prediction if we made one
		if int(str(prediction).split('.')[1][0])>=5:
			prediction = int(prediction)+1
		else:
			prediction = int(prediction)
		effective_rating = prediction
	elif user_rating:
		# User has already scored for real; use that
		effective_rating = user_rating.rating
	else:
		# User hasn't scored, and we couldn't get a prediction
		effective_rating = None


	return render_template('movie_page.html',movie=movie,
		user_rating=user_rating, average=avg_rating,
		prediction=prediction, all_ratings = all_ratings)

@app.route("/add_rating", methods=["POST"])
def add_rating():
	rating = request.form.get("rating")
	movie_id = request.form.get("movie")
	user_id = session.get("user_id")
	new_rating = Rating(user_id = user_id, movie_id = movie_id, 
		rating = rating)
	print(new_rating,"Rishabh")
	db.session.add(new_rating)
	db.session.commit()
	return redirect('/user-page/'+str(user_id))

if __name__ == "__main__":

    connect_to_db(app)
    app.run()