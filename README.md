## Concert Planner
A web application to manage bands, venues, and concerts
## Table of contents
About the Project
Features
Installation
Usage
Tests
Technologies Used
Contact

## Features
 .Bands: View band details and their concert schedules.
 .Venues: Manage venue details and hosted concerts.
 .Concerts: Schedule concerts and associate them with bands and venues.
 .Relational Queries: Retrieve concert info, venues played, bands performing, and check for "hometown shows."
## Installation
 Prerequisites
Ensure you have the following installed on your local machine:
.Python 3.x
.SQLite
.pip for managing Python packages
## setup
Clone the repo:
1.git clone https://github.com/your-username/concert-planner.git
cd concert-planner
2.Set up a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate   venv\Scripts\activate
3.Install dependencies:
pip install -r requirements.txt
4.Set up the database:
python setup_db.py
4.Run the app:
python main.py

## Usage
Running the Application: You can start the application using the following command:
python main.py
.Band Methods: Get concerts with band.get_concerts() and venues with band.get_venues().
.Venue Methods: Get concerts on a specific date with venue.concert_on(date).
Concert Methods: Check if it’s a "hometown show" with concert.hometown_show().

## Tests
Run unit tests:
python -m unittest discover tests
## Example Queries
band = session.query(Band).first()
print(band.get_concerts())

## Technologies Used
Python 3
SQLAlchemy
SQLite
Unittest.

## Cotacts
Nicholas Korir | GitHub: kibe-nick