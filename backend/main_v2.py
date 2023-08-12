from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
# import uuid

from flask_restful import Api

from celery import Celery
from celery.schedules import crontab
from redis import Redis

import datetime
from datetime import timedelta


from jwt_utils import jwt

# SETTING UP DATABASE
import os

from models import *

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine

# from flask_caching import Cache

current_dir = os.path.abspath(os.path.dirname(__file__))

from jwt_config import *

from config import create_app, create_cache


# from cache_config import cache

app = create_app()

# SETTING UP JAVA WEB TOKEN
from flask_jwt_extended import JWTManager
app.config.from_object(Config)
jwt.init_app(app)
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(
  current_dir, "database.sqlite3")

# app.config.update(
#     CELERY_BROKER_URL='redis://localhost:6379',
#     CELERY_RESULT_BACKEND='redis://localhost:6379',
# )

# cache_config = {
#     "CACHE_TYPE": "redis",  # use Redis
#     "CACHE_REDIS_URL": "redis://localhost:6379",  # Redis URL
#     "CACHE_DEFAULT_TIMEOUT": 300  # Time in seconds
# }

cache = create_cache(app)


from database import db
db.init_app(app)

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

# Import API routes from APIs.py
from APIs import api_routes

# Register API routes with app
app.register_blueprint(api_routes)

# configuring flask api
api = Api(app)
api.init_app(app)


CORS(app, resources={r"/*": {"origins": "*"}})

app.app_context().push()

engine = create_engine("sqlite:///./database.sqlite3")

# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(
#         crontab(hour=17, minute=30),  # run the task every day at 5:30 PM
#         send_daily_reminders.s(),
#     )

# @celery.task
# def send_daily_reminders():
#     users = Users.query.filter(Users.last_activity <= datetime.utcnow() - timedelta(days=1)).all()

#     for user in users:
#         # add your code here to send an alert to the user
#         # it can be an email, SMS or a Google Chat message using a webhook
#         pass


@celery.task
def test(arg):
    print(arg)
 





""" Full code section for checking users with no 24 hour activity then sending daily reminder email"""

### send_reminder_email function part of the code

import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from jinja2 import Template





# ????????????????????????????????????????????????????????????????????????????????????????????????????????????????

# SMPTP_SERVER_HOST = "localhost"
# SMPTP_SERVER_PORT = 1025
# SENDER_ADDRESS = 'test@dp.com'
# # EMAIL_HOST_USER = 'support@prettyprinted.com'
# SENDER_PASSWORD = ""


# from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)


# def send_email(to_address, subject, message, content="text", attachment_file=None):
#     msg = MIMEMultipart()
#     msg["From"] = SENDER_ADDRESS
#     msg["To"] = to_address
#     msg["Subject"] = subject
#     print("send_reminders level 5")
#     print()
    

#     if content == "html":
#         msg.attach(MIMEText(message, "html"))
#     else:
#         msg.attach(MIMEText(message, "plain"))

#     if attachment_file:
#         with open(attachment_file, "rb") as attachment:
#             # Add file as application/octet-stream
#             part = MIMEBase("application", "octet-stream")
#             part.set_payload(attachment.read())
#         # Email attachments are sent as base64 encoded
#         encoders.encode_base64(part)
#         # From: https://www.ietf.org/rfc/rfc2183.txt
#         # Bodyparts can be designated `attachment' to indicate that they are
#         # separate from the main body of the mail message, and that their
#         # display should not be automatic, but contingent upon some further
#         # action of the user.
#         part.add_header(
#             "Content-Disposition", f"attachment; filename= {attachment_file}",
#         )
#         # Add the attchment to msg
#         msg.attach(part)
    
    
#     # Send email with the PDF attachment

#     server = smtplib.SMTP('localhost', 1025)  # Replace with your SMTP server settings
#     sender = 'admin@test.com'

#     recipient = 'user@test.com'  # use this for dummy mail server

#     # body = 'Please find attached your profile statistics report.'
#     # msg.attach(MIMEText(body, 'plain'))
#     server.sendmail(sender, recipient, msg.as_string())
#     server.quit()

#     print("send_reminders level 6")
    

#     # s = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
#     # s.starttls()
#     # print("send_reminders level 7")
    
#     # s.login(SENDER_ADDRESS, SENDER_PASSWORD) 
#     # print("send_reminders level 8")
#     # s.send_message(msg)
#     # print("send_reminders level 9")
#     # s.quit()
#     return True

# ??????????????????????????????????????????????????????????????????????????????????????????

