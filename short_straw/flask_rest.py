from flask import Flask, request, jsonify, url_for
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)


sessions = {}


class ShortStraw(Resource):
    def get(self, session_id):
        return {session_id: sessions[session_id]}

    def put(self, session_id):
        req_data = request.get_json()
        choices = req_data["choices"]
        sessions[session_id] = choices
        return {session_id: sessions[session_id]}


api.add_resource(ShortStraw, '/<string:session_id>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="2828")