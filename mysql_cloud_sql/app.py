import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

# Configure dotenv to read environment variables from .env file
load_dotenv(verbose=True)

# Initializing Flask app
app = Flask(__name__)

# Google Cloud SQL
DB_USER = os.getenv('DB_USER')
DB_USER_PWD = os.getenv('DB_USER_PWD')
DB_PUBLIC_IP_ADDRESS = os.getenv('DB_PUBLIC_IP_ADDRESS')
CONNECTION_NAME = os.getenv('CONNECTION_NAME')
DATABASE_NAME = os.getenv('DATABASE_NAME')

# SQLAlchemy Configuration

# To use mysqlconnector as the MySQL Driver, we need to install it using pip
# and executing the following command in the terminal:
# pip install mysql-connector-python

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_USER_PWD}@{DB_PUBLIC_IP_ADDRESS}/{DATABASE_NAME}?unix_socket=/cloudsql/{CONNECTION_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)
Member = Base.classes.members

# Add a new member
# new_member = Member(name="Vishy Anand", email="thevish@chess.com")
# db.session.add(new_member)
# db.session.commit()

# NOTE: We can't use query direcly on the classes mapped to tables in
# an existing database. To run queries, we need to use the query(mapped_table)
# on the db.session object.
records = db.session.query(Member).all()

# Get all the Members
for record in records:
    print(f'Name: {record.name}, Email: {record.email}')

if __name__ == '__main__':
    app.run(debug=True)
