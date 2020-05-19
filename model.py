"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict
import correlation


db = SQLAlchemy()


class User(db.Model):

	__tablename__ = "users"

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	email = db.Column(db.String(64), nullable=True)
	password = db.Column(db.String(64), nullable=True)
	age = db.Column(db.Integer, nullable=True)
	gender = db.Column(db.String(10), nullable=True)
	zipcode = db.Column(db.String(15), nullable=True)

	def __str__(self):

		return "User id: {} Age: {}".format(self.id,self.age)

	def predict_rating(self, movie):
		"""Predict user's rating of a movie."""

		UserMovies = db.aliased(Rating)
		MovieUsers = db.aliased(Rating)

		query = (db.session.query(Rating.user_id, Rating.rating, UserMovies.rating, MovieUsers.rating)
			.join(UserMovies, UserMovies.movie_id == Rating.movie_id)
			.join(MovieUsers, Rating.user_id == MovieUsers.user_id)
			.filter(UserMovies.user_id == self.id)
			.filter(MovieUsers.movie_id == movie.id))

		known_ratings = {}
		paired_ratings = defaultdict(list)

		for rating_user_id, rating_rating, user_movie_rating, movie_user_rating in query:
			paired_ratings[rating_user_id].append((user_movie_rating, rating_rating))
			known_ratings[rating_user_id] = movie_user_rating

		similarities = []

		for _id, rating in known_ratings.items():
			similarity = correlation.pearson(paired_ratings[_id])
			if similarity > 0:
				similarities.append((similarity, rating))

		if not similarities:
			return None

		numerator = sum([rating * sim for sim, rating in similarities])
		denominator = sum([sim for sim, rating in similarities])

		return numerator / denominator

class Movie(db.Model):
	"""Movie info in rating website."""

	__tablename__= "movies"

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	title = db.Column(db.String(64))
	release_date = db.Column(db.DateTime)
	imdb_url = db.Column(db.String(200))

	def __str__(self):

		return "Movie Id: {} Title: {}".format(self.id,self.title)

class Rating(db.Model):
	"""Rating information in ratings website."""

	__tablename__= "ratings"

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
	movie_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	rating = db.Column(db.Integer)
	timestamp = db.Column(db.String(20),nullable=True)

	#Define relationship to user
	user = db.relationship("User", backref=db.backref("ratings", order_by=id))

	#Define relationship to movie
	movie = db.relationship("Movie",backref=db.backref("ratings", order_by=id))

	def __str__(self):
		return "Rating id={} movie_id={} user_id={}".format(self.id,
			self.user_id,self.movie_id)

def connect_to_db(app):
	"""Connect the database to our Flask app."""
	# Configure to use our SQLite database
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ratings.db'
	db.app = app
	db.init_app(app)
	db.create_all()


if __name__ == "__main__":
	# As a convenience, if we run this module interactively, it will leave
	# you in a state of being able to work with the database directly.
	from main import app
	connect_to_db(app)
	print ("Connected to DB.")