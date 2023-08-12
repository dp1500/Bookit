from database import db
from flask_login import UserMixin
from flask_login import login_user
from flask_login import LoginManager
from datetime import datetime


# from sqlalchemy.ext.declarative import declarative_base
# from flask_sqlalchemy import SQLAlchemy

# engine = None
# Base = declarative_base()
# db = SQLAlchemy()

login_manager = LoginManager()

# @login_manager.user_loader
# def load_user(user_id):
#   return users.query.get(int(user_id))

@login_manager.user_loader 
def load_user(user):
  return Users.query.get(int(user))


class Users(db.Model, UserMixin):
  __tablename__ = 'users'
  user_id = db.Column(db.Integer, autoincrement = True, primary_key = True, unique = True, nullable = False)
  username = db.Column(db.String, unique = True, nullable = False)
  name = db.Column(db.String)
  email = db.Column(db.String)
  password = db.Column(db.String)
  role = db.Column(db.String)
  # profile_pic_url = db.Column(db.String)
  last_activity = db.Column(db.DateTime, default=datetime.utcnow)
  
  def get_id(self):
           return (self.Uid)

class Theatres(db.Model, UserMixin):
  __tablename__ = 'theatres'
  # __table_args__ = {'extend_existing': True}
  theatre_id = db.Column(db.Integer, autoincrement = True, primary_key = True, unique = True, nullable = False)
  # username = db.Column(db.String, unique = True, nullable = False)
  theatre_name = db.Column(db.String, unique = True)

  user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

  city = db.Column(db.String)
  address = db.Column(db.String)
  capacity = db.Column(db.Integer)
  screens = db.Column(db.Integer)

  theatre_shows = db.relationship('Shows', backref='theatres')


class Movies(db.Model):
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
    movie_name = db.Column(db.String)
    description = db.Column(db.String)

    releaseDate = db.Column(db.String)
    
    total_rating = db.Column(db.Integer)
    number_of_ratings = db.Column(db.Integer)

    rating = db.Column(db.Float)

    genres = db.Column(db.String)  # Storing genres as a comma-separated string

    image_url = db.Column(db.String)

    likes = db.Column(db.Integer)
    n_comments = db.Column(db.Integer)


class Shows(db.Model):
    __tablename__ = 'shows'
    show_id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatres.theatre_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)

    show_capacity = db.Column(db.Integer)
    seats_booked = db.Column(db.Integer)
    seats_left = db.Column(db.Integer)


    timing = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)

    screenNumber = db.Column(db.Integer)
    
    ticket_price = db.Column(db.Float)

  
class Screens(db.Model):
  
  __tablename__ = 'screens'
  screen_id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
    
  theatre_id = db.Column(db.Integer, nullable=False)
    # theatre = db.relationship('Theatres', backref=db.backref('screens', lazy=True))

  capacity = db.Column(db.Integer)

  screenNumber = db.Column(db.Integer)

from sqlalchemy.ext.declarative import DeclarativeMeta
from flask import json
  
class Bookings(db.Model, UserMixin):
  __tablename__ = 'bookings'
  booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  show_id = db.Column(db.Integer, db.ForeignKey('shows.show_id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
  booking_date = db.Column(db.Date, nullable=False)
  ticket_count = db.Column(db.Integer, nullable=False)
  total_price = db.Column(db.Float, nullable=False)

  def __repr__(self):
    return f"<Booking {self.booking_id}>"
  
  def to_dict(self):
    # Convert the model instance into a dictionary
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}
  
  # Add a method to convert the dictionary to JSON
  def to_json(self):
    # return json.dumps(self.to_dict())
    
    return self.to_dict()








    
    