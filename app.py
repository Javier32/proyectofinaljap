from functools import wraps
import requests
import os
from flask import Flask, request, Response
from config import *
import json
import time
import datetime
import os 
from pymongo import MongoClient
from bson import json_util
import collections
from logica_planilla import *
import csv

app = Flask(__name__)

@app.route('/')
def hola():}
    @app.after_request
def after(response):
    log ={
        'service':str(request.url_rule),
        'date':str(datetime.datetime.now()),
        'status':{
            'code': str(response.status_code),
            'text': str(response.status)
            },
        'responses':
        {
            'long':str(response.content_length),
            'type':str(response.content_type),
            'mimetype': str(response.mimetype)},
        'user':{
            'ip_user': str(request.environ['REMOTE_ADDR']),
            'user_port': str(request.environ['REMOTE_PORT'])
            }
        }
    
    client = MongoClient(mongo_uri)
    db = client.test_database
    collection = db.test_collection
    try:
        insertar_log = collection.insert_one(log)
        if insertar_log.acknowledged == True:
            
            print('Now Saving: ', log)
            print ('Success: saved log. ')
    except:
        print('Error. Terminando el proceso. ', sys.exc_info())

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    for user in USERS:
        if (user['user'] == username and user['pass'] == password):            
            return True
        else:
            print('Error: sus credenciales no coinciden.')

def authenticate():
    return Response(
    'No se pudo verificar su nivel de acceso para ésta URL.\n'
    'Debes iniciar sesión con las credenciales correctas', 401,
    {'WWW-Authenticate': 'Basic realm="Login requerido"'})


def requires_auth(f):
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/results')
def resultados():
    return main_sheets()

@app.route('/microdata')
def microdatos():
    return sent_sentimiento()       
@app.route('/working_page')
def mostrar():
    return('Ésta página funciona.')
app.run()


