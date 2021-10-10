import http.client
import json
import os
from os import remove
import openpyxl

class SoccerApi:
    def __init__ (self, endpoint, apikey):
        self.endpoint = endpoint
        self.apikey = apikey

    def request (self, parameters):
        conn = http.client.HTTPSConnection(self.endpoint)
        headers = {
            'x-rapidapi-host': self.endpoint,
            'x-rapidapi-key': self.apikey
        }
        conn.request("GET", parameters, headers=headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode("utf-8"))
        conn.close()
        return data['response']

    @staticmethod
    def fileValidation (file):
        if os.path.isfile(file):
            remove(file)

    @staticmethod
    def writeExcel(titles, data, file_name):
        wb = openpyxl.Workbook()
        hoja = wb.active
        hoja.append(titles)
        for row in data:
            hoja.append(row)
        wb.save(file_name)
    
    # FUNCIONES PARA PETICIONES
    def status (self):
        response = self.request("/status")
        print (response)

    def colombianTeams (self):
        file_name = 'listadoEquiposColombianos.xlsx'
        self.fileValidation(file_name)
        response = self.request("/teams?season=2021&league=239")
        teams = []
        for team in response:
            teams_data = []
            teams_data.extend([team['team']['id'], team['team']['name'], team['team']['founded'], team['team']['logo'], team['venue']['name'], team['venue']['city'], team['venue']['address'], team['venue']['capacity']])
            teams.append(teams_data)
        titles = ['IdEquipo', 'NombreEquipo', 'AñoFundado', 'LinkLogo', 'Estadio', 'CiudadEstadio', 'DirecciónEstadio', 'CapacidadEstadio']
        self.writeExcel(titles, teams, file_name)

if __name__ == '__main__':
    obj = SoccerApi('v3.football.api-sports.io', 'e40412f166e45bf9bb19ca88dac70be2')
    # obj.status()
    obj.colombianTeams()