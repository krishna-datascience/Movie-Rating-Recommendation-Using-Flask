This is a Movie Rating flask Application

Steps:

1. Goto Command prompt to this folder location and then run
	pip install -r requirements.txt

2. python model.py (To setup your database file)

3. python seed.py (To Fill values in the databse)

You can skip step 2 & 3 as the ratings.db file is already populated with data. You may edit data in the seed_data folder, post that delete the ratings.db file and then run step 2 & 3.

seed_data folder:
	* u.data -> Ratings
	* u.item -> Movie List
	* u.user -> User list
	
If you choose to have a new data field, edit the code accordingly.

4. python feed_data.py (To add additional users to your database)
	This will create two users for testing:
	* First User - user-name = test@testing.com | pass = test
	* Second User - user-name = user@testing.com | pass = user

5. python main.py (To run your application)

-------------------------------------------------------------------------------------------------------------------------------------------
For More Project Visit : https://github.com/krishna-datascience