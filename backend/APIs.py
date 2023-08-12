from flask_restful import Resource, fields, marshal_with,reqparse, Api
from flask import jsonify, url_for
from models import *
from database import db
from validation import *
from flask import request, Blueprint
from sqlalchemy import desc , select, join

# from flask_jwt_extended import create_access_token, JWTManager, jwt_required
from jwt_utils import jwt
from flask_jwt_extended import jwt_required, get_jwt_identity

from flask_jwt_extended import create_access_token

import os

from extensions import cache

# Create blueprint for API routes
api_routes = Blueprint('api', __name__)
api = Api(api_routes)

# from getImage import *

# from werkzeug.utils import secure_filename
# import os


# #configuring path and constraint to save images
# UPLOAD_FOLDER = 'static\images'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# def allowed_file(filename):
#   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# parser for updating profile data
profile_parser = reqparse.RequestParser()
profile_parser.add_argument('name')
profile_parser.add_argument('username')
profile_parser.add_argument('about')
profile_parser.add_argument('old_password')
profile_parser.add_argument('new_password')
profile_parser.add_argument('file')

profile_parser.add_argument('password')

# from config import create_cache
# from flask import Flask
# app = Flask(__name__)
# cache = create_cache(app)

# from main import cache

#creating api for login
class Login(Resource):
    def post(self):
        
        username = request.json.get('username')
        password = request.json.get('password')

        user = Users.query.filter_by(username=username).first()

        if user == None:
            response = jsonify(error='Username Does Not Exist')
            response.status_code = 409  # HTTP status code for conflict
            return response
        
        elif user.password != password:
            response = jsonify(error='Invalid credentials')
            response.status_code = 401  # HTTP status code for conflict
            return response
        
        elif user.password == password:
            access_token = create_access_token(identity=username)

            #update last activity time so that celery can notify the user by sending email, to open app
            user.last_activity = datetime.utcnow()
            db.session.commit()
            
            return {'access_token': access_token}, 200


# api to login using token based authentication
api.add_resource(Login, '/api/login')


