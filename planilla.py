import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from config import *
import csv

def devolver_datos():

    scope = URLGOOGLE
    credenciales = ServiceAccountCredentials.from_json_keyfile_name('secreto.json', scope)
    aplicacion = gspread.authorize(credenciales)
    planilla = aplicacion.open("Encuesta-JAP-2017").sheet1
    elementos_en_planilla = planilla.get_all_records()

    if elementos_en_planilla:
        try:
            texto = json.dumps(elementos_en_planilla)
            arch = open("planilla.csv", "w")
            leer = csv.writer(arch)
            leer.writerow(texto)
            return '<h2>Archivo CSV guardado </h2>'
        except PermissionError:
            print('Por favor, cierre el archivo anterior, para visualizar el actual')
        
        arch.close()