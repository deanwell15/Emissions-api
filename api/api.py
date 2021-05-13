from flask import Flask, request, abort, json
from flask_cors import CORS
import random
from json import loads
from collections import Counter
import pymongo

app = Flask(__name__)
CORS(app)

_PORT = 5555
_HOST = "0.0.0.0"

mongodb_conn = pymongo.MongoClient("mongodb://root:muffin15@mongo:27017/")
#connect from DataGrip via link mongodb://root:muffin15@195.133.1.227:27017/
db = mongodb_conn['F_database_T']
collection = db['flights']

#request link http://195.133.1.227:5555/get_coordinates?fn=TYA1052&plane=Boeing+737-800&date=14.12.2020
@app.route("/get_coordinates", methods=['GET'])
def get_coordinates():

    fn = ' '.join(request.args.get('fn').split('+'))
    plane = ' '.join(request.args.get('plane').split('+'))
    date = ' '.join(request.args.get('date').split('+'))

    print('Recieved for coords:', fn, plane, date, flush=True)

    d = {}

    for flight in collection.find({"$and": [
                                    {'Way.flights.flightname': fn},
                                    {'Way.flights.rounds': {'$elemMatch': {'airplane': plane}}},
                                    {'Way.flights.rounds': {'$elemMatch': {'data': date}}}
                                ]}):
        w = flight['Way']
        d = w['coordinates']['points']

        #print(len(d), flush=True)

    return app.response_class(
        json.dumps(d),
        status=200,
        mimetype='application/json'
    )

#request link http://195.133.1.227:5555/get_more?fn=TYA1052&plane=Boeing+737-800&date=14.12.2020
@app.route("/get_more", methods=['GET'])
def get_more():

    fn = ' '.join(request.args.get('fn').split('+'))
    plane = ' '.join(request.args.get('plane').split('+'))
    date = ' '.join(request.args.get('date').split('+'))

    print('Recieved for more info:', fn, plane, date, flush=True)

    d = {}

    for flight in collection.find({"$and": [
                                    {'Way.flights.flightname': fn},
                                    {'Way.flights.rounds': {'$elemMatch': {'airplane': plane}}},
                                    {'Way.flights.rounds': {'$elemMatch': {'data': date}}}
                                ]}):
        w = flight['Way']
        d = w['flights']['rounds'][0]

        #print(len(d), flush=True)

    return app.response_class(
        json.dumps(d),
        status=200,
        mimetype='application/json'
    )

#request link http://195.133.1.227:5555/get_plane
@app.route("/get_plane", methods=['GET'])
def get_plane():
    try:
        #d = {'result':[db[collection].find_one()['Way'] for collection in planes]}
        d = []

        for flight in collection.find():
            w = flight['Way']
            d.append({
                'flight': w['flights']['flightname'],
                'airplane': w['flights']['rounds'][0]['airplane'],
                'date': w['flights']['rounds'][0]['data'],
                'from': w['from'],
                'to': w['to'],
                #'points': w['coordinates']['points']
            })

        return app.response_class(
            json.dumps(d),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        print('Что-то пошло не так:\n', e, flush=True)
        abort(400)

    return "Ok!"


if __name__ == "__main__":
    app.run(host=_HOST, port=_PORT)