#api for login out that deletes the cookie (token)
class LogoutAPI(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        
        # Get the user from the database
        user = Users.query.filter_by(username=current_user).first() 

        if not user:
            return {'message': 'User not found'}, 404

        # Update the last online timestamp
        user.last_online = datetime.now()
        db.session.commit()

        return {'message': 'Logout successful'}
    
api.add_resource(LogoutAPI, "/api/logout","/api/logout/<string:Uid>")



# ////////////////////////  Code for generating amdin page stats //////////////
import matplotlib.pyplot as plt
from sqlalchemy import func, extract

from matplotlib import pyplot as plt

class AdminHomePageStats(Resource):

    @jwt_required() 
    def get(self):
        # Get current user
        current_user = get_jwt_identity()

        # Find the user in the database
        user = Users.query.filter_by(username=current_user).first()

        if user and user.role == 'admin':
            # Top theatre in terms of revenue
            top_theatre_revenue = db.session.query(
                Theatres.theatre_name, func.sum(Bookings.total_price).label('revenue')
            ).join(
                Shows, Theatres.theatre_id == Shows.theatre_id
            ).join(
                Bookings, Shows.show_id == Bookings.show_id
            ).filter(
                Theatres.user_id == user.user_id
            ).group_by(
                Theatres.theatre_name
            ).order_by(
                desc('revenue')
            ).first()

            if top_theatre_revenue:
                top_theatre_revenue = {"theatre_name": top_theatre_revenue[0], "revenue": float(top_theatre_revenue[1])}

            # Total bookings
            total_bookings = db.session.query(
                func.count(Bookings.booking_id)
            ).join(
                Shows, Bookings.show_id == Shows.show_id
            ).join(
                Theatres, Shows.theatre_id == Theatres.theatre_id
            ).filter(
                Theatres.user_id == user.user_id
            ).scalar()

            # Total revenue
            total_revenue = db.session.query(
                func.sum(Bookings.total_price)
            ).join(
                Shows, Bookings.show_id == Shows.show_id
            ).join(
                Theatres, Shows.theatre_id == Theatres.theatre_id
            ).filter(
                Theatres.user_id == user.user_id
            ).scalar()

            # Top theatre in terms of bookings
            top_theatre_bookings = db.session.query(
                Theatres.theatre_name, func.count(Bookings.booking_id).label('bookings_count')
            ).join(
                Shows, Theatres.theatre_id == Shows.theatre_id
            ).join(
                Bookings, Shows.show_id == Bookings.show_id
            ).filter(
                Theatres.user_id == user.user_id
            ).group_by(
                Theatres.theatre_name
            ).order_by(
                desc('bookings_count')
            ).first()

            if top_theatre_bookings:
                top_theatre_bookings = {"theatre_name": top_theatre_bookings[0], "bookings_count": top_theatre_bookings[1]}

            # New statistic calculations:
            # Revenue per theatre
            revenue_per_theatre = db.session.query(
                Theatres.theatre_name, func.sum(Bookings.total_price).label('revenue')
            ).join(
                Shows, Theatres.theatre_id == Shows.theatre_id
            ).join(
                Bookings, Shows.show_id == Bookings.show_id
            ).filter(
                Theatres.user_id == user.user_id
            ).group_by(
                Theatres.theatre_name
            ).all()

            # Revenue per month
            revenue_per_month = db.session.query(
                extract('month', Bookings.booking_date).label('month'),
                func.sum(Bookings.total_price).label('revenue')
            ).join(
                Shows, Bookings.show_id == Shows.show_id
            ).join(
                Theatres, Shows.theatre_id == Theatres.theatre_id
            ).filter(
                Theatres.user_id == user.user_id
            ).group_by(
                'month'
            ).order_by(
                'month'
            ).all()

            fig, ax = plt.subplots(figsize=(6, 4))  # Adjust the size as needed
            
             # Pie chart
            theatre_names = [row.theatre_name for row in revenue_per_theatre]
            revenues = [row.revenue for row in revenue_per_theatre]
            plt.figure(figsize=(5, 5))
            plt.pie(revenues, labels=theatre_names, autopct='%1.1f%%')
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.title('Revenue per Theatre')
            plt.savefig('static/charts/revenue_per_theatre.png')
            
            # Bar chart
            months = [row.month for row in revenue_per_month]
            monthly_revenues = [row.revenue for row in revenue_per_month]
            plt.figure(figsize=(5, 5))
            plt.bar(months, monthly_revenues)
            plt.title('Revenue per Month')
            plt.xlabel('Month')
            plt.ylabel('Revenue')
            plt.savefig('static/charts/revenue_per_month.png')

            return {
                'topTheatreRevenue': top_theatre_revenue,
                'totalBookings': total_bookings,
                'totalRevenue': total_revenue,
                'topTheatreBookings': top_theatre_bookings,
                'revenuePerTheatre': [row._asdict() for row in revenue_per_theatre],
                'revenuePerMonth': [row._asdict() for row in revenue_per_month],
                'revenuePerTheatreChart': request.url_root[:-1] + '/static/charts/revenue_per_theatre.png',
                'revenuePerMonthChart': request.url_root[:-1] + '/static/charts/revenue_per_month.png',
        }, 200

        else:
            return {'message': 'User not found or not authorized.'}, 400


api.add_resource(AdminHomePageStats, "/api/admin-home-page-stats","/api/admin-home-page-stats/<string:Uid>")

# /////////////////////////////////////////////////// code end for stats /////////////////////

class ProfileDataApi(Resource):
    
    @jwt_required()
    def get(self):
        
        current_user = get_jwt_identity()
        print(current_user)
        
        # update_followers_AND_following_count(Uid)

        user = Users.query.filter_by(username=current_user).first() 

        if user:
            response = { "user_id": user.user_id, "name": user.name, "username": user.username}
            # not sending password to the client for secuirty reasons

            return jsonify(response)
        else:
            response = jsonify(error='Username Does Not Exist')
            response.status_code = 409  # HTTP status code for conflict
            return response

    def post(self):

        name = request.json.get('name')
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        role = request.json.get('role')


        last_activity = datetime.utcnow()
        
        username_exists = Users.query.filter_by(username=username).first()


        if username_exists:
            response = jsonify(error='Username already exists')
            response.status_code = 409  # HTTP status code for conflict
            return response

        else:
            if role:
                # If role data is present
                new_user = Users(username=username, name=name, password=password, email=email, last_activity=last_activity, role=role)
            else:
                # If role data is not present, assign "user" as the role
                new_user = Users(username=username, name=name, password=password, email=email, last_activity=last_activity, role="user")
            
            # new_user = Users(username=username, name=name, password = password, email = email,last_activity = last_activity, role = role)
            db.session.add(new_user)
            db.session.commit()

            return 200

    @jwt_required()
    def put(self):
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username=current_user).first()

        if not user:
            return {'error': 'User not found'}, 404
        
        # Fetch data from request
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400

        # Get the data from the request
        name = data.get('name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        new_password = data.get('new_password')
        
        # Check if the current password matches
        if password != user.password:
                return {'message': 'Invalid current password'}, 405
        
        
        # Update the user's profile
        if name:
            user.name = name
        if username:
            user.username = username
        if email:
            user.email = email
        if new_password:
            user.password = new_password 
        
        db.session.commit()

        return {'message': 'Profile updated successfully'}, 200
        
api.add_resource(ProfileDataApi, "/api/ProfileData","/api/ProfileData/<string:Uid>")

class TheatreDataApi(Resource):
    
    @jwt_required()
    def get(self, theatre_id=None):  # Add theatre_id parameter
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username=current_user).first()

        if theatre_id:  # If theatre_id is provided, return a single theatre
            theatre = Theatres.query.filter_by(user_id=user.user_id, theatre_id=theatre_id).first()
            if theatre is None:
                return {"message": "Theatre not found"}, 404

            result = {
                'theatre_id': theatre.theatre_id,
                'theatre_name': theatre.theatre_name,
                'city': theatre.city,
                'address': theatre.address,
                'screens': theatre.screens
            }
            return jsonify(result)
        
        # Otherwise, return all theatres
        theatres = Theatres.query.filter_by(user_id=user.user_id).all()
        result = []
        for theatre in theatres:
            result.append({
                'theatre_id': theatre.theatre_id,
                'theatre_name': theatre.theatre_name,
                'city': theatre.city,
                'address': theatre.address,
                'screens': theatre.screens
            })
        return jsonify(result)

    # @jwt_required()
    # def get(self):
    #     # bhai kaaam k
    #     # har jagah jwt pe user id se authenticate ho
    #     print("appi called")
    #     current_user = get_jwt_identity()
    #     print("level 2")
    #     user = Users.query.filter_by(username=current_user).first() 
    #     print("level 3")
    #     theatres = Theatres.query.filter_by(user_id=user.user_id).all()
    #     result = []
    #     print("level 4")
    #     for theatre in theatres:
    #         result.append({
    #             'theatre_id': theatre.theatre_id,
    #             'theatre_name': theatre.theatre_name,
    #             'city': theatre.city,
    #             'address': theatre.address,
    #             'screens': theatre.screens
    #         })
    #     print("level 5")
    #     return jsonify(result)

    @jwt_required()
    def post(self):

        
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username=current_user).first() 
        
        if user.role != 'admin':
            return 401

        theatreName = request.json.get('theatreName')
        capacity = request.json.get('capacity')
        city = request.json.get('city')
        address = request.json.get('address')
        screens = request.json.get('screens')
        screenCapacities = request.json.get('screenCapacities')  # New: Get screenCapacities from the request JSON
        # role = request.json.get('role')

        print(theatreName)

        
        theatre_exists = Theatres.query.filter_by(theatre_name=theatreName).first()


        if theatre_exists:
            response = jsonify(error='Theatre already exists')
            response.status_code = 409  # HTTP status code for conflict
            return response

        else:
            new_theatre = Theatres(theatre_name=theatreName, capacity=capacity, city=city, address=address, screens=screens, user_id = user.user_id)
            
            
            # new_user = Users(username=username, name=name, password = password, email = email,last_activity = last_activity, role = role)
            db.session.add(new_theatre)
            db.session.commit()

            # Get the generated theatre_id
            theatre_id = new_theatre.theatre_id

            # Add screens to the screens database with the corresponding theatre_id
            for index, screenCapacity in enumerate(screenCapacities):
                new_screen = Screens(
                    theatre_id=theatre_id,
                    capacity=screenCapacity,
                    screenNumber=index + 1,
                )
                db.session.add(new_screen)

            db.session.commit()

            return 200
    
    @jwt_required()
    def put(self, theatre_id):
        # get the identity of current user
        current_user = get_jwt_identity()
        # retrieve the user from the Users table
        user = Users.query.filter_by(username=current_user).first()

        # only allow admins to update theatre data
        if user.role != 'admin':
            return {"message": "Unauthorized access"}, 401

        # retrieve the theatre to be updated
        theatre = Theatres.query.filter_by(theatre_id=theatre_id, user_id=user.user_id).first()

        if theatre is None:
            return {"message": "Theatre not found"}, 404

        # get the data from the request
        theatreName = request.json.get('theatreName')
        capacity = request.json.get('capacity')
        city = request.json.get('city')
        address = request.json.get('address')
        screens = request.json.get('screens')
        screenCapacities = request.json.get('screenCapacities')

        # update the theatre data
        theatre.theatre_name = theatreName
        theatre.capacity = capacity
        theatre.city = city
        theatre.address = address
        theatre.screens = screens

        # update the screen capacities
        for index, screenCapacity in enumerate(screenCapacities):
            screen = Screens.query.filter_by(theatre_id=theatre_id, screenNumber=index + 1).first()
            if screen is not None:
                screen.capacity = screenCapacity
            else:
                # If screen does not exist, create a new one
                new_screen = Screens(
                    theatre_id=theatre_id,
                    capacity=screenCapacity,
                    screenNumber=index + 1,
                )
                db.session.add(new_screen)

        # Remove extra screens if the count is decreased
        extra_screens = Screens.query.filter(Screens.theatre_id == theatre_id, Screens.screenNumber > screens).all()
        for screen in extra_screens:
            # Delete future shows related to the screen to be deleted
            future_shows = Shows.query.filter(Shows.screenNumber == screen.screenNumber, Shows.theatre_id == theatre_id, Shows.date >= datetime.now()).all()
            for show in future_shows:
                db.session.delete(show)

            # Delete the screen
            db.session.delete(screen)

        # commit the changes to the database
        db.session.commit()

        return {"message": "Theatre data updated successfully"}, 200
    
    @jwt_required()
    def delete(self, theatre_id):
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username=current_user).first()
        
        if user.role != 'admin':
            return {"message": "Unauthorized access"}, 401

        theatre = Theatres.query.filter_by(theatre_id=theatre_id, user_id=user.user_id).first()

        if theatre is None:
            return {"message": "Theatre not found"}, 404

        # Delete all the screens associated with the theatre
        screens = Screens.query.filter_by(theatre_id=theatre_id).all()
        for screen in screens:
            db.session.delete(screen)

        # Delete all the future shows from the shows database associated with the theatre
        current_date = datetime.now().date()
        shows = Shows.query.filter(Shows.theatre_id == theatre_id, Shows.date >= current_date).all()
        for show in shows:
            db.session.delete(show)

        # Delete the theatre
        db.session.delete(theatre)
        db.session.commit()

        return {"message": "Theatre deleted successfully"}, 200

        
