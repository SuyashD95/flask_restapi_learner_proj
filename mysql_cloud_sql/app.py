import os

from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api, Resource, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

# Configure dotenv to read environment variables from .env file
load_dotenv(verbose=True)

# Initializing Flask app
app = Flask(__name__)
api = Api(app)

# Google Cloud SQL
DB_USER = os.getenv('DB_USER')
DB_USER_PWD = os.getenv('DB_USER_PWD')
DB_PUBLIC_IP_ADDRESS = os.getenv('DB_PUBLIC_IP_ADDRESS')
CONNECTION_NAME = os.getenv('CONNECTION_NAME')
DATABASE_NAME = os.getenv('DATABASE_NAME')

# SQLAlchemy Configuration

# Using the official MySQL Driver for Python (developed by Oracle), 
# mysqlconnector, to connect to the remote MySQL database 
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_USER_PWD}@{DB_PUBLIC_IP_ADDRESS}/{DATABASE_NAME}?unix_socket=/cloudsql/{CONNECTION_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Using AutoMap to utilize tables already existing in the database
# without the need to create our own Model classes.
Base = automap_base()
Base.prepare(db.engine, reflect=True)
Member = Base.classes.members

# NOTE: We can't use query direcly on the classes mapped to tables in
#       an existing database. To run queries, we need to use the
#       query(mapped_table) on the db.session object.


class MemberEntity(Resource):
    """Resource class to handle requests made to the 'members' table 
    in the database at the specified URLs:
        1. /members/all
        2. /members/new
        3. /members/delete

    Handles the following requests at the following endpoints:
        1. GET    - Get all the members.
        2. POST   - Create a new member.
        3. DELETE - Delete all the members.
    """
    
    def get(self):
        """Handles GET requests to the resource.

        Return code 200 along with a JSON response containing details
        about all the members stored in the database.

        Abort handling GET requests and return 404 if no members
        exist in the database along with an error message.
        """
        result = db.session.query(Member).all()

        if not result:
            abort(404, error_code=404, error_msg='No member exist in the database')

        members = {}
        for record in result:
            members[record._id] = {
                'name': record.name, 
                'email': record.email
            }

        return [members], 200

    def post(self):
        """Handles POST requests to the resource.

        Returns status code 201 with a JSON response containing information
        about the newly created member.

        Aborts the request if a member with the given ID already exists
        and return a 409 error with a message.
        """
        # Add a new member
        # new_member = Member(name="Vishy Anand", email="thevish@chess.com")
        # db.session.add(new_member)
        # db.session.commit()
        pass

    def delete(self):
        """Handles DELETE requests to the specified resource and returns
        status code 204 to signal that all the members have been
        successfully removed from the database.

        No additional content/data (like JSON) will be sent back to the user.

        Abort handling the request if no member exists in the database
        and return error code 404 with a message.
        """
        pass


class MemberRecord(Resource):
    """Resource class to handle requests made to a specific record
    of the 'members' table of the database at the specified URLs: 
        1. /members/{user_id}
        2. /members/{user_name}
    
    Handles the following requests at the following endpoints:
        
        1. GET    - Get a member by name.
        2. PATCH  - Update an existing member.
        3. PUT    - Overwriting an existing member and if it doesn't exist, 
                    create a new member at the specified ID.
        4. DELETE - Delete an existing member.
    """

    def get(self, user_name):
        """Handles GET requests to the resource and return HTTP code 200
        on a successful completion of a request.

        The given name should be identical to the name of the potential
        member that could exist in the database. This means that "Name"
        and "NaMe" are treated as two different values because their cases
        are different, even though they have the same value.

        Return a JSON response containing details about the specified user. 
        If multiple members with the same name exists, return with info
        only about the first matching member that was found.

        Abort handling GET requests and return 404 if no member with
        the specified name is found along with an error message.
        """
        record = db.session.query(Member).filter_by(name=user_name).first()

        if not record:
            abort(404, error_code=404, 
                error_msg='No member with the given name exists in the database.'
            )

        return record, 200

    def put(self, user_id):
        """Handles PUT requests at the specified URL and returns status
        code 200 if an already existing member has been overwritten 
        if no member exists with the given id, return code 201 to signal
        to the user that a new member has been created with the given ID.

        Along with the status code, return a JSON response with details
        about the new member (which has either replaced or have been newly
        created).
        """
        pass

    def patch(self, user_id):
        """Handles PATCH requests for the specified resource and returns
        status code 200 to signal that an existing member's information
        has been updated with the new values sent in by the user as JSON.

        Abort handling of the request if no existing member is found with
        the given ID and thus, return 404 along with an error message.
        """
        pass

    def delete(self):
        """Handles DELETE requests to the specified resource and returns
        status code 204 to signal that the member with the given ID has been
        successfully removed from the database.

        No additional content/data (like JSON) will be sent back to the user.

        Abort handling the request if no member with the given ID is found
        and return error code 404 with a message.
        """
        pass 


# Adding member table related resource to the API and specifying their endpoints
api.add_resource(MemberEntity, '/members/all', endpoint='get_all_members')
api.add_resource(MemberEntity, '/members/new', endpoint='create_new_member')
api.add_resource(MemberEntity, '/members/delete', endpoint='delete_all_members')
api.add_resource(MemberRecord, '/members/<string:user_name>', endpoint='get_member_by_name')
api.add_resource(MemberRecord, '/members/<int:user_id>/replace', endpoint='overwrite_existing_member')
api.add_resource(MemberRecord, '/members/<int:user_id>/update', endpoint='update_existing_member')
api.add_resource(MemberRecord, '/members/<int:user_id>/delete', endpoint='delete_existing_member')

if __name__ == '__main__':
    app.run(debug=True)
