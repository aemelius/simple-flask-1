import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from . import db
from app.exceptions import ValidationError

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False)

    def __repr__(self):
        return '<Message %r:%s>' % (self.id, self.name)

    def to_json(self):
        return {"id": self.id, "name": self.name}

    @staticmethod
    def from_json(json_message):
        name = json_message.get('name')
        if name is None or name == '':
            raise ValidationError('Message name is missing')
        return Message(name=name)

def none_to_slashN(item):
    return item if item is not None else '\\N'

def slashN_to_null(item):
    return db.null() if item == '\\N' else item

class Airline(db.Model):
    __tablename__ = 'airlines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False)
    alias = db.Column(db.String(128), unique=False)
    iata = db.Column(db.String(8), unique=False)
    icao = db.Column(db.String(8), unique=False)
    callsign = db.Column(db.String(128), unique=False)
    country = db.Column(db.String(128), unique=False)
    active = db.Column(db.Boolean)



    def __repr__(self):
        return "%i,%s,%s,%s,%s,%s,%s,%s" % (self.id,
                                            none_to_slashN(self.name),
                                            none_to_slashN(self.alias),
                                            none_to_slashN(self.iata) ,
                                            none_to_slashN(self.icao) ,
                                            none_to_slashN(self.callsign),
                                            none_to_slashN(self.country),
                                            'Y' if self.active else 'N')
    def to_json(self):
        return {
            "id": self.id,
            "name":self.name,
            "alias":self.alias,
            "iata":self.iata ,
            "icao":self.icao ,
            "callsign": self.callsign,
            "country":self.country,
            "active": 'Y' if self.active else 'N'
        }

    @staticmethod
    def from_row(row):
        return Airline(id=int(row[0]),
                       name=slashN_to_null(row[1]),
                       alias=slashN_to_null(row[2]),
                       iata=slashN_to_null(row[3]),
                       icao=slashN_to_null(row[4]),
                       callsign=slashN_to_null(row[5]),
                       country=slashN_to_null(row[6]),
                       active=row[7] == 'Y')


