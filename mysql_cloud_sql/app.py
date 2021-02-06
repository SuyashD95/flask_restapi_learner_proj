import os

from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api, Resource
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

    Handles the following requests at the following endpoints:
        1. GET  - Get all the members.
        2. POST - Create a new member.
    """
    pass
    def get(self):
        """Handles GET requests to the resource.

        Return code 200 along with a JSON response containing details
        about all the members stored in the database.

        Abort handling GET requests and return 404 if no members
        exist in the database along with an error message.
        """
        # records = db.session.query(Member).all()

        # Get all the Members
        # for record in records:
        # print(f'Name: {record.name}, Email: {record.email}')
        pass

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
    pass

records = db.session.query(Member).all()


# Get all the Members
for record in records:
    print(f'Name: {record.name}, Email: {record.email}')

if __name__ == '__main__':
    app.run(debug=True)