# SMPTP_SERVER_HOST = "localhost"
# SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = 'devanshparmar10@gmail.com'
# EMAIL_HOST_USER = 'support@prettyprinted.com'
# SENDER_PASSWORD = ""


from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)


def send_email(to_address, subject, message, content="text", attachment_file=None):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject
    print("send_reminders level 5")
    print()
    

    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))

    if attachment_file:
        with open(attachment_file, "rb") as attachment:
            # Add file as application/octet-stream
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        # Email attachments are sent as base64 encoded
        encoders.encode_base64(part)
        # From: https://www.ietf.org/rfc/rfc2183.txt
        # Bodyparts can be designated `attachment' to indicate that they are
        # separate from the main body of the mail message, and that their
        # display should not be automatic, but contingent upon some further
        # action of the user.
        part.add_header(
            "Content-Disposition", f"attachment; filename= {attachment_file}",
        )
        # Add the attchment to msg
        msg.attach(part)
    
    
    # Send email with the PDF attachment

    server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your SMTP server settings
    sender = 'devanshparmar10@gmail.com'

    server.starttls()

    server.login('devanshparmar10@gmail.com', 'ysbwwcdxcgfvwsxp')

    # recipient = 'pipac69843@wiemei.com'

    recipient = to_address

    # body = 'Please find attached your profile statistics report.'
    # msg.attach(MIMEText(body, 'plain'))
    server.sendmail(sender, recipient, msg.as_string())
    server.quit()

    print("send_reminders level 6")

    return True


def format_message(template_file, data={}):
    with open(template_file) as file_:
        template = Template(file_.read())
        return template.render(data=data)
    
"""can turn this into send monthly report email function"""


def send_reminder_email(user): 
    print("send_reminders level 3")
    message = "Hey {}, you have not visited our site in the last 24 hours. See what your friends are upto!".format(user.name)
    # this can be a seaprate task
    send_email(
        to_address= user.email,
        # to_address= 'ciconor573@duiter.com',
        subject="Blog Lite, See Whats Cooking",
        message=message,
        content="text",
        attachment_file=None,
    )
    print("send_reminders level 4")


### checks for users with no 24 hour activity then sends daily reminder email

from datetime import datetime, timedelta, date

celery.conf.update(
    CELERY_TIMEZONE='Asia/Kolkata',
    # other configuration variables here
)

@celery.task(name="send_reminders")
def send_reminders():
    print("send_reminders level 1")
    user_list = Users.query.all() 
    for user in user_list:
        # Check if the user has not visited/posted anything in the last 24 hours
        last_activity = user.last_activity
        if last_activity is None or datetime.utcnow() - last_activity > timedelta(hours=24):
            # Send a reminder email to the user
            send_reminder_email(user)
            print("hello from send_reminders test")
    print("send_reminders level 2")

# ///////////////////////// code that scedules reminders to be sent daily at 5 :30pm by calling send_reminders function ///////
from celery.schedules import crontab

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("Setting up periodic tasks...")
    sender.add_periodic_task(
        crontab(hour=17, minute=30),  # Runs every day at 5:30 PM IST
        send_reminders.s(),
    )
    # sender.add_periodic_task(300.0, send_reminders.s())  # Runs every 300 seconds  (5 minutes)
    
    print("Periodic tasks set up.") 

###############################################################



# test function to send email every 15 seconds
# @celery.task
# def send_test_email():
#     print("Sending test email...")
#     send_email(
#         to_address="devanshparmar10@gmail.com",  # replace with a valid email
#         subject="Test email",
#         message="This is a test email.",
#         content="text",
#         attachment_file=None,
#     )
#     print("Test email sent.")



# ////////////////////////////////////// SENDING CSV FILE TO ADMINS EMAIL WHEN CLICKED ON GENERATE //////////////////

from sqlalchemy import func
import csv
import io
from flask import url_for


def convert_to_csv(data):
    output = io.StringIO()
    writer = csv.writer(output)

    # Write the header
    writer.writerow(data[0].keys())

    # Write the data rows
    for row in data:
        writer.writerow(row.values())
    
    return output.getvalue()

import pandas as pd

# app.config['SERVER_NAME'] = '127.0.0.1:5000'


