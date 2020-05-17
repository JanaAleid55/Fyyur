from datetime import datetime
from flask_wtf import Form
from formenum import Genre, State
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField,BooleanField,TextAreaField
from wtforms.validators import DataRequired, AnyOf, URL

class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today(),
    )


class VenueForm(Form):
    state_value=''
    name = StringField(
        'name', validators=[DataRequired(message='Please enter a name.')]
    )
    city = StringField(
        'city', validators=[DataRequired(message='Please enter a city.')]
    )
    state = SelectField(
        'state', validators=[DataRequired(message='Please enter a state.')],
         choices=State.state_list(),        
    )
    address = StringField(
        'address', validators=[DataRequired(message='Please enter a address.')]
    )
    phone = StringField(
        'phone', validators=[DataRequired()]
    )
    seeking_talent = BooleanField (
        'seeking_talent', default = False
    )
    seeking_description =TextAreaField(
        'seeking_description'
    )
    image_link = StringField(
        'image_link', validators=[URL(message="Invalid URL")]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
         choices=Genre.genre_list(),
    )
    site_link = StringField(
        'site_link', validators=[URL(message="Invalid URL")]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(message="Invalid URL")]
    )


class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
         choices=State.state_list()
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )

    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
         choices=Genre.genre_list()
    )
    site_link = StringField(
        'site_link', validators=[URL()]
    )
    seeking_venue = BooleanField (
        'seeking_venue', default = False
    )
    seeking_description =TextAreaField(
        'seeking_description'
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM


