# initialize_db.py
from sqlalchemy import create_engine
from main import Base  # Adjust this import based on your actual model file name

# Create the engine for SQLite
engine = create_engine('sqlite:///concerts.db', echo=True)

# Create all tables
Base.metadata.create_all(engine)