@celery.task(name="export_theatre_data")
def export_theatre_data(theatre_id):
    # Fetch the theatre data from the database
    print("theatre_id is : ", theatre_id)
    

    theatre = Theatres.query.filter_by(theatre_id=theatre_id).first()

    user = Users.query.filter_by(user_id = theatre.user_id).first()

    print("theatre name: ", theatre.theatre_name) 
    
    # Calculate the total revenue generated by the theatre
    total_revenue = db.session.query(
        func.sum(Bookings.total_price)
    ).join(
        Shows, Bookings.show_id == Shows.show_id
    ).filter(
        Shows.theatre_id == theatre_id
    ).scalar()
    
    # Calculate the total bookings made at the theatre
    total_bookings = db.session.query(
        func.sum(Bookings.ticket_count)
    ).join(
        Shows, Bookings.show_id == Shows.show_id
    ).filter(
        Shows.theatre_id == theatre_id
    ).scalar()
    
    # Get the number of shows currently showing at the theatre
    current_shows = Shows.query.filter_by(theatre_id=theatre_id).count()
    print("current shows incoming")
    print("current shows: ", current_shows)

    
    

    # field_names = ['Theatre Name', 'City', 'Address']
    data = {
    "Theatre Name": [theatre.theatre_name],
    "City": [theatre.city],
    "Address": [theatre.address],
    "Number of Screens": [theatre.screens],
    "Number of Current Shows": [current_shows],
    "Total Bookings": [total_bookings], 
    "Total Revenue": [total_revenue]
    }

    df = pd.DataFrame(data)

    
    filename = f'theatre_{theatre_id}.csv'
    file_path = os.path.join('static/csv/', filename)

    
    df.to_csv(file_path, index=False, header=True)

    download_link = f'http://127.0.0.1:5000/static/csv/{filename}'
        

    send_email(user.email, 'Your data export is ready', 'You can download your data export from this link: ' + download_link, 'plain')
    #def                    send_email(to_address,subject     , message                                                                                               , content="text", attachment_file=None):

@app.route('/api/export_theatre_data/<int:theatre_id>', methods=['POST'])
def export_theatre_data_endpoint(theatre_id):
    # Check if the current user is authorized to export data for this theatre
    # ...

    # Triggering the Celery task
    export_theatre_data.delay(theatre_id)
    
    # Return a response to the frontend
    return jsonify({'message': 'Data export has been initiated.'}), 202


# send_reminders() # this is to test the function

# ////////////////////  SENDING MONTHLY PDFS TO USERS ///////////////////

from flask import render_template_string
from weasyprint import HTML

@celery.task(name="send_monthly_report")
def send_monthly_report():
    # Get the list of all users
    user_list = Users.query.all()
    
    for user in user_list:
        # Get bookings made by the user in the past month
        bookings = Bookings.query.filter_by(user_id=user.user_id)\
                                 .filter(Bookings.booking_date >= date.today().replace(day=1)).all()

        # Create the report
        report = create_report(user, bookings)
        
        # Convert HTML report to PDF
        html = HTML(string=report)
        pdf = html.write_pdf()

        # Save the PDF to a file
        pdf_file = f"{user.username}_report.pdf"
        with open(pdf_file, "wb") as file:
            file.write(pdf)
        
        # Send the report as an email
        send_email(
            to_address=user.email,
            subject="Monthly Entertainment Report",
            message="See attached for your monthly report.",
            content="text",
            attachment_file=pdf_file
        )

def create_report(user, bookings):
    total_tickets_bought = 0
    total_expenditure = 0
    movies_watched = []

    for booking in bookings:
        print('Booking:', booking)
        total_tickets_bought += booking.ticket_count
        total_expenditure += booking.total_price

        # Get the show
        show = Shows.query.get(booking.show_id)
        
        # Get the movie
        movie = Movies.query.get(show.movie_id)
        movies_watched.append(movie.movie_name)

    # Here's a simple example of a report. You can customize this based on your needs.
    report = f"""
    <h1>Monthly Entertainment Report for {user.name}</h1>
    <p>Total tickets bought: {total_tickets_bought}</p>
    <p>Total expenditure: {total_expenditure}</p>
    <p>Movies watched: {', '.join(movies_watched)}</p>
    """

    return report


@celery.on_after_configure.connect
def setup_periodic_tasks_2(sender, **kwargs):
    sender.add_periodic_task(
        crontab(day_of_month=1, hour=0, minute=0),  # Runs on the first day of every month at 00:00
        send_monthly_report.s(),
    )

# /////////////// To test monthly reports being sent ////////////////

# @celery.on_after_configure.connect
# def setup_periodic_tasks_3(sender, **kwargs):
#     sender.add_periodic_task(15.0, send_monthly_report.s(), name='Send monthly report every 30 seconds')


# hello world route
@app.route('/', methods=['GET'])
def greetings():
    return("Hello, world!")

if __name__ == "__main__":
    app.run(debug=True)
