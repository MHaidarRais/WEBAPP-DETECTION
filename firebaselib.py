from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
from google.cloud import firestore
import pyrebase

# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()
app = Flask(__name__)
api = Api(app)


firebaseconfig = {
  "apiKey": "AIzaSyCOR837pETLv0ea-VQFTmqdOOcCgqpGb8s",
  "authDomain": "flaskexp-45c90.firebaseapp.com",
  "databaseURL": "https://flaskexp-45c90.firebaseio.com",
  "projectId": "flaskexp-45c90",
  "storageBucket": "flaskexp-45c90.appspot.com",
  "messagingSenderId": "1083645712266",
  "appId": "1:1083645712266:web:ef9a25146c2c51e2ea9a73",
  "measurementId" : "G-7BXE8B3S59"
}

firebase = pyrebase.initialize_app(firebaseconfig)
storage = firebase.storage()

def abort_if_task_doesnt_exist(task_id):
    tasks_ref = db.collection('ETLE')
    ref = tasks_ref.where(u'taskid', u'==', task_id)
    if not ref:
        abort(404, message="Task {} doesn't exist".format(task_id))


parser = reqparse.RequestParser()
parser.add_argument('day')
parser.add_argument('month')
parser.add_argument('year')
parser.add_argument('hour')
parser.add_argument('minute')
parser.add_argument('second')
parser.add_argument('city')
parser.add_argument('state')
parser.add_argument('lat')
parser.add_argument('long')
parser.add_argument('number_plate')


class Task(object):
    def __init__(self, day, month, year, hour, minute, second, city, state, lat, long, number_plate):
        self.day = day
        self.month = month
        self.year = year
        self.hour = hour
        self.minute = minute
        self.second = second
        self.city = city
        self.state = state
        self.lat = lat
        self.long = long
        self.number_plate = number_plate

    def to_dict(self):
        task = {
            'day': self.day,
            'month': self.month,
            'year': self.year,
            'hour': self.hour,
            'minute': self.minute,
            'second': self.second,
            'city': self.city,
            'state': self.state,
            'lat': self.lat,
            'long': self.long,
            'number_plate': self.number_plate
        }
        return task

    def __repr__(self):
        return 'ETLE(day={}, month={}, year={}, hour={}, minute={}, second={}, city={}, state={}, lat={}, long={}, number_plate={})'.format(
            self.day, self.month, self.year, self.hour, self.minute, self.second, self.city, self.state, self.lat, self.long, self.number_plate)


class TaskList(Resource):
    def get(self):
        tasks_ref = db.collection('ETLE')
        docs = tasks_ref.stream()
        tasks = {}
        for doc in docs:
            tasks[doc.id] = doc.to_dict()
        return tasks

    def post(self):
        args = parser.parse_args()
        task = Task(day=args['day'], month=args['month'], year=args['year'], hour=args['hour'], minute=args['minute'], second=args['second'], city=args['city'], state=args['state'], lat=args['lat'], long=args['long'],number_plate=args['number_plate'])
        db.collection('ETLE').add(task.to_dict())
        return task.to_dict(), 201


class TaskListById(Resource):
    def get(self, taskid):
        doc_ref = db.collection('ETLE').document(taskid)
        if doc_ref:
            return doc_ref.get().to_dict()
        return None

    def put(self, taskid):
        args = parser.parse_args()
        tasks_ref = db.collection('ETLE')
        tasks_ref.document(taskid).update({
            "day": args['day'],
            "month": args['month'],
            "year": args['year'],
            "hour": args['hour'],
            "minute": args['minute'],
            "second": args['second'],
            "city": args['city'],
            "state": args['state'],
            "lat": args['lat'],
            "long": args['long'],
            "number_plate": args['number_plate']
        })
        return True, 201

    def delete(self, taskid):
        tasks_ref = db.collection('ETLE')
        tasks_ref.document(taskid).delete()
        return True, 201


api.add_resource(TaskList, '/etle')
api.add_resource(TaskListById, '/etle/<etleid>')

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8888, debug=True)
