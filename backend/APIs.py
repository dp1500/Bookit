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
    @cache.memoize(timeout=500) 
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
            result.append({
                'movie_id': movie.movie_id,
                'movie_name': movie.movie_name,
                'description': movie.description,
                'releaseDate': movie.releaseDate,
                'rating': movie.rating,
                'genres': movie.genres,
                'image_url': movie.image_url,
                
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


        Movie = Movies(movie_name = title, genres = genres, description = description, releaseDate = releaseDate, image_url = file_path, rating= rating)
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

  