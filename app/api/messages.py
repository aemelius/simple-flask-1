from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Message, Airline
from . import api
import csv
import urllib.request
import os



@api.route('/messages/', strict_slashes=False)
def get_messages():
    return jsonify({
        'messages': [comment.to_json() for comment in Message.query.all()]
    })


@api.route('/messages/<int:id>', strict_slashes=False)
def get_message(id):
    message = Message.query.get_or_404(id)
    return jsonify(message.to_json())


@api.route('/messages', methods=['POST'], strict_slashes=False)
def new_post_message():
    message = Message.from_json(request.json)
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_json()), 201, \
        {'Location': url_for('api.get_message', id=message.id)}

@api.route('/load/airlines', methods=['POST'], strict_slashes=False)
def load_airlines():
    source_file='https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat'
    urllib.request.urlretrieve(source_file, os.path.join(os.getcwd(), 'airlines.dat'))
    Airline.query.delete()
    with open(os.path.join(os.getcwd(), 'airlines.dat'), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            #print([type(x) for x in row])
            #print(row)
            airline=Airline.from_row(row)
            db.session.add(airline)
    db.session.commit()
    return jsonify({"message": "Data Loaded", "source":source_file})
    
@api.route('/airlines/', strict_slashes=False)
def get_airlines():
    return jsonify({
        'airlines': [airline.to_json() for airline in Airline.query.all()]
    })

@api.route('/airlines/<int:id>', strict_slashes=False)
def get_airline(id):
    message = Airline.query.get_or_404(id)
    return jsonify(message.to_json())
