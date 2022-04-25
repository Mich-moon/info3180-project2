from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DecimalField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 50)])
    password = StringField('Password', validators=[
        DataRequired(), Length(1, 50)])


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 50)])
    password = StringField('Password', validators=[
        DataRequired(), Length(1, 50)])
    fullname = StringField('Fullname', validators=[
        DataRequired(), Length(1, 50)])
    email = StringField('Email', validators=[
                        DataRequired(), Length(1, 50)])
    location = StringField('Location', validators=[
                           DataRequired(), Length(1, 100)])
    biography = TextAreaField('Biography', validators=[DataRequired()])
    photo = FileField('Image upload', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])


class CarForm(FlaskForm):
    make = StringField('Make', validators=[
        DataRequired(), Length(1, 50)])
    model = StringField('Model', validators=[
        DataRequired(), Length(1, 50)])
    colour = StringField('Colour', validators=[
        DataRequired(), Length(1, 20)])
    year = IntegerField('Year', validators=[DataRequired()])
    transmission = StringField('Transmission', validators=[
        DataRequired(), Length(1, 50)])
    car_type = StringField('Car Type', validators=[
        DataRequired(), Length(1, 50)])
    price = DecimalField('Price', places=2, validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    photo = FileField('Image upload', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    user_id = HiddenField('Hidden', validators=[DataRequired()])