api.add_resource(TheatreDataApi, "/api/TheatreData","/api/TheatreData/<int:theatre_id>")

#    ///////////////// 2 additional APIs for DisplayShows page ////////

class UsersTheatreDataApi(Resource):
    
    # @jwt_required()
    def get(self, theatre_id=None):  # Add theatre_id parameter
        # current_user = get_jwt_identity()
        # user = Users.query.filter_by(username=current_user).first()

        if theatre_id:  # If theatre_id is provided, return a single theatre
            theatre = Theatres.query.filter_by(theatre_id=theatre_id).first()
            if theatre is None:
                return {"message": "Theatre not found"}, 404

            result = {
                'theatre_id': theatre.theatre_id,
                'theatre_name': theatre.theatre_name,
                'city': theatre.city,
                'address': theatre.address,
                'screens': theatre.screens
            }
            return jsonify(result)
        
        # Otherwise, return all theatres
        theatres = Theatres.query.filter_by().all()
        result = []
        for theatre in theatres:
            result.append({
                'theatre_id': theatre.theatre_id,
                'theatre_name': theatre.theatre_name,
                'city': theatre.city,
                'address': theatre.address,
                'screens': theatre.screens
            })
        return jsonify(result)

api.add_resource(UsersTheatreDataApi, "/api/UserTheatreData","/api/UserTheatreData/<int:theatre_id>")

class UserMovieDataApi(Resource):
        
    # @jwt_required()
        def get(self, movie_id):

            movie = Movies.query.filter_by(movie_id=movie_id).first()

            
            # If the movie doesn't exist, return a 404 error
            if movie is None:
                return {"message": "Movie not found"}, 404
            
            # if movie.number_of_ratings == None:
            #     movie.number_of_ratings = 0
                
           
            if movie.rating == None:
                movie.rating = 0

            movie_info = {
                'movie_id': movie.movie_id,
                    'movie_name': movie.movie_name,
                    'description': movie.description,
                    'releaseDate': movie.releaseDate,
                    'rating': movie.rating,
                    'genres': movie.genres,
                    'image_url': movie.image_url,
                    'likes': movie.likes,
                    'n_comments': movie.n_comments
            }
            # return jsonify(movie_info)
            return movie_info

api.add_resource(UserMovieDataApi, "/api/UserMovieData/<int:movie_id>")


# ///////////////////////// API to get theatres list for theatre display page /////////////////
class TheatresInCityApi(Resource):

    
    def get(self, city=None):
        
        # user = Users.query.filter_by(username=current_user).first()

        if city:
            theatres = Theatres.query.filter_by(city=city).all()
            result = []
            for theatre in theatres:
                result.append({
                    'theatre_id': theatre.theatre_id,
                    'theatre_name': theatre.theatre_name,
                    'city': theatre.city,
                    'address': theatre.address,
                    'screens': theatre.screens
                })
            return jsonify(result)

        return {"message": "Please specify a city."}, 400

api.add_resource(TheatresInCityApi, "/api/TheatresInCity/<string:city>")


from datetime import datetime

class TheatresShowsApi(Resource):
    def get(self, movie_id, city, date):
        theatres = Theatres.query.filter_by(city=city).all()
        result = []
        for theatre in theatres:
            # Convert the date string to a datetime object
            show_date = datetime.strptime(date, '%Y-%m-%d').date()
            shows = Shows.query.filter_by(theatre_id=theatre.theatre_id, movie_id=movie_id, date=show_date).all()
            if shows:  # Only include theatres that have shows of the movie
                theatre_data = {
                    'theatre_id': theatre.theatre_id,
                    'theatre_name': theatre.theatre_name,
                    'city': theatre.city,
                    'address': theatre.address,
                    'screens': theatre.screens,
                    'shows': []
                }
                for show in shows:
                    show_data = {
                        'timing': show.timing,
                        'date': show.date,
                        'ticket_price': show.ticket_price,
                        'screenNumber': show.screenNumber,
                        'show_capacity': show.show_capacity,
                        'seats_left': show.seats_left,
                        'show_id': show.show_id
                    }
                    theatre_data['shows'].append(show_data)
                result.append(theatre_data)
        return jsonify(result)

api.add_resource(TheatresShowsApi, "/api/TheatresShowsApi/<int:movie_id>/<string:city>/<string:date>")



    # @jwt_required()
    # def put(self):
    #     current_user = get_jwt_identity()
        
    #     user = Users.query.filter_by(username=current_user).first() 

    #     if user:

    #         name = request.form.get('name')
    #         username = request.form.get('username')
    #         email = request.form.get('email')
    #         about = request.form.get('about')
    #         new_password = request.form.get('new_password')
    #         old_password = request.form.get('old_password')
    #         image_file = request.files.get('file')

    #         if name == None or username == None or email == None or old_password == None:
    #             raise BusinessValidationError(status_code= 400, error_code=	"input missing", error_message= "input missing")

    #         if old_password == user.password:

    #             if name != 'null':
    #                 user.name = name
    #             if username != 'null':
    #                 user.username = username
    #             if email != 'null':
    #                 user.email = email
    #             if about != 'null':
    #                 user.about = about
                
    #             if image_file is not None:

    #                 # save the file to a folder on the server
    #                 file_path = 'static/images/profile_pics/' + image_file.filename
    #                 image_file.save(file_path)

    #                 # including backend server path so that frontend can acces the image
    #                 file_path = 'http://127.0.0.1:5000/static/images/profile_pics/' + image_file.filename
    #                 user.profile_pic_url = file_path
                
    #             if new_password and new_password!= "null":
    #                 user.password = new_password
            
                        
    #             db.session.commit()
    #             flash("profile updated succesfully")
    #             return 200
            
    #         else:
    #             return 409
    #             # invalid credentials
    #     else:
    #         raise NotFoundError(message = "user not found", status_code= 404)
        


import time

