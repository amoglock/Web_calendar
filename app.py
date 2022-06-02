from flask import Flask, abort
import sys
from flask_restful import Api, Resource, reqparse, inputs, fields, marshal_with
from eventDB import add_event, get_all_events, get_today_events, get_event_by_id, delete_event

app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('date', type=inputs.date, help="The event date with the correct format is required! "
                                                   "The correct format is YYYY-MM-DD!", required=True)
parser.add_argument('event', type=str, help="The event name is required!", required=True)

parser_2 = reqparse.RequestParser()  # parser for filtering events if necessary
parser_2.add_argument('start_time', type=inputs.date, help="Start date for search.", required=False)
parser_2.add_argument('end_time', type=inputs.date, help="End date for search.", required=False)

resource_fields = {
    'id': fields.Integer,
    'event': fields.String,
    'date': fields.String,
}


class GetResponse(Resource):
    @marshal_with(resource_fields)
    def get(self):
        today_events = get_today_events()
        return today_events if today_events else {"data": "There are no events for today!"}


class PostResponse(Resource):
    def post(self):
        data = parser.parse_args()
        add_event(data['event'], data['date'].date())
        return {
            "message": "The event has been added!",
            "event": data['event'],
            "date": str(data['date'].date())
        }

    @marshal_with(resource_fields)
    def get(self) -> list:
        data = parser_2.parse_args()
        if data['start_time'] and data['end_time']:
            return get_all_events(data['start_time'].date(), data['end_time'].date())
        return get_all_events()


class EventByID(Resource):
    @marshal_with(resource_fields)
    def get(self, event_id):
        event = get_event_by_id(event_id)
        if event:
            return event
        return abort(404, "The event doesn't exist!")

    def delete(self, event_id):
        EventByID.get(self, event_id)
        delete_event(event_id)
        return {"message": "The event has been deleted!"}


api.add_resource(GetResponse, '/event/today')
api.add_resource(PostResponse, '/event')
api.add_resource(EventByID, '/event/<int:event_id>')

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
