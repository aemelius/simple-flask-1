import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from app import create_app

app = create_app()

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'
