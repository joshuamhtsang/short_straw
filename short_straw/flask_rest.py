from flask import Flask, request, jsonify, url_for
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import config_postgres as config_pg


app = Flask(__name__)

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://%s:%s@%s/%s' % \
    (
        config_pg.POSTGRES_USER,
        config_pg.POSTGRES_PW,
        config_pg.POSTGRES_URL,
        config_pg.POSTGRES_DB
     )
db = SQLAlchemy(app)

# Flask RESTful API
api = Api(app)

CORS(app)


# DB Models
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    choices = db.relationship('Choice', backref='owner_session')

    def __repr__(self):
        return '<Session %r>' % self.name


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    frequency = db.Column(db.Integer)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))

    def __repr__(self):
        return '<Choice %r>' % self.name


# Flask-API resources to interact with DB.
class SessionResource(Resource):
    # Get choices of a session.
    def get(self, session_id=None):
        if session_id is None:
            sessions = {}
            return sessions
        else:
            session = Session.query.filter_by(id=session_id).first()
            choices = session.choices
            return \
                {
                    "id": session.id,
                    "name": session.name,
                    "choices": str(choices)
                }, 200

    # Update the choices of a session.
    def put(self, session_id=None):
        if session_id is None:
            sessions = {}
            return sessions
        else:
            session = Session.query.filter_by(id=session_id).first()
            choice_name = request.args.get('choice_name')
            print(choice_name)
            new_choice = Choice(name=choice_name, owner_session=session)
            db.session.add(new_choice)
            db.session.commit()
        return None


class SessionListResource(Resource):
    # Get list of available sessions.
    def get(self):
        list = Session.query.all()
        name_list = [item.name for item in list]
        return name_list

    # Create a new session.
    # NOTE TO SELF: Needs to return the ID of the new session assigned by the
    # database
    def post(self):
        req_data = request.get_json()
        name = req_data["name"]
        choices = req_data["choices"]
        print(choices)

        # Create the new session in the DB and get the assigned ID.
        new_session = Session(name=name)
        db.session.add(new_session)
        db.session.flush()
        id = new_session.id
        print("The created session has id: ", id)
        db.session.commit()

        # Add choices to the new session.
        for choice in choices.split(','):
            choice_object = Choice(name=choice, owner_session=new_session)
            db.session.add(choice_object)
            db.session.commit()
        return id, 201


api.add_resource(SessionResource, '/sessions/<string:session_id>')
api.add_resource(SessionListResource, '/sessions')

if __name__ == "__main__":
    # Setup needed tables in database.
    db.create_all()

    # Creating a test session with 2 choices.
    josh_session = Session(name='my first session')
    db.session.add(josh_session)
    banana = Choice(name='Banana', owner_session=josh_session)
    apple = Choice(name='Apple', owner_session=josh_session)
    db.session.add(banana)
    db.session.add(apple)
    db.session.commit()

    # Retrieving the session created above and its related choices.
    some_session = Session.query.filter_by(
        name='my first session'
    ).first()
    print(some_session)
    print(some_session.id)
    print(some_session.choices)
    print(some_session.choices[0])
    print(some_session.choices[1])
    print(some_session.choices[0].name)
    print(some_session.choices[1].name)

    # Retrieval a list of all sessions.
    print(Session.query.all())

    # Run the Flask app.
    app.run(host="0.0.0.0", port="2828")
