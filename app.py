from flask import Flask, request, make_response
from functools import wraps
from config import *
import datetime
import pymongo 
from pymongo import MongoClient
import sys
from planilla import *
import logs_mongo


app = Flask(__name__)

#Autenticacion

def autenticacion(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == USER and auth.password == PASSW:
            return f(*args, **kwargs)
        return make_response('Login incorrecto!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return decorated

#Funcion after_request que captura las peticiones resueltas y devuelve valores de interes para registrarlos en el log

@app.after_request
def peticion_resuelta(response):
    log =   {
    'fecha_invocacion': datetime.datetime.now(),
    'estado': {
        'codigo': response.status_code,
        'texto': response.status
            },
    'respuesta': {
        'largo': response.content_length,
        'tipo': response.content_type,
        'mimetype': response.mimetype
            }
    }

    logs_mongo.conexion_db_mongo(log)
    return response

#Endpoint microdatos con autenticacion, que devuelve todos los resultados de la planilla en un archivo csv

@app.route('/microdatos')
@autenticacion
def planilla_google():
    return devolver_datos()

@app.route('/')
@autenticacion
def sucess():
    return '<h2>Autenticacion exitosa, bienvenido</h2>'
if __name__ == '__main__':
    app.run()