class MoviesDataApi(Resource):
    
    # @jwt_required()
    @cache.cached(timeout=50)  # Cache this view for 500 seconds
    # @cache.memoize(50)
    def get(self):
        # app.logger.info('Index function was called')
        start_time = time.perf_counter()

        movies = Movies.query.order_by(desc(Movies.movie_id)).all()
        result = []
        for movie in movies:
            # if movie.number_of_ratings == None:
            #     movie.number_of_ratings = 0
            
            # if movie.number_of_ratings == 0:
            #     Rating = 0
            # else:
            #     Rating = movie.total_rating / movie.number_of_ratings
            result.append({
                'movie_id': movie.movie_id,
                'movie_name': movie.movie_name,
                'description': movie.description,
                'releaseDate': movie.releaseDate,
                'rating': movie.rating,
                'genres': movie.genres,
                'image_url': movie.image_url,
                'likes': movie.likes,
                'n_comments': movie.n_comments
            })
        
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        print(f"Time taken: {elapsed_time} seconds")

        return jsonify(result)


    @jwt_required()
    def post(self):

        
        current_user = get_jwt_identity()
        
        user = Users.query.filter_by(username=current_user).first() 
        print(" level 1")
        if user.role != 'admin':
            return 401 #unAuthorised
        
        print(" level 2")

        title = request.form.get('title')

        # movie = Movies.query.filter_by(movie_name = title)
        
        # if movie:
        #     return 410 # movie already exists in database
        
        description = request.form.get('description')
        releaseDate = request.form.get('releaseDate')
        genres = request.form.get('genres')
        rating = int(request.form.get('rating'))

        if not rating:
            return {"error": "Rating is required"}, 400
        
        if not 1 <= rating <= 10:
            return {"error": "Rating must be between 1 and 10"}, 400

        image_file = request.files.get('file')
        
        print(" level 10")

        if image_file is None:
            return 'No file uploaded', 409

        print(" level 12")

        # save the file to a folder on the server
        file_path = './static/images/' + image_file.filename
        image_file.save(file_path)

        # including backend server path so that frontend can acces the image
        file_path = 'http://127.0.0.1:5000/static/images/' + image_file.filename


        Movie = Movies(movie_name = title, genres = genres, description = description, releaseDate = releaseDate, image_url = file_path, likes = 0, rating= rating, n_comments=0, total_rating=0, number_of_ratings = 0)
        db.session.add(Movie)

        db.session.commit()

        return 200 
        
api.add_resource(MoviesDataApi, "/api/MoviesData","/api/MoviesData/<string:movieName>")

class MovieDataApi(Resource):
        
        
    # @jwt_required()
        @cache.memoize(timeout=50) 
        def get(self, movieName):

            movie = Movies.query.filter_by(movie_name=movieName).first()

            
            # If the movie doesn't exist, return a 404 error
            if movie is None:
                return {"message": "Movie not found"}, 404
            
            # if movie.number_of_ratings == None:
            #     movie.number_of_ratings = 0
                
            # if movie.number_of_ratings == 0:
            #     Rating = 0
            # else:
            #     Rating = movie.total_rating / movie.number_of_ratings

            movie_info = {
                'movie_id': movie.movie_id,
                    'movie_name': movie.movie_name,
                    'description': movie.description,
                    'releaseDate': movie.releaseDate,
                    'rating': movie.rating,
                    'genres': movie.genres,
                    'image_url': movie.image_url,
                    'likes': movie.likes,
                    'n_comments': movie.n_comments
            }
            # return jsonify(movie_info)
            print(movie_info)
            return movie_info

api.add_resource(MovieDataApi, "/api/MovieData/<string:movieName>")

class ShowsApi(Resource):

    @jwt_required()
    def post(self):
        data = request.get_json()
        
        # Extract show details from the request data
        movie_id = data.get('movie_id')
        timing = data.get('timing')
        date = data.get('date')
        ticket_price = data.get('ticketPrice')
        screenNumber = data.get('screenNumber')
        show_capacity = data.get('show_capacity')
        theatre_id = data.get('theatre_id')

        # Create a new show record in the database
        show = Shows(
            movie_id=movie_id,
            timing=timing,
            date=date,
            ticket_price=ticket_price,
            screenNumber = screenNumber,
            show_capacity = show_capacity,
            theatre_id = theatre_id,
            seats_booked = 0,
            seats_left = show_capacity
        )
        db.session.add(show)
        db.session.commit()

        # Return a response indicating successful show addition
        return {'message': 'Show added successfully'}, 201
    

    
    # @jwt_required()
    def get(self, theatre_id=None):
        if theatre_id:
            # Get future shows of the given theatre
            shows = Shows.query.filter(Shows.theatre_id == theatre_id, Shows.date >= date.today()).all()
            show_list = []
            for show in shows:
                show_data = {
                    'show_id': show.show_id,
                    'movie_id': show.movie_id,
                    'timing': str(show.timing),
                    'date': show.date,
                    # .strftime('%Y-%m-%d'),  # format date as string
                    'ticket_price': show.ticket_price,
                    'screen_id': show.screenNumber,
                }
                show_list.append(show_data)
            print(show_list)
            return show_list, 200
        else:
            return {"message": "No theatre ID provided"}, 400
    
api.add_resource(ShowsApi, "/api/ShowsApi","/api/ShowsApi/<int:theatre_id>")

class EditShowApi(Resource):
    
    @jwt_required()
    def put(self, show_id):

    # Get the existing show record
        
        show = Shows.query.filter_by(show_id=show_id).first()

        if show:
            # Get the new show details from the request data
            data = request.get_json()
            
            movie_id = data.get('movie_id')
            timing = data.get('timing')
            date = data.get('date')
            ticket_price = data.get('ticketPrice')
            screenNumber = data.get('screenNumber')
            show_capacity = data.get('screenCapacity')
            print(show_capacity)
            theatre_id = data.get('theatre_id')
            # seats_booked = data.get('seats_booked')  # Add this if you plan to modify seats_booked
            # seats_left = data.get('seats_left')  # Add this if you plan to modify seats_left

            # Update the existing show record with new details
            show.movie_id = movie_id
            show.timing = timing
            show.date = date
            show.ticket_price = ticket_price
            show.screenNumber = screenNumber
            show.show_capacity = show_capacity
            show.theatre_id = theatre_id
            show.show_capacity = show_capacity
            # show.seats_booked = seats_booked if seats_booked is not None else show.seats_booked
            # show.seats_left = seats_left if seats_left is not None else show.seats_left

            # Commit the changes to the database
            db.session.commit()

            return {'message': 'Show updated successfully'}, 200
        else:
            return {'message': 'Show not found'}, 404
    
    @jwt_required()
    def delete(self, show_id):
        # Get the existing show record
        show = Shows.query.filter_by(show_id=show_id).first()

        if show:
            # Find and delete all the future bookings of the show
            Bookings.query.filter(Bookings.show_id == show_id, Bookings.booking_date >= date.today()).delete()

            # Delete the show from the database
            db.session.delete(show)

            db.session.commit()

            return {'message': 'Show deleted successfully'}, 200
        else:
            return {'message': 'Show not found'}, 404
        
api.add_resource(EditShowApi, "/api/EditShow","/api/EditShow/<int:show_id>")

class ScreensDataApi(Resource):
    
    @jwt_required()
    def get(self, theatreId):
        # current_user = get_jwt_identity()
        # Fetch screens of the specified theater_id from the database
        screens = Screens.query.filter_by(theatre_id=theatreId).all()
        

        screen_info = []
        for screen in screens:
            screen_info.append({
                'screen_id': screen.screen_id,
                'screen_number': screen.screenNumber,
                'screen_capacity': screen.capacity
            })

        # Return the list of screen information as a JSON response
        return screen_info

api.add_resource(ScreensDataApi, "/api/ScreensApi","/api/ScreensApi/<int:theatreId>")


# //////////////      APIs used for final booking page     /////////////

class ShowDetailsApi(Resource):
    def get(self, show_id):
        show = Shows.query.get(show_id)
        theatre = Theatres.query.get(show.theatre_id)
        movie = Movies.query.get(show.movie_id)
        result = {
            'theatre_name': theatre.theatre_name,
            'address': theatre.address,
            'city': theatre.city,
            'screenNumber': show.screenNumber,
            'date': show.date,
            'timing': show.timing,
            'ticket_price': show.ticket_price,
            'movie_name': movie.movie_name
        }
        return jsonify(result)

