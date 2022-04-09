from . import db
from werkzeug.security import generate_password_hash
from datetime import datetime


class Car(db.Model):
    __tablename__ = 'Cars'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    colour = db.Column(db.String(20), nullable=False)
    year = db.Column(db.String(5), nullable=False)
    transmission = db.Column(db.String(20), nullable=False)
    car_type = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    photo = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)

    def __init__(self, description, make, model, colour, year, transmission, car_type, price, photo, user_id):
        self.description = description
        self.make = make
        self.model = model
        self.colour = colour
        self.year = year
        self.transmission = transmission
        self.car_type = car_type
        self.price = price
        self.photo = photo
        self.user_id = user_id

    def __repr__(self):
        return '<Car %r>' % self.model


class Favourite(db.Model):
    __tablename__ = 'Favourites'

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('Cars.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)

    def __init__(self, car_id, user_id):
        self.car_id = car_id
        self.user_id = user_id

    def __repr__(self):
        return '<User {0} : Car {1} >'.format(self.user_id, self.car_id)


class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    location = db.Column(db.String(100))
    biography = db.Column(db.String(500))
    photo = db.Column(db.String(255))
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, username, password, name, email, location, biography, photo):
        self.username = username
        self.password = generate_password_hash(
            password, method='pbkdf2:sha256')
        self.name = name
        self.email = email
        self.location = location
        self.biography = biography
        self.photo = photo

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % self.username
