from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

# Create the engine for SQLite
engine = create_engine('sqlite:///concerts.db', echo=True)

# Base class for our models
Base = declarative_base()

# Band Model
class Band(Base):
    __tablename__ = 'bands'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    hometown = Column(String)

    # Relationship with Concert
    concerts = relationship('Concert', back_populates='band')
    def get_concerts(self):
        """Returns a collection of all the concerts that the Band has played"""
        return self.concerts

    def get_venues(self):
        """Returns a collection of all the venues that the Band has performed at"""
        return {concert.venue for concert in self.concerts}
    
    def play_in_venue(self, venue, date):
        """Creates a new concert for the band in the given venue on the specified date"""
        new_concert = Concert(date=date, band=self, venue=venue)
        session.add(new_concert)
        session.commit()

    def all_introductions(self):
        """Returns an array of introduction strings for each concert the band has played"""
        return [concert.introduction() for concert in self.concerts]

    @classmethod
    def most_performances(cls, session):
        """Returns the band with the most concerts played"""
        band_performances = session.query(Concert.band_id, func.count(Concert.id).label('count')).group_by(Concert.band_id).order_by(func.count(Concert.id).desc()).first()
        return session.query(Band).filter_by(id=band_performances[0]).first()

# Venue Model
class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    city = Column(String)

    # Relationship with Concert
    concerts = relationship('Concert', back_populates='venue')
    
    def get_concerts(self):
        """Returns a collection of all the concerts for the Venue"""
        return self.concerts

    def get_bands(self):
        """Returns a collection of all the bands who performed at the Venue"""
        return {concert.band for concert in self.concerts}
    
    def concert_on(self, date):
        """Finds and returns the first concert on the specified date at the venue"""
        return session.query(Concert).filter_by(venue_id=self.id, date=date).first()

    def most_frequent_band(self):
        """Returns the band with the most concerts at the venue"""
        band_performances = session.query(Concert.band_id, func.count(Concert.id).label('count')).filter_by(venue_id=self.id).group_by(Concert.band_id).order_by(func.count(Concert.id).desc()).first()
        return session.query(Band).filter_by(id=band_performances[0]).first()

# Concert Model
class Concert(Base):
    __tablename__ = 'concerts'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    
    # Foreign keys to link to Band and Venue
    band_id = Column(Integer, ForeignKey('bands.id'))
    venue_id = Column(Integer, ForeignKey('venues.id'))

    # Relationships back to Band and Venue
    band = relationship('Band', back_populates='concerts')
    venue = relationship('Venue', back_populates='concerts')

    def get_band(self):
        """Returns the Band instance for this Concert"""
        return self.band

    def get_venue(self):
        """Returns the Venue instance for this Concert"""
        return self.venue
    
    def hometown_show(self):
        """Returns True if the concert is in the band's hometown, False otherwise"""
        return self.venue.city == self.band.hometown

    def introduction(self):
        """Returns a string with the band's introduction for this concert"""
        return f"Hello {self.venue.city}!!!!! We are {self.band.name} and we're from {self.band.hometown}"


# Create the tables
Base.metadata.create_all(engine)

# Session setup
Session = sessionmaker(bind=engine)
session = Session()

#Test Data
def add_test_data(session):
    # Create bands
    band1 = Band(name="The Beatles", hometown="Liverpool")
    band2 = Band(name="Pink Floyd", hometown="London")

    # Create venues
    venue1 = Venue(title="Madison Square Garden", city="New York")
    venue2 = Venue(title="The O2 Arena", city="London")

    # Create concerts
    concert1 = Concert(date="2024-09-19", band=band1, venue=venue1)
    concert2 = Concert(date="2024-09-20", band=band2, venue=venue2)

    # Add to session and commit
    session.add_all([band1, band2, venue1, venue2, concert1, concert2])
    session.commit()

# Test the relationships
def test_queries(session):
    # Query a band and get its concerts
    band = session.query(Band).first()
    print(f"Band: {band.name}")
    print("Concerts:", band.get_concerts())
    print("Venues played:", band.get_venues())

    # Query a venue and get its concerts
    venue = session.query(Venue).first()
    print(f"Venue: {venue.title}")
    print("Concerts:", venue.get_concerts())
    print("Bands played:", venue.get_bands())

    # Query a concert and get its band and venue
    concert = session.query(Concert).first()
    print(f"Concert on {concert.date}")
    print("Band playing:", concert.get_band().name)
    print("Venue:", concert.get_venue().title)

# Test Methods
def test_methods(session):
    band = session.query(Band).first()
    print("Band Concerts:", band.get_concerts())
    print("Band Venues:", band.get_venues())
    print("All Introductions:", band.all_introductions())
    
    venue = session.query(Venue).first()
    print("Concert on Date:", venue.concert_on("2024-09-19"))
    print("Most Frequent Band:", venue.most_frequent_band())

    concert = session.query(Concert).first()
    print("Hometown Show?", concert.hometown_show())
    print("Concert Introduction:", concert.introduction())


# Initialize test data and run test queries
if __name__ == "__main__":
    add_test_data(session)
    test_queries(session)