from flask import Flask, request, jsonify, url_for
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://admin:admin@127.0.0.1:5432/shortstraw'
db = SQLAlchemy(app)

# Flask RESTful API
api = Api(app)

CORS(app)


sessions = {}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    choices = db.Column(db.ARRAY(db.String()))

    def __repr__(self):
        return '<Session %r>' % self.name


class ShortStraw(Resource):
    def get(self, session_id=None):
        if session_id == None:
            return sessions
        else:
            return {session_id: sessions[session_id]}, 200

    def put(self, session_id):
        req_data = request.get_json()
        choices = req_data["choices"]
        sessions[session_id] = choices
        return {session_id: sessions[session_id]}, 201


api.add_resource(ShortStraw, '/session/<string:session_id>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="2828")

    db.create_all()

    josh_session = Session(
        name='my first session!',
        choices=''
    )

    db.session.add(josh_session)

    db.session.commit()

