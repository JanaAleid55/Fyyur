#fist test
#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from models import rollback, close, setup_db,Venue, Show, Artist
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


app = Flask(__name__)
setup_db(app)
moment = Moment(app)
# app.config.from_object('config')
# migrate = Migrate(app, db)
# db.drop_all()
# db.create_all()

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format,locale='en')

app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  areas = Venue.query.distinct('city','state').all()
  data = []
  for area in areas:
    venues = Venue.query.filter_by(city= area.city, state= area.state).all()
    record = {
      'city': area.city,
      'state': area.state,
      'venues': [venue.venue_partial_details() for venue in venues],
    }
    data.append(record)
    
  return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term','')
  result = Venue.query.filter(Venue.name.ilike('%{}%'.format(search_term))).all()
  count_venues = len(result)
  response = {
      "count": count_venues,
      "data": [venue.venue_partial_details()  for venue in result]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue=Venue.query.get(venue_id)
  data=venue.all_venue_details()
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
   try:
    description=''
    seeking=False
    if 'seeking_talent' in request.form:
      seeking = True
      if 'seeking_description' in request.form:
        description = request.form['seeking_description']
        
    venue = Venue(
    name=request.form['name'],
    city=request.form['city'],
    state=request.form['state'],
    address=request.form['address'],
    genres=request.form.getlist('genres'),
    phone=request.form['phone'],
    image_link=request.form['image_link'],
    facebook_link=request.form['facebook_link'],
    website=request.form['site_link'],
    seeking_description=description,
    seeking_talent=seeking,
    )
    venue.insert()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
   except:
    rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
   finally:
    close()
   return render_template('pages/home.html')


  # on successful db insert, flash success
  # flash('Venue ' + request.form['city'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue=Venue.query.get(venue_id)
    venue.remove()
  except:
    rollback()
  finally:
    close()
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists=Artist.query.order_by('id').all()
  data=[{"id":artist.id, "name":artist.name}  for artist in artists]
  # TODO: replace with real data returned from querying the database

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term','')
  result = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).all()
  count_artists = len(result)
  response = {
      "count": count_artists,
      "data": [artist.artist_partial_details()  for artist in result]
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/venue/<int:venue_id>/search', methods=['POST'])
def search_venue_artists(venue_id):
  form = ShowForm()
  search_term = request.form.get('search_term','')
  artists = Artist.query.filter(Show.artist_id == Artist.id,Show.venue_id == venue_id,Artist.name.ilike('%{}%'.format(search_term))).all()
  # Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).all()
  count_artists = len(artists)
  response = {
      "count": count_artists,
      "venue": venue_id,
      "data": [artist.artist_partial_details()  for artist in artists]
  }
  return render_template('pages/search_venue_artists.html', results=response, search_term=search_term, form=form)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist=Artist.query.get(artist_id)
  data=artist.all_artist_details()
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist=Artist.query.get(artist_id).artist_details()
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
   try:
    seeking=False
    if 'seeking_venue' in request.form:
      seeking = True

      description=''
      if 'seeking_description' in request.form:
        description = request.form['seeking_description']

    artist = Artist.query.get(artist_id)
    artist.name=request.form['name']
    artist.city=request.form['city']
    artist.state=request.form['state']
    artist.genres=request.form.getlist('genres')
    artist.phone=request.form['phone']
    artist.image_link=request.form['image_link']
    artist.facebook_link=request.form['facebook_link']
    artist.website=request.form['site_link']
    artist.seeking_description=description
    artist.seeking_venue=seeking
    artist.update()
   except:
    rollback()
   finally:
    close()

   return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue=Venue.query.get(venue_id).venue_details()
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

   try:
    seeking=False
    if 'seeking_talent' in request.form:
      seeking = True
      
    description=''
    if 'seeking_description' in request.form:
      description = request.form['seeking_description']

    venue = Venue.query.get(venue_id)
    venue.name=request.form['name']
    venue.city=request.form['city']
    venue.state=request.form['state']
    venue.address=request.form['address']
    venue.genres=request.form.getlist('genres')
    venue.phone=request.form['phone']
    venue.image_link=request.form['image_link']
    venue.facebook_link=request.form['facebook_link']
    venue.website=request.form['site_link']
    venue.seeking_description=description
    venue.seeking_talent=seeking
    venue.update()
   except:
    rollback()
   finally:
    close()

   return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
   try:
    description=''
    seeking=False
    if 'seeking_venue' in request.form:
      seeking = True
      if 'seeking_description' in request.form:
        description = request.form['seeking_description']

    artist = Artist(
    name=request.form['name'],
    city=request.form['city'],
    state=request.form['state'],
    phone=request.form['phone'],
    genres=request.form.getlist('genres'),
    image_link=request.form['image_link'],
    facebook_link=request.form['facebook_link'],
    website=request.form['site_link'],
    seeking_description=description,
    seeking_venue=seeking,
    )
    artist.insert()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
   except:
    rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
   finally:
    close()

   return render_template('pages/home.html')


  # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  # return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows=Show.query.all()
  data=[show.show_details() for show in shows]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
   try:
    show = Show(
    artist_id=request.form['artist_id'],
    venue_id=request.form['venue_id'],
    start_time=request.form['start_time'],
    )
    show.insert()
    flash('Show was successfully listed!')
   except:
    rollback()
    flash('An error occurred. Show could not be listed.')
   finally:
    close()

   return render_template('pages/home.html')

  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
