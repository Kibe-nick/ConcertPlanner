import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, Band, Venue, Concert

# Create a temporary in-memory database for testing
engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def test_band_creation():
    band = Band(name="The Beatles", hometown="Liverpool")
    session.add(band)
    session.commit()
    
    # Query the band from the database
    retrieved_band = session.query(Band).filter_by(name="The Beatles").first()
    assert retrieved_band is not None
    assert retrieved_band.hometown == "Liverpool"

def test_venue_creation():
    venue = Venue(title="Royal Albert Hall", city="London")
    session.add(venue)
    session.commit()
    
    # Query the venue from the database
    retrieved_venue = session.query(Venue).filter_by(title="Royal Albert Hall").first()
    assert retrieved_venue is not None
    assert retrieved_venue.city == "London"

def test_concert_creation():
    band = Band(name="The Rolling Stones", hometown="London")
    venue = Venue(title="Madison Square Garden", city="New York")
    session.add(band)
    session.add(venue)
    session.commit()  # Commit to ensure band and venue IDs are created

    concert = Concert(date="2024-01-01", band=band, venue=venue)
    session.add(concert)
    session.commit()
    
    # Query the concert from the database
    retrieved_concert = session.query(Concert).filter_by(date="2024-01-01").first()
    assert retrieved_concert is not None
    assert retrieved_concert.band.name == "The Rolling Stones"
    assert retrieved_concert.venue.title == "Madison Square Garden"

def test_relationships():
    band = Band(name="Queen", hometown="London")
    venue = Venue(title="Wembley Stadium", city="London")
    concert = Concert(date="2024-02-01", band=band, venue=venue)
    session.add(band)
    session.add(venue)
    session.add(concert)
    session.commit()
    
    # Test band relationships
    retrieved_band = session.query(Band).filter_by(name="Queen").first()
    assert len(retrieved_band.concerts) == 1
    assert retrieved_band.concerts[0].venue.title == "Wembley Stadium"

    # Test venue relationships
    retrieved_venue = session.query(Venue).filter_by(title="Wembley Stadium").first()
    assert len(retrieved_venue.concerts) == 1
    assert retrieved_venue.concerts[0].band.name == "Queen"

# Run tests
if __name__ == '__main__':
    pytest.main()
