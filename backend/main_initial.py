from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import uuid

from flask_restful import Resource, Api

from celery import Celery
from redis import Redis

import datetime

from jwt_utils import jwt


#### SETTING UP DATABASE
import os

from models import *

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
# from sqlalchemy import Table, Column, Integer, String, ForeignKey, delete
 
current_dir = os.path.abspath(os.path.dirname(__file__))

from config import *

app = Flask(__name__)

##### SETTING UP JAVA WEB TOKEN
from flask_jwt_extended import JWTManager
app.config.from_object(Config)
jwt.init_app(app)
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(
  current_dir, "database.sqlite3")

from database import db
db.init_app(app)



# app.config.from_object(__name__)

# Import API routes from APIs.py
from APIs import api_routes

# Register API routes with app
app.register_blueprint(api_routes)


#configuring flask api
api = Api(app)
api.init_app(app)
   
# CORS(app, resources={r"/*": {"origins": "*"}})

# CORS(app, resources={r"/*":{'origins':"*"}})
# CORS(app, resources={r'/*':{'origins': 'http://localhost:8080',"allow_headers": "Access-Control-Allow-Origin"}})
CORS(app, resources={r"/*": {"origins": "*"}})

app.app_context().push()

engine = create_engine("sqlite:///./database.sqlite3")




# hello world route
@app.route('/', methods=['GET'])
def greetings():
    return("Hello, world!")

if __name__ == "__main__":
    app.run(debug=True)