api.add_resource(ShowDetailsApi, "/api/ShowDetailsApi/<int:show_id>")

class UserDetailsApi(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username=current_user).first()
        result = {
            'id': user.user_id,
            'name': user.name,
        }
        return jsonify(result)

api.add_resource(UserDetailsApi, "/api/UserDetailsApi")


class BookTicketsApi(Resource):
    @jwt_required()
    def post(self):
        # current_user = get_jwt_identity()

        user_id = request.json.get('user_id')
        show_id = request.json.get('show_id')
        booking_date_str = request.json.get('booking_date')
        ticket_count = int(request.json.get('ticket_count'))
        total_price = int(request.json.get('total_price'))

        booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d').date()

        # Look up the show
        show = Shows.query.filter_by(show_id=show_id).first()
        if not show:
            return {'message': 'Show not found'}, 404

        # Check if enough seats are available
        if int(show.seats_left) < int(ticket_count):
            return {'message': 'Not enough seats available'}, 400

        # Update the show's booked and left seats
        show.seats_booked += ticket_count
        show.seats_left -= ticket_count
        db.session.commit()

        # Add the booking
        booking = Bookings(
            user_id=user_id,
            show_id=show_id,
            booking_date=booking_date,
            ticket_count=ticket_count,
            total_price=total_price,
        )
        db.session.add(booking)
        db.session.commit()

        return {'message': 'Booking successful'}, 201


api.add_resource(BookTicketsApi, "/api/BookTicketsApi")


#     /////////////////          for search funtionality         //////////////////

class SearchMoviesApi(Resource):
    def get(self, query):
        # Use SQLAlchemy's `ilike` function for case-insensitive substring matching
        movies = Movies.query.filter(Movies.movie_name.ilike(f"%{query}%")).limit(5).all()

        result = []
        for movie in movies:
            result.append({
                'id': movie.movie_id,
                'movie_name': movie.movie_name,
                # Add more movie properties here if needed
            })
        print(result)
        return jsonify(result)

api.add_resource(SearchMoviesApi, "/api/searchMovies/<string:query>")


# //////////////////// profile page apis ///////////////////////
from datetime import date



class CurrentBookingsApi(Resource):
    @jwt_required()
    def get(self):
        # Get the identity of the current user
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username=current_user).first() 

        if not user:
            return {'error': 'User not found'}, 404

        # Get the current date
        current_date = date.today()

        # Get all bookings for the current user where the show date is in the future ////////

        # current_bookings = Bookings.query.join(Shows).filter(
        #     Bookings.user_id == user.user_id,
        #     Shows.date >= current_date
        # ).all()

        current_bookings = db.session.query(
            Bookings, Shows, Theatres, Movies
        ).filter(
            Bookings.user_id == user.user_id,
            Shows.date >= current_date,
            Bookings.show_id == Shows.show_id,
            Shows.theatre_id == Theatres.theatre_id,
            Shows.movie_id == Movies.movie_id
        ).all()

        # Convert the bookings to JSON ///
        # current_bookings_json = [booking.to_json() for booking in current_bookings]

        current_bookings_json = [
            {
                **booking.to_dict(),
                'theatre_name': theatre.theatre_name,
                'movie_name': movie.movie_name
            }
            for booking, show, theatre, movie in current_bookings
        ]

        print("current bookings are: ")
        print(current_bookings)
        return jsonify(current_bookings_json)


class BookingHistoryApi(Resource):
    @jwt_required()
    def get(self):
        # Get the identity of the current user
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username=current_user).first() 

        if not user:
            return {'error': 'User not found'}, 404

        # Get the current date
        current_date = date.today()

        # Get all bookings for the current user where the show date is in the past

        # booking_history = Bookings.query.join(Shows).filter(
        #     Bookings.user_id == user.user_id,
        #     Shows.date < current_date
        # ).all()

        booking_history = db.session.query(
            Bookings, Shows, Theatres, Movies
        ).filter(
            Bookings.user_id == user.user_id,
            Shows.date < current_date,
            Bookings.show_id == Shows.show_id,
            Shows.theatre_id == Theatres.theatre_id,
            Shows.movie_id == Movies.movie_id
        ).all()

        # Convert the bookings to JSON
        # booking_history_json = [booking.to_json() for booking in booking_history]

        booking_history_json = [
            {
                **booking.to_dict(),
                'theatre_name': theatre.theatre_name,
                'movie_name': movie.movie_name
            }
            for booking, show, theatre, movie in booking_history
        ]


        print(booking_history_json)
        return jsonify(booking_history_json)


# Add the resources to the API
api.add_resource(CurrentBookingsApi, '/api/CurrentBookings')
api.add_resource(BookingHistoryApi, '/api/BookingHistory')

    # @jwt_required()
    # def delete(self):

    #     current_user = get_jwt_identity()

    #     user = db.session.query(users).filter(users.username == current_user).first()

    #     if user:
    #         # blogs_by_user = db.session.query(blogs).filter(blogs.user_id == Uid).all()
    #         delete_blogs_by_user = blogs.__table__.delete().where(blogs.user_id == user.Uid)


    #         # followings = follows.query.filter(follows.follower == Uid or follows.following == Uid).all()

    #         followings_id = follows.query.filter(follows.following == user.Uid).all()
    #         for id in followings_id:
    #             temp_user = db.session.query(users).filter(users.Uid == id.follower).first()
    #             temp_user.n_following -= 1
                
            
    #         followers_id = follows.query.filter(follows.follower == user.Uid).all()
    #         for id in followers_id:
    #             temp_user = db.session.query(users).filter(users.Uid == id.following).first()
    #             temp_user.n_followers -= 1
                

    #         delete_followings = follows.__table__.delete().where(follows.follower == user.Uid)
    #         delete_followers = follows.__table__.delete().where(follows.following == user.Uid)


    #         db.session.delete(user)

    #         # db.session.delete(blogs_by_user)
    #         # db.session.delete(followings)

    #         db.session.execute(delete_blogs_by_user)
    #         db.session.execute(delete_followings)
    #         db.session.execute(delete_followers)

    #         db.session.commit()
    #         return "profile succesfully deleted", 200
    #     else:
    #        raise NotFoundError(message = "user not found", status_code= 204)
 


# class UserProfileDataApi(Resource):
    
    
#     def get(self, username):
        
#         # update_followers_AND_following_count(Uid)

#         user = users.query.filter_by(username=username).first() 

#         if user:
#             response = { "Uid": user.Uid, "name": user.name, "username": user.username, "posts": user.posts, "n_followers": user.n_followers, "n_following": user.n_following, "email": user.email,"about": user.about, "profile_pic_url" : user.profile_pic_url}
#             # not sending password to the client for secuirty reasons
#             print(" user response sent to frontend")
#             return jsonify(response)
#         else:
#             response = jsonify(error='Username Does Not Exist')
#             response.status_code = 409  # HTTP status code for conflict
#             return response


# class ProfileBlogsApi(Resource):

#     @jwt_required()
#     def get(self):
        
#         # Uid = int(Uid)
        
#         current_user = get_jwt_identity()

#         user = users.query.filter_by(username=current_user).first()

#         if user == None:
#             return "error getting user or user not found ", 409
       
#         Blogs = db.session.query(blogs).filter(blogs.user_id == user.Uid).order_by(desc(blogs.time_stamp)) 
        
