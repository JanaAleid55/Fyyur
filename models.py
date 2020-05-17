from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from datetime import datetime



db = SQLAlchemy()

def setup_db(app):
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    db.create_all()

def rollback():
    db.session.rollback()

def close():
    db.session.close()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website =db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue', cascade="all, delete-orphan", passive_deletes=True, lazy=True)
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()
        
    def venue_partial_details(self):
        return {
            'id': self.id,
            'name': self.name,
            'num_upcoming_shows': self.upcoming_shows().count(),
        }   
    def venue_details(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,

        }
    def upcoming_shows(self):
        upcoming_shows = Show.query.filter(Show.venue_id == self.id,Show.start_time > datetime.now())
        return upcoming_shows
    def past_shows(self):
        past_shows = Show.query.filter(Show.venue_id == self.id,Show.start_time < datetime.now())
        return past_shows

    def all_venue_details(self): 
        past_shows = self.past_shows()
        upcoming_shows = self.upcoming_shows()
        return {
            "id": self.id,
            "name": self.name,
            "genres": [self.genres],
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "website": self.website,
            "facebook_link": self.facebook_link,
            "seeking_talent": self.seeking_talent,
            "seeking_description": self.seeking_description,
            "image_link": self.image_link,
            "past_shows":[show.shows_artist_details()  for show in past_shows],
            "upcoming_shows":[show.shows_artist_details() for show in upcoming_shows],
            "past_shows_count": past_shows.count(),
            "upcoming_shows_count": upcoming_shows.count(),
        }
         

     

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website =db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False ,default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist',lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # TODO: implement any missing fields, as a database migration using Flask-Migrate   
    def artist_partial_details(self):
        return {
            'id': self.id,
            'name': self.name,
            'num_upcoming_shows': self.upcoming_shows().count(),
    }  
        
    def artist_details(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,

        }
        
    def upcoming_shows(self):
        upcoming_shows = Show.query.filter(Show.artist_id == self.id,Show.start_time > datetime.now())
        return upcoming_shows
    def past_shows(self):
        past_shows =Show.query.filter(Show.artist_id == self.id,Show.start_time < datetime.now())
        return past_shows       

    def all_artist_details(self):
        past_shows = self.past_shows()
        upcoming_shows = self.upcoming_shows()
        return {
            "id": self.id,
            "name": self.name,
            "genres": [self.genres],
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "website": self.website,
            "facebook_link": self.facebook_link,
            "seeking_venue": self.seeking_venue,
            "seeking_description": self.seeking_description,
            "image_link": self.image_link,
            "past_shows":[show.shows_venue_details()  for show in past_shows],
            "upcoming_shows":[show.shows_venue_details() for show in upcoming_shows],
            "past_shows_count": past_shows.count(),
            "upcoming_shows_count": upcoming_shows.count(),
        }
         

class Show(db.Model):
    __tablename__ = 'Show'
    
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', ondelete='CASCADE'))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete='CASCADE'))
    start_time = db.Column('date', db.DateTime)

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def shows_artist_details(self):
      artist = Artist.query.get(self.artist_id)
      return{
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": str(self.start_time)
      }
    def shows_venue_details(self):
      venue = Venue.query.get(self.venue_id)
      return{
      "venue_id": venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": str(self.start_time)
      }
    def show_details(self):
      venue = Venue.query.get(self.venue_id)
      artist = Artist.query.get(self.artist_id)
      return{
      "venue_id": venue.id,
      "venue_name": venue.name, 
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": str(self.start_time)
      }