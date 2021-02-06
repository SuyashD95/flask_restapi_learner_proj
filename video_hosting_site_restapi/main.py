from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# App Configuration
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Models for the Database
class VideoModel(db.Model):
    """Model class defined for the Video table."""

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Object representation of a record of VideoModel"""
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"


# Intializing Request Parser for PUT request on a Video resource
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video is required", required=True)

# Intializing Request Parser for PATCH request on a Video resource
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="New name of the video")
video_update_args.add_argument("views", type=int, help="New view count of the video")
video_update_args.add_argument("likes", type=int, help="New number of likes on the video")

# Resource fields to specify how objects needs to be serialized
resource_fields = {
    "_id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer
}


class Video(Resource):
    """Handles all requests related to the endpoint: /video/<int:video_id>"""

    @marshal_with(resource_fields)
    def get(self, video_id):
        """Handles the GET request and takes in a single URL paramter
        video_id which is an Integer.

        Return a dict giving information about a video with the given
        Video ID.
        """
        result = VideoModel.query.filter_by(_id=video_id).first()
        if not result:
            abort(404, message="Video with the given ID was not found...")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        """Handle PUT requests at the URL registered for
        the resource and creates a new video item into the
        database.

        Returns the response as a dict along with 201 HTTP
        status code (which denotes that a resource has been created').
        """
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(_id=video_id).first()

        if result:
            abort(409, message="Video ID already in use...")

        video = VideoModel(_id=video_id, name=args["name"], views=args["views"], likes=args["likes"])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        """Handles PATCH requests at the resource's specified endpoint
        and modifies the data of an existing record.

        Abort if no video with the given video ID exists in the database,
        returning a 404 error code along with an error message.

        Returns the response as a dict which will be serialized into JSON
        along with the 200 HTTP status code for a successful modification.
        """
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(_id=video_id).first()
        if not result:
            abort(404, message="Cannot update because video with the given ID not found...")

        # Modify the values of a record in the Video model.
        if args["name"]:
            result.name = args["name"]
        if args["views"]:
            result.views = args["views"]
        if args["likes"]:
            result.likes = args["likes"]

        db.session.add(result)
        db.session.commit()

        return result

    def delete(self, video_id):
        """Handle DELETE requests at the URL registered for
        the resource to delete a video with the specified video ID.

        Abort the operation if the given video doesn't exist
        and return 404 error code; otherwise return the 204 status
        code which represents that a resource has been successfully
        deleted.

        This function doesn't return any JSON serializable data back
        to the user in case of a success.
        """
        pass
        # abort_if_video_id_doesnt_exist(video_id)
        # del videos[video_id]
        # return '', 204


# Register resources and connect it to their respective URL endpoints
api.add_resource(Video, "/video/<int:video_id>")

# Run a local development server in debug mode.
if __name__ == "__main__":
    app.run(debug=True)
