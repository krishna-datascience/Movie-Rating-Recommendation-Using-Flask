from datetime import datetime
import csv
from model import User, Rating, Movie, connect_to_db, db
from main import app

def load_users():
	"""Load users from u.user into database."""

	with open('seed_data/u.user', 'r') as f:
		reader = csv.reader(f, delimiter='|')
		for row in reader:
			new_user = User(id = row[0], age = row[1], gender = row[2], zipcode = row[4])
			db.session.add(new_user)
		db.session.commit()


def load_movies():
	"""Load movies from u.item into database."""

	with open('seed_data/u.item', 'r') as f:
		reader = csv.reader(f, delimiter='|')
		for row in reader:
			if row[2]:
				d = datetime.strptime(row[2], "%d-%b-%Y")
				d = d.date()
			new_movie = Movie(id = row[0], title = row[1], release_date = d, imdb_url = row[4])
			db.session.add(new_movie)
		db.session.commit()

def load_ratings():
	"""Load ratings from u.data into database."""
	with open('seed_data/u.data', 'r') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			new_rating = Rating(user_id = row[0], movie_id = row[1], rating = row[2], timestamp = row[3])
			db.session.add(new_rating)
		db.session.commit()

if __name__ == "__main__":
	connect_to_db(app)
	load_users()
	load_movies()
	load_ratings()
