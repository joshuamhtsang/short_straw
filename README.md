# short_straw
A flask-based API to simulate the age old tradition of drawing straws!

# How to run

$ pip3 install -r requirements.txt

$ python3 flask_rest.py

# Example requests

Create a new session with name 'my_first_session' with 3 choices: Apple, Orange and Banana: 

$ curl --header "Content-Type: application/json" --request POST --data '{"name":"my_first_session","choices":"Apple,Orange,Banana"}' localhost:2828/sessions

The session will be created with a dynamically assigned ID in the database. To retrieve that session, you need to
know its ID (session_id):

$ curl --header "Content-Type: application/json" --request GET localhost:2828/sessions/<session_id>

To get a full list of all created sessions:

$ curl --header "Content-Type: application/json" --request GET localhost:2828/sessions

# Running the postgres database

$ docker-compose -f postgres.yml up

The tables in the database can be made by running the 'db.create_all()' function
in flask_rest.py.