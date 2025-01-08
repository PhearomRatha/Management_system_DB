from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Event
from sqlalchemy import exc
from config import Config
from flask_restx import Api, Resource, reqparse, fields

app = Flask(__name__)

# Configuration setup
config = Config()
app.config.from_object(config)

# Initialize API and Namespace
api = Api(app, version='1.0', title='Your API', description='API Description')
api_ns = api.namespace("Reference", path='/apiv1', description="Reference Data")

# Initialize the database
db.init_app(app)

# Create all tables
with app.app_context():
    db.create_all()

# -------------------- Get  ---------------------
# Parsers
event_parser = reqparse.RequestParser()
event_parser.add_argument('event_name', type=str, required=True, help="Event name is required")
event_parser.add_argument('description', type=str, help="Description of the event")
event_parser.add_argument('start_date', type=str, required=True, help="Start date (YYYY-MM-DD) is required")
event_parser.add_argument('end_date', type=str, required=True, help="End date (YYYY-MM-DD) is required")
event_parser.add_argument('start_time', type=str, required=True, help="Start time (HH:MM:SS) is required")
event_parser.add_argument('end_time', type=str, required=True, help="End time (HH:MM:SS) is required")
event_parser.add_argument('location', type=str, required=True, help="Event location is required")
event_parser.add_argument('speaker_list', type=str, help="Comma-separated speaker names")
event_parser.add_argument('ticket_price', type=float, help="Ticket price for the event")
event_parser.add_argument('guest_list', type=str, help="Comma-separated guest names")

# Fields for marshaling
event_fields = api.model('Event', {
    'event_id': fields.Integer,
    'event_name': fields.String,
    'description': fields.String,
    'start_date': fields.String,
    'end_date': fields.String,
    'start_time': fields.String,
    'end_time': fields.String,
    'location': fields.String,
    'speaker_list': fields.String,
    'ticket_price': fields.Float,
    'guest_list': fields.String
})


@api_ns.route('/events')
class EventListResource(Resource):
    
    @api.marshal_list_with(event_fields)
    def get(self):
        """Get all events"""
        events = Event.query.all()
        return events

    @api.expect(event_parser)
    def post(self):
        """Create a new event"""
        args = event_parser.parse_args()
        new_event = Event(
            event_name=args['event_name'],
            description=args['description'],
            start_date=args['start_date'],
            end_date=args['end_date'],
            start_time=args['start_time'],
            end_time=args['end_time'],
            location=args['location'],
            speaker_list=args['speaker_list'],
            ticket_price=args['ticket_price'],
            guest_list=args['guest_list']
        )
        try:
            db.session.add(new_event)
            db.session.commit()
            return {'message': 'Event created successfully'}, 201
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f"Error: {str(e.__cause__)}"}, 500
        
@api_ns.route('/events/<int:event_id>')
class EventResource(Resource):
    @api.marshal_with(event_fields)
    def get(self, event_id):
        """Get event by ID"""
        event = Event.query.get(event_id)
        if not event:
            return {'message': 'Event not found'}, 404
        return event

    @api.expect(event_parser)
    def put(self, event_id):
        """Update an event by ID"""
        args = event_parser.parse_args()
        event = Event.query.get(event_id)
        if not event:
            return {'message': 'Event not found'}, 404

        event.event_name = args['event_name']
        event.description = args['description']
        event.start_date = args['start_date']
        event.end_date = args['end_date']
        event.start_time = args['start_time']
        event.end_time = args['end_time']
        event.location = args['location']
        event.speaker_list = args['speaker_list']
        event.ticket_price = args['ticket_price']
        event.guest_list = args['guest_list']

        try:
            db.session.commit()
            return {'message': 'Event updated successfully'}, 200
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f"Error: {str(e.__cause__)}"}, 500

    def delete(self, event_id):
        """Delete an event by ID"""
        event = Event.query.get(event_id)
        if not event:
            return {'message': 'Event not found'}, 404

        try:
            db.session.delete(event)
            db.session.commit()
            return {'message': 'Event deleted successfully'}, 200
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f"Error: {str(e.__cause__)}"}, 500

        
        

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)