#         # if Blogs == None:
#         #     return "error getting blogs or no blogs fouund", 407

#         if Blogs:

#             blogsData = []
#             for blog in Blogs:
#                 # user = db.session.query(users).filter(users.Uid == blog.user_id).first()

#                 blogsData.append( { "username": user.username, "blog_id" : blog.blog_id, "title": blog.title, "description" : blog.description, "image_url": blog.image_url, 
#                             "likes": blog.likes, "n_comments": blog.n_comments,"time_stamp": blog.time_stamp.isoformat()  })
        
#             # jsonify(response)
#             return blogsData

#         else:
#             raise NotFoundError(message = "blog not found", status_code= 204)
    
# class UserProfileBlogsApi(Resource):
    
#     def get(self, username):
        
#         user = users.query.filter_by(username=username).first()

#         if user == None:
#             return "error getting user or user not found ", 409
       
#         Blogs = db.session.query(blogs).filter(blogs.user_id == user.Uid).order_by(desc(blogs.time_stamp)) 
        
#         # if Blogs == None:
#         #     return "error getting blogs or no blogs fouund", 407

#         if Blogs:

#             blogsData = []
#             for blog in Blogs:
#                 # user = db.session.query(users).filter(users.Uid == blog.user_id).first()

#                 blogsData.append( { "username": user.username, "blog_id" : blog.blog_id, "title": blog.title, "description" : blog.description, "image_url": blog.image_url, 
#                             "likes": blog.likes, "n_comments": blog.n_comments,"time_stamp": blog.time_stamp.isoformat()  })
        
#             # jsonify(response)
#             return blogsData

#         else:
#             raise NotFoundError(message = "blog not found", status_code= 204)   


# # to sort list of bolgs according time
# from operator import itemgetter


# class FeedBlogsApi(Resource):

#     @jwt_required()
#     def get(self):
#         # Uid = int(Uid)

#         print("feed api called")
#         current_user = get_jwt_identity()

#         Currentuser = users.query.filter_by(username=current_user).first()

#         followings = follows.query.filter(follows.follower == Currentuser.Uid).all()

#         # blogsData = []

#         # if followings == None:
#         #     return blogsData, 204

#         #     # raise NotFoundError(message = "blog not found", status_code= 204)   

#         # else:
#         FeedPageData = {
#             "logged_user_name": Currentuser.name,
#             "logged_user_followings": Currentuser.n_following,
#             "blogsData": []
#         }


#         for follow in followings:
#             Blogs = db.session.query(blogs).filter(blogs.user_id == follow.following).order_by(desc(blogs.time_stamp)).all()
#             user = db.session.query(users).filter(users.Uid == follow.following).first()

#             for blog in Blogs:
#                 if blog.n_views == None:
#                     blog.n_views = 0
#                 blog.n_views += 1
#                 db.session.commit()
#                 FeedPageData["blogsData"].append( { "Uid":  user.Uid, "username": user.username, "profile_pic_url": user.profile_pic_url,"blog_id" : blog.blog_id, "title": blog.title, "description" : blog.description, "image_url": blog.image_url, 
#                              "likes": blog.likes, "n_comments": blog.n_comments, "time_stamp": blog.time_stamp.isoformat()  }) 
        
#         # if blogsData == []:
#         #     raise NotFoundError(message = "blog not found", status_code= 204)   

#         FeedPageData["blogsData"] = sorted(FeedPageData["blogsData"], key=itemgetter('time_stamp'), reverse=True)
#         print(FeedPageData)
#         return FeedPageData


# class ProfileStats(Resource):

#     @jwt_required()
#     def get(self):
        
#         """ graph mei followers_following_ratio, "avg_engagement_rate": avg_engagement_rate,
#             "avg_likes_per_post": avg_likes_per_post,
#             "avg_comments_per_post": avg_comments_per_post. ye sab dikha dena """
        

#         # avg_engagement_rate = ((total_likes + total_comments) / total_views) * 100


#         current_user = get_jwt_identity()

#         user = users.query.filter_by(username=current_user).first()
#         blogs_by_user = blogs.query.filter(blogs.user_id == user.Uid).all()
#         # followings = follows.query.filter(follows.follower == user.Uid).all()

#         total_posts = len(blogs_by_user)
#         total_followers = user.n_followers
#         total_following = user.n_following
        

#         if total_following == 0:
#             followers_following_ratio = "ND"
#         else:
#             followers_following_ratio = total_followers/total_following
        
#         total_likes_from_all_posts = 0
#         total_comments_from_all_posts = 0
#         total_views_from_all_posts = 0

#         most_liked_post_title = ""
#         most_liked_post_likes = 0

#         most_commented_post_title = ""
#         most_commented_post_n_comments = 0


#         for blog in blogs_by_user:

#             total_likes_from_all_posts += blog.likes
#             total_comments_from_all_posts += blog.n_comments
#             if blog.n_views == None:
#                 blog.n_views = 0
#             total_views_from_all_posts += blog.n_views

#             if blog.likes > most_liked_post_likes:
#                 most_liked_post_title = blog.title
#                 most_liked_post_likes = blog.likes

#             if blog.n_comments > most_commented_post_n_comments:
#                 most_commented_post_title = blog.title
#                 most_commented_post_n_comments = blog.n_comments
        
#         if total_posts == 0:
#             avg_engagement_rate = "ND"
#             avg_likes_per_post = "ND"
#             avg_comments_per_post = "ND"
        
#         else:
#             avg_engagement_rate = ((total_likes_from_all_posts + total_comments_from_all_posts) / total_views_from_all_posts) 
#             avg_engagement_rate = round(avg_engagement_rate, 2)

#             avg_likes_per_post = total_likes_from_all_posts / total_posts
#             avg_likes_per_post = round(avg_likes_per_post, 2)

#             avg_comments_per_post = total_comments_from_all_posts / total_posts
#             avg_comments_per_post = round(avg_comments_per_post, 2)
        


#         import matplotlib.pyplot as plt
#         import datetime

#         # Define the data to be plotted
#         stats = {'avg_likes_per_post': avg_likes_per_post, 'avg_comments_per_post': avg_comments_per_post, 'avg_engagement_rate': avg_engagement_rate}

#         plt.figure(figsize=(8, 6))
#         # Create a bar chart
#         plt.bar(range(len(stats)), list(stats.values()), align='center')
#         plt.xticks(range(len(stats)), list(stats.keys()))
#         plt.ylabel('Average')
#         plt.title('Profile Stats')
#         for i, v in enumerate(stats.values()):
#             plt.text(i, v, str(v), ha='center', va='bottom')

    

#         # Save the bar chart image to a desired location

#         current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

#         file_path = f'static/images/profile_stats/{current_datetime}.jpg'

#         plt.savefig(file_path)

#         print("profile stats api called 5")

#          # including backend server path so that frontend can acces the image
#         file_path = f'http://127.0.0.1:5000/static/images/profile_stats/{current_datetime}.jpg'
#         # Save the bar chart image to a desired location
        
#         print("profile stats api called 6")

#         # Close the plot
#         plt.close()

#         profile_stats = {
#             "total_posts": total_posts,
#             "total_followers": total_followers,
#             "total_following": total_following,
#             "followers_following_ratio": followers_following_ratio,

#             "most_liked_post_title": most_liked_post_title,
#             "most_liked_post_likes": most_liked_post_likes,

#             "most_commented_post_title": most_commented_post_title,
#             "most_commented_post_n_comments": most_commented_post_n_comments,

#             "total_likes_from_all_posts": total_likes_from_all_posts,
#             "total_comments_from_all_posts": total_comments_from_all_posts,
#             "total_views_from_all_posts": total_views_from_all_posts,
#             "avg_engagement_rate": avg_engagement_rate,
#             "avg_likes_per_post": avg_likes_per_post,
#             "avg_comments_per_post": avg_comments_per_post,
#             "graph_image_file_path": file_path,
#             "username": current_user,
#             "email": user.email
#             }

#         return jsonify(profile_stats)
    
# # Add API resource routes
# api.add_resource(ProfileStats, '/api/profilestats')



# class LikePost(Resource):
#     def post(self, blog_id):
#         # Retrieve the post_id from the request body
#         # post_id = request.json.get('post_id')
#         blog_id = int(blog_id)
#         blog = db.session.query(blogs).filter(blogs.blog_id == blog_id).first()
#         # Increment the like count for the post with post_id in the blog with blog_id
#         blog.likes += 1
#         # and store the updated count in your database
#         db.session.commit()
#         # ...
        
#         # Return the updated like count and whether the user has liked the post
#         return {
#             'likes': blog.likes,
#             'isLiked': True,  # assuming the user has just liked the post
#         }

# api.add_resource(LikePost, '/api/LikePost/<string:blog_id>')

# class Comments(Resource):

#     def get(self, blog_id):
#         blog_id = int(blog_id)

#         commentS = db.session.query(comments).filter(comments.blog_id == blog_id).all()
#         comments_list = []
#         for comment in commentS:
#             user = db.session.query(users).filter(users.Uid == comment.poster_user_id).first()
#             comments_list.append({"comment_id": comment.comment_id, "blog_id": comment.blog_id, "comment": comment.comment, "poster_user_id": comment.poster_user_id,"username": user.username, "profile_pic_url": user.profile_pic_url,})
            
#         return jsonify(comments_list)
    
#     @jwt_required()
#     def post(self, blog_id):
#         blog_id = int(blog_id)

#         comment = request.form.get('comment')

#         # comment = request.json.get('comment')

#         current_user = get_jwt_identity()
#         user = users.query.filter_by(username=current_user).first()
#         new_comment = comments(blog_id=blog_id, comment=comment, poster_user_id=user.Uid)
#         db.session.add(new_comment)
#         blog = db.session.query(blogs).filter(blogs.blog_id == blog_id).first()
#         blog.n_comments += 1
#         db.session.commit()

#         blog_id = int(blog_id)

#         commentS = db.session.query(comments).filter(comments.blog_id == blog_id).all()
#         comments_list = []
#         for comment in commentS:
#             user = db.session.query(users).filter(users.Uid == comment.poster_user_id).first()
#             comments_list.append({"comment_id": comment.comment_id, "blog_id": comment.blog_id, "comment": comment.comment, "poster_user_id": comment.poster_user_id,"username": user.username, "profile_pic_url": user.profile_pic_url,})
            
#         return jsonify(comments_list)

#         # return {"message": "comment added"}, 201

# api.add_resource(Comments, "/api/comments/<string:blog_id>")


# import csv

# class BlogApi(Resource):

#     def get(self, blog_id):

#         # blog_id = int(blog_id)

#         blog = db.session.query(blogs).filter(blogs.blog_id == blog_id).first()

#         if blog:
#             return {"blog_id" : blog.blog_id, "title": blog.title, "description" : blog.description, "image_url": blog.image_url, 
#                                         "time_stamp": blog.time_stamp.isoformat() }, 200
#         else:
#             raise NotFoundError(message = "blog not found", status_code= 204)   

#     @jwt_required()
#     def put(self, blog_id):

#         current_user = get_jwt_identity()

#         blog_id = int(blog_id)
#         blog = db.session.query(blogs).filter(blogs.blog_id == blog_id).first()

#         if blog:

#             title = request.form.get('title')
#             description = request.form.get('description')
#             image_file = request.files.get('file')

#             if title == None or description == None:
#                 raise BusinessValidationError(status_code= 400, error_code=	"input missing", error_message= "input missing")
            

#             if image_file is not None:

#                 # save the file to a folder on the server
#                 file_path = 'static/images/blogs/' + image_file.filename
#                 image_file.save(file_path)

#                 # including backend server path so that frontend can acces the image
#                 file_path = 'http://127.0.0.1:5000/static/images/blogs/' + image_file.filename
#                 blog.image_url = file_path
            
#             if title != 'null':
#                 blog.title = title
#             if description != 'null':
#                 blog.description = description
            

#             db.session.commit()
            
#             # return { "Uid": user.Uid, "name": user.name, "username": user.username, "posts": user.posts, "followers": user.n_followers, "following": user.n_following, "about": user.about}
#             return 200
#         else:
#             raise NotFoundError(message = "blog not found", status_code= 204)
    
#     @jwt_required()
#     def delete(self, blog_id):

#         current_user = get_jwt_identity()

#         blog_id = int(blog_id)

#         blog = db.session.query(blogs).filter(blogs.blog_id == blog_id).first()

#         user = db.session.query(users).filter(users.Uid == blog.user_id).first()

#         if blog:
#             db.session.delete(blog)
#             user.posts = user.posts-1

#             db.session.commit()
#             return 200
#         else:
#             raise BusinessValidationError(status_code= 400, error_code=	"input missing", error_message= "bad request")



#     @jwt_required()
#     def post(self):

#         current_user = get_jwt_identity()

#         print(" level 1")

#         csvFlag = request.form.get('csvFlag')

#         print("level 1.2")

#         if csvFlag != "null":
#             csv_file = request.files['csv'] # add this line to access the uploaded CSV file
#             print(" level 2")
#             # print(csv_file)
#             if csv_file:
#                 print(" level 3")
#                 image_file = request.files.get('file')
#                 print(" level 4")
#                 csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
#                 csv_row = next(csv_data)
#                 csv_row = next(csv_data)  # read the first (and only) row of the CSV file
#                 csv_title = csv_row[0]  # assume that the title is in the first column of the CSV file
#                 csv_description = csv_row[1]  # assume that the description is in the second column of the CSV file
#                 print(" level 5")
#                 if image_file is None:
#                     return 'No file uploaded', 409
#                 print(" level 6")
#                 # save the file to a folder on the server
#                 file_path = 'static/images/blogs/' + image_file.filename
#                 image_file.save(file_path)

#                 # including backend server path so that frontend can acces the image
#                 file_path = 'http://127.0.0.1:5000/static/images/blogs/' + image_file.filename

#                 user = users.query.filter_by(username=current_user).first()
#                 print(" level 7")
#                 new_blog = blogs(user_id = user.Uid, title = csv_title, description = csv_description, image_url = file_path, likes =0, n_comments =0,n_views =0)
#                 db.session.add(new_blog)

#                 user.posts = user.posts + 1
#                 db.session.commit()
#                 print(" level 8")
#                 return 200
#         else:
#             print(" level 9")

#             title = request.form.get('title')
#             description = request.form.get('description')

#             image_file = request.files.get('file')
            
#             print(" level 10")

#             if image_file is None:
#                 return 'No file uploaded', 409

#             print(" level 12")

#             # save the file to a folder on the server
#             file_path = 'static/images/blogs/' + image_file.filename
#             image_file.save(file_path)

#             # including backend server path so that frontend can acces the image
#             file_path = 'http://127.0.0.1:5000/static/images/blogs/' + image_file.filename

#             user = users.query.filter_by(username=current_user).first()

#             new_blog = blogs(user_id = user.Uid, title = title, description = description, image_url = file_path, likes =0, n_comments =0)
#             db.session.add(new_blog)

#             user.posts = user.posts + 1
#             db.session.commit()

#             return 200 


# from  sqlalchemy.sql.expression import func, select
# import random

# # api to get blogss for browse page
# class BrowseBlogsApi(Resource):

#     def get(self):
        
#         # Blogs = db.session.query(blogs).limit(6)

#         # count = db.session.query(blogs).count()
#         Blogs = db.session.query(blogs).limit(10)

#         if blogs:

#             blogsData = []

#             for blog in Blogs:
                
#                 if random.randint(1, 40) > 4:
#                     user = db.session.query(users).filter(users.Uid == blog.user_id).first()

#                     blogsData.append( { "Uid":  user.Uid, "username": user.username, "profile_pic_url": user.profile_pic_url,"blog_id" : blog.blog_id, "title": blog.title, "description" : blog.description, "image_url": blog.image_url, 
#                                 "time_stamp": blog.time_stamp.isoformat() })

#             random.shuffle(blogsData)        
#             return blogsData
#         else:
#             raise NotFoundError(message = "blog not found", status_code= 204)

# ## api to get follow status of a current user to a given user
# class FollowStatusApi(Resource):

#     @jwt_required()
#     def get(self, username):
#         # here the ussername arg is for the userprofile current user is visiting
#         current_user = get_jwt_identity()

#         Currentuser = users.query.filter_by(username=current_user).first()
#         user_being_visited = users.query.filter_by(username=username).first()

#         followings = follows.query.filter(follows.follower == Currentuser.Uid).all()

#         print(followings)

#         print(user_being_visited.Uid)

#         print("username for follow search is:   " + str(username))

#         for following in followings:
#             if following.following == user_being_visited.Uid:
#                 print(following.following)
#                 print(user_being_visited.Uid)
#                 print("step 2")
#                 return {'isFollowing': True}

#         print("not following")
#         return {'isFollowing': False}


        
#         # result = follows.query.filter(follows.follower == Currentuser.Uid and follows.following == user_being_visited.Uid).first()
        
#         # if result:
#         #     return {'isFollowing': True}
#         # else:
#         #     return {'isFollowing': False}


#     @jwt_required()
#     def post(self,username):
#         # here the ussername arg is for the userprofile current user is visiting
#         current_user = get_jwt_identity()
        
#         Currentuser = users.query.filter_by(username=current_user).first()
#         user_being_visited = users.query.filter_by(username=username).first()
        
#         # result = follows.query.filter(follows.follower == Currentuser.Uid and follows.following == user_being_visited.Uid).first()

#         followings = follows.query.filter(follows.follower == Currentuser.Uid).all()

#         result = False

#         for following in followings:
#             if following.following == user_being_visited.Uid:
#                 print(following.following)
#                 print(user_being_visited.Uid)
#                 result = True
#             else:
#                 result = False

#         if result:
#             follows.query.filter_by(following= user_being_visited.Uid, follower = Currentuser.Uid).delete()
#             # db.session.delete(result)
#             Currentuser.n_following -= 1
#             user_being_visited.n_followers -= 1
#             db.session.commit()

#             return {'isFollowing': False}
        
#         else:
#             new_following = follows(follower = Currentuser.Uid, following = user_being_visited.Uid)
#             # db.session.add(new_following)

#             new_follow = follows(follower=Currentuser.Uid, following=user_being_visited.Uid)

#             # add the new Follow object to the session
#             db.session.add(new_follow)

#             Currentuser.n_following += 1
#             user_being_visited.n_followers += 1
#             db.session.commit()

#             return {'isFollowing': True}

        
        

        
#         # isFollowing = True
#         # user = 'alice'  # Get the logged-in user from the session
#         # is_following = args['isFollowing']
#         # users[user] = is_following

# class FollowingsListApi(Resource):

#     @jwt_required()
#     def get(self):

        
#         current_username = get_jwt_identity()
#         user = users.query.filter_by(username=current_username).first()
        
#         followings = follows.query.filter(follows.follower == user.Uid).all()
        
#         followings_list = []
        
#         for follow in followings:
            
#             # following_user = users.query.filter_by(users.Uid == follow.following).first()
#             following_user = users.query.filter_by(Uid = follow.following).first()
            
#             followings_list.append({
#                 'id': following_user.Uid,
#                 'username': following_user.username,
#                 'profile_pic_url': following_user.profile_pic_url
#             })
        
#         return jsonify(followings_list)

# api.add_resource(FollowingsListApi, '/api/followingsList')

# class FollowersListApi(Resource):

#     @jwt_required()
#     def get(self):

        
#         current_username = get_jwt_identity()
#         user = users.query.filter_by(username=current_username).first()
        
#         followings = follows.query.filter(follows.following == user.Uid).all()
        
#         followings_list = []
        
#         for follow in followings:
            
#             # following_user = users.query.filter_by(users.Uid == follow.following).first()
#             following_user = users.query.filter_by(Uid = follow.follower).first()
            
#             followings_list.append({
#                 'id': following_user.Uid,
#                 'username': following_user.username,
#                 'profile_pic_url': following_user.profile_pic_url
#             })
        
#         return jsonify(followings_list)

# api.add_resource(FollowersListApi, '/api/followersList')

# # api to get search results for search box
# class SearchUsersApi(Resource):

    
#     @jwt_required()
#     def get(self):

#         q = request.args.get('q')
#         current_user = get_jwt_identity()
#         Users = users.query.filter(users.username.like(f'%{q}%')).limit(5).all()
#         results = []
#         for user in Users:
#             if user.username != current_user:
#                 results.append({"Uid": user.Uid, "username": user.username, "profile_pic_url": user.profile_pic_url})

#         return jsonify(results)

# class LikePostApi(Resource):
    
#     def get(self, blog_id):

#         blog_id = int(blog_id)

#         blog = db.session.query(blogs).filter(blogs.blog_id == blog_id).first()
#         blog.likes = blog.like + 1

#         db.session.commit()
#         return 200


##################### ADDING ALL APIs to the blueprint #################

#users data api


# #current-user profile blogs api
# api.add_resource(ProfileBlogsApi, "/api/ProfileBlogsData","/api/ProfileBlogsData/<string:Uid>")

# #user profile blogs api
# api.add_resource(UserProfileBlogsApi, "/api/UserProfileBlogsData","/api/UserProfileBlogsData/<string:username>")

# #user profile data api
# api.add_resource(UserProfileDataApi, "/api/UserProfileData","/api/UserProfileData/<string:username>")


# #Feed blogs api
# api.add_resource(FeedBlogsApi, "/api/FeedBlogsData","/api/FeedBlogsData/<string:Uid>")

# # blogpost api
# api.add_resource(BlogApi, "/api/BlogData","/api/BlogData/<string:blog_id>")

# # api to get random blogs for browse page
# api.add_resource(BrowseBlogsApi, "/api/BrowseBlogsApi","/api/BrowseBlogsApi/<string:Uid>")


# # api to get users for search box
# api.add_resource(SearchUsersApi, "/api/SearchUsers","/api/SearchUsers/<string:q>")

# # api to get and change follow status of a current user to a given user
# api.add_resource(FollowStatusApi, "/api/FollowStatus","/api/FollowStatus/<string:username>")