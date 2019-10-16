# short_straw
A flask-based API to simulate the age old tradition of drawing straws!

# How to run

$ pip3 install -r requirements.txt

$ python3 flask_rest.py

# Example requests

Create a new session called 'my_first_session' with 3 choices: Apple, Orange and Banana: 

$ curl --header "Content-Type: application/json" --request PUT --data '{"choices":["Apple","Orange","Banana"]}' localhost:2828/session/my_first_session

This creates a 'resource'.  You can now retrieve that session resource:

$ curl --header "Content-Type: application/json" --request GET  localhost:2828/session/my_first_session

# Running the postgres database

$ docker-compose -f postgres.yml up

The tables in the database can be made by running the 'db.create_all()' function
in flask_rest.py.