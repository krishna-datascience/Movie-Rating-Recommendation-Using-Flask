from model import User, Rating, Movie, connect_to_db, db
from main import app


def create_user():
    email = input("Email : ").strip()
    password = input("Password :").strip()
    age = int(input("Age"))
    gender = input("Gender (M/F) : ").strip()
    zipcode = input("ZipCode : ").strip()

    new_user = User(email=email, password=password, age=age, zipcode=zipcode,gender=gender)
    db.session.add(new_user)
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    # add our test user
    if not User.query.filter_by(email="test@testing.com").first():
        eye = User(email="test@testing.com", password="test")
        db.session.add(eye)
        db.session.commit()

        # Toy Story
        r = Rating(user_id=eye.id, movie_id=1, rating=1)
        db.session.add(r)

        # Robocop 3
        r = Rating(user_id=eye.id, movie_id=1274, rating=5)
        db.session.add(r)

        # Judge Dredd
        r = Rating(user_id=eye.id, movie_id=373, rating=5)
        db.session.add(r)

        # 3 Ninjas
        r = Rating(user_id=eye.id, movie_id=314, rating=5)
        db.session.add(r)

        # Aladdin
        r = Rating(user_id=eye.id, movie_id=95, rating=1)
        db.session.add(r)

        # The Lion King
        r = Rating(user_id=eye.id, movie_id=71, rating=1)
        db.session.add(r)

        db.session.commit()

    # Add our user
    if not User.query.filter_by(email="user@testing.com").first():
        rohini = User(email="user@testing.com",
                       password="user",
                       age=42, gender='F',
                       zipcode="94114")
        db.session.add(rohini)
        db.session.commit()

        # Toy Story
        r = Rating(user_id=rohini.id, movie_id=1, rating=5)
        db.session.add(r)

        # Robocop 3
        r = Rating(user_id=rohini.id, movie_id=1274, rating=1)
        db.session.add(r)

        # Judge Dredd
        r = Rating(user_id=rohini.id, movie_id=373, rating=1)
        db.session.add(r)

        # 3 Ninjas
        r = Rating(user_id=rohini.id, movie_id=314, rating=1)
        db.session.add(r)

        # Aladdin
        r = Rating(user_id=rohini.id, movie_id=95, rating=5)
        db.session.add(r)

        # The Lion King
        r = Rating(user_id=rohini.id, movie_id=71, rating=5)
        db.session.add(r)

        db.session.commit()
    while True:
        print("Press 1 to add a new user: ")
        print("Press any other key to quit : ")
        n = input()
        if n == "1":
            create_user()
        else:
            break