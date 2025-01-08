from flask_sqlalchemy import SQLAlchemy 
 
db = SQLAlchemy() 
 

    
    
class Event(db.Model):
    __tablename__ = "events"

    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    speaker_list = db.Column(db.Text, nullable=True)
    ticket_price = db.Column(db.Float, nullable=False)
    guest_list = db.Column(db.Text, nullable=True)