from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

names = {
    "tim": {
        "age": 19,
        "gender": "male"
    },
    "suyash": {
        "age": 25,
        "gender": "male"
    },
    "sonal": {
        "age": 25,
        "gender": "female"
    }
}


class HelloWorld(Resource):

    def get(self, name):
        """Handle GET requests at the URL registered for
        the resource.

        The name is a URL argument passed as a String.

        Returns the response as a dict (formatted
        as a JSON object) because it support serialization i.e.,
        conversion of an object into a sequence of bits/byte stream.
        """
        return names[name]

    def post(self):
        """Handle POST requests at the URL registered for
        the resource. Returns the response as a dict.
        """
        return {"data": "Posted"}


api.add_resource(HelloWorld, "/helloworld/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)
