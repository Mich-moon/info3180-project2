"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
from app import app, db, login_manager
from flask import render_template, request, jsonify, send_file, redirect, url_for
from flask import flash, session, abort, send_from_directory, g, make_response
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app.models import User, Car, Favourite
from .forms import RegisterForm, LoginForm


# Using JWT
import jwt
from flask import _request_ctx_stack
from functools import wraps
import datetime


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Create a JWT @requires_auth decorator
        # This decorator can be used to denote that a specific route should check
        # for a valid JWT token before displaying the contents of that route.

        auth = request.headers.get('Authorization', None)

        if not auth:
            return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
        elif len(parts) == 1:
            return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
        elif len(parts) > 2:
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

        token = parts[1]
        try:
            payload = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
        except jwt.DecodeError:
            return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

        g.current_user = user = payload
        return f(*args, **kwargs)

    return decorated


def generate_token(payload):
    # generate JWT token when a user logs into your web application
    # and you send it back to the frontend where it can be stored in
    # localStorage for any subsequent API requests.

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify(error=None, data={'token': token}, message="Token Generated")


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/register', methods=['POST'])
def register():
    """Accepts user information and saves it to the database"""

    form = RegisterForm

    if request.method == 'POST':

        if form.validate_on_submit():

            photo = form.photo.data
            photo_filename = secure_filename(photo.filename)
            photo.save(os.path.join(
                os.environ.get('UPLOAD_FOLDER'), photo_filename
            ))

            user = User(
                username=form.username.data,
                password=form.password.data,
                name=form.name.data,
                email=form.email.data,
                location=form.location.data,
                biography=form.biography.data,

                photo=photo_filename
            )
            db.session.add(user)
            db.session.commit()

            new_id = user.id
            user = db.session.query(User).get(new_id)

            return jsonify(user), 201

        return jsonify(errors=form_errors(form)), 400


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Accepts login credentials as username and password"""
    form = LoginForm()

    if request.method == "POST":

        if form.validate_on_submit():

            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()

            if user is not None and check_password_hash(user.password, password):
                # get user id, load into session
                login_user(user)

                user_name = form.name.data
                user_id = db.session.query(User).filter_by(
                    username=user_name).all().id

                payload = {
                    'sub': user_id,  # subject, usually a unique identifier
                    'name': user_name,
                    # issued at time
                    'iat': datetime.datetime.now(datetime.timezone.utc),
                    # expiration time
                    'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=2)
                }

                # generate JWT token
                jwt = generate_token(payload)
                return jsonify(
                    message="Login Successful",
                    token=jwt
                ), 200

        return jsonify(errors=form_errors(form)), 400


@app.route('/api/auth/logout', methods=['POST'])
@login_required
@requires_auth
def logout():
    """Logs out a user"""
    # Logout the user and end the session
    logout_user()
    return jsonify(message="Log out successful"), 200


@app.route('/api/cars', methods=['POST', 'GET'])
@requires_auth
def cars():
    """Returns all cars & adds a new car"""

    jwt_payload = g.current_user
    jwt_user_id = jwt_payload['sub']

    if request.method == 'POST':
        if form.validate_on_submit():

            photo = form.photo.data
            photo_filename = secure_filename(photo.filename)
            photo.save(os.path.join(
                os.environ.get('UPLOAD_FOLDER'), photo_filename
            ))

            car = Car(
                description=form.description.data,
                make=form.make.data,
                model=form.model.data,
                colour=form.colour.data,
                year=form.year.data,
                transmission=form.transmission.data,
                car_type=form.car_type.data,
                price=form.price.data,
                photo=form.photo.data,
                user_id=jwt_user_id
            )
            db.session.add(car)
            db.session.commit()

            new_id = car.id
            car = db.session.query(Car).get(new_id)

            return jsonify(car=car), 201

        return jsonify(errors=form_errors(form)), 400

    else:
        results = db.session.query(Car).all()

        if results is not None:

            cars = [{
                "id": c.id,
                "description": c.description,
                "make": c.make,
                "model": c.model,
                "colour": c.colour,
                "year": c.year,
                "transmission": c.transmission,
                "car_type": c.car_type,
                "price": c.price,
                "photo": c.photo,
                "user_id": c.user_id
            } for c in results]

            return jsonify(cars=cars), 200


@app.route('/api/cars/<car_id>', methods=['GET'])
@requires_auth
def get_car(car_id):
    """Get Details of a specific car"""
    car = db.session.query(Car).get(int(car_id))

    if car is not None:
        return jsonify(car=car), 200

    return jsonify(message="Item not found"), 400


@app.route('/api/cars/<car_id>/favourite', methods=['POST'])
@requires_auth
def add_favourite_car(car_id):
    """Add car to Favourites for logged in user"""
    jwt_payload = g.current_user
    jwt_user_id = jwt_payload['sub']

    fave = Favourite(
        car_id=int(car_id),
        user_id=jwt_user_id
    )
    db.session.add(fave)
    db.session.commit()

    return jsonify(
        message="Car Successfully Favourited",
        car_id=car_id
    ), 201


@app.route('/api/search', methods=['GET'])
@requires_auth
def search_cars():
    """Search for cars by make or model"""
    if request.args and 'make' in request.args:
        make = request.args['make']
        cars = db.session.query(Car).filter_by(make=make).all()
        return jsonify(cars=cars), 200
    elif request.args and 'model' in request.args:
        model = request.args['model']
        cars = db.session.query(Car).filter_by(model=model).all()
        return jsonify(cars=cars), 200
    else:
        return jsonify(message="Query param expected"), 400


@app.route('/api/users/<user_id>', methods=['GET'])
@requires_auth
def get_user(user_id):
    """Get Details of a user"""
    user = db.session.query(User).get(int(user_id))

    if user is not None:
        return jsonify(user=user), 200

    return jsonify(message="Item not found"), 404


@app.route('/api/users/<user_id>/favourites', methods=['GET'])
@requires_auth
def get_favourite_car(user_id):
    """Get cars that a user has favourited"""
    #user_favourites = Favourite.query.filter_by(user_id=user_id).all()
    user_favourites = db.session.query(
        Favourite).filter_by(user_id=user_id).all()

    if user_favourites is not None:
        return jsonify(favourites=user_favourites), 200

    return jsonify(message="Item not found"), 404


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            )
            error_messages.append(message)

    return error_messages


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return jsonify(error="Page Not Found"), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
