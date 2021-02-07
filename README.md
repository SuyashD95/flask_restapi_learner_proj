# flask_restapi_learner_proj
Demo projects that I have created to learn about developing REST APIs using Flask_RESTful and Flask-SQLAlchemy frameworks.

## About Demo Projects

### 1. Hello World API
It is a very simple app intended to teach people the very basics of developing REST APIs using the Flask-RESTful framework.

### 2. Video Hosting Site API
It is an intermediate and more comprehensive app which utilizes a lot of features of the Flask-RESTful framework which are commonly used in real-world API development like Argument Parsing, Input Validation, Handling Bad/Invalid Requests as well as communicating with a data persistence layer, a SQLite3 database, with the help of Flask-SQLAlchemy.

### 3. MySQL Cloud SQL REST API (deployed using Google App Engine) available for general public use at https://treechat-303804.el.r.appspot.com/.
This is the most advanced as well as the most complicated project that I have created with the intention to get used to working with near real-world scenarios. I have used Flask-SQLAlchemy to connect to a MySQL database hosted remotely as a Cloud SQL instance on the Google Cloud Platform.

I have used automap feature of SQLAlchemy to work with the existing tables in the remote MySQL instance and have created 7 API endpoints in which I utilized the 5 most commonly used HTTP methods (GET, POST, PUT, PATCH, DELETE) as well as adopted best practices for input validation and error handling, returning the proper HTTP status codes and suitable error messages (as per W3C's guidelines).

All of my code, both the main.py which houses the code for the api as well as test.py which contains a series of unit tests to check the functionality of the various request handlers, are very well documented with proper comments and docstrings attached to every class and function. I have also exercised best practices while deploying the app to ensure that sensitive data is not exposed or compromised.

## Attribution
I have used **[Tech with Tim](https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg)'s** channel video on developing REST APIs titled **[ Python REST API Tutorial - Building a Flask REST API](https://www.youtube.com/watch?v=GMppyAPbLYk)**.

Apart from this, I would also like to take this opportunity to thank the developers responsible for developing and maintaining the **[Flask](https://flask.palletsprojects.com/en/1.1.x/), [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)** and **[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)** frameworks.
