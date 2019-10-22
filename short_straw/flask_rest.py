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


class ShortStraw(Resource):
    def get(self, session_id=None):
        if session_id == None:
            sessions = {}
            return sessions
        else:
            session = Session.query.filter_by(id=session_id).first()
            return \
                {
                    "id": session.id,
                    "name": session.name,
                    "choices": session.choices
                }, 200

    def put(self, session_id):
        req_data = request.get_json()
        id = session_id
        name = req_data["name"]
        choices = req_data["choices"]
        new_session = Session(
            id=id,
            name=name
        )
        db.session.add(new_session)
        db.session.commit()
        for choice in choices:
            choice_object = Choice(
                name=choice,
                owner_session=new_session
            )
            db.session.add(choice_object)
            db.session.commit()
        return True, 201


api.add_resource(ShortStraw, '/session/<string:session_id>')

if __name__ == "__main__":
    # Setup needed tables in database.
    db.create_all()

    josh_session = Session(name='my first session')
    db.session.add(josh_session)
    db.session.commit()
    banana = Choice(name='Banana', owner_session=josh_session)
    db.session.add(josh_session)
    db.session.commit()

    # Run the Flask app.
    app.run(host="0.0.0.0", port="2828")



