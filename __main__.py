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

    def colombianStandings (self):
        file_name = 'tablaPosiones.xlsx'
        self.fileValidation(file_name)
        response = self.request("/standings?league=239&season=2021")
        response = response[0]['league']['standings'][0]
        standings = []
        for standing in response:
            standings_data = []
            standings_data.extend([standing['rank'], standing['team']['name'], standing['points'], standing['goalsDiff'], standing['all']['played'], standing['all']['win'], standing['all']['draw'], standing['all']['lose'], standing['all']['goals']['for'], standing['all']['goals']['against']])
            standings.append(standings_data)
        titles = ['Posicion', 'Equipo', 'Puntos', 'GolDiferencia', 'PartidosJugados', 'PartidosGanados', 'PartidosEmpatados', 'PartidosPerdidos', 'GolesMarcados', 'GolesEnContra']
        self.writeExcel(titles, standings, file_name)

    def generateFileBinarySearch(self, data_array, gol, file_name):
        self.fileValidation(file_name)
        final_data = []
        for data in data_array:
            if data[8] == gol:
                final_data.append(data)
        titles = ['Posicion', 'Equipo', 'Puntos', 'GolDiferencia', 'PartidosJugados', 'PartidosGanados', 'PartidosEmpatados', 'PartidosPerdidos', 'GolesMarcados', 'GolesEnContra']
        self.writeExcel(titles, final_data, file_name)

    def binarySearch(self, gol):
        file_name = 'resultadosBusqueda.xlsx'
        self.fileValidation(file_name)
        response = self.request("/standings?league=239&season=2021")
        response = response[0]['league']['standings'][0]
        standings = []
        for standing in response:
            standings_data = []
            standings_data.extend([standing['rank'], standing['team']['name'], standing['points'], standing['goalsDiff'], standing['all']['played'], standing['all']['win'], standing['all']['draw'], standing['all']['lose'], standing['all']['goals']['for'], standing['all']['goals']['against']])
            standings.append(standings_data)

        for i in range(1,len(standings)):
            for j in range(0,len(standings)-i):
                if(standings[j+1][8] < standings[j][8]):
                    aux=standings[j]
                    standings[j]=standings[j+1]
                    standings[j+1]=aux
        sorted_arr = standings

        i = 0
        start = 0
        end = len(sorted_arr) - 1
        while i < len(sorted_arr):
            middle = (start + end) // 2
            if sorted_arr[middle][8] == gol:
                print('Si existen equipos con esa cantidad de goles, generando archivo...')
                self.generateFileBinarySearch(sorted_arr, gol, file_name)
                return True
            elif sorted_arr[middle][8] < gol:
                start = middle + 1
            else:
                end = middle - 1
            i += 1
        print('No existen equipos con esa cantidad de goles')
        return False


if __name__ == '__main__':
    obj = SoccerApi('v3.football.api-sports.io', 'e40412f166e45bf9bb19ca88dac70be2')
    op = input('\n\nSeleccione una opción:\n1. Generar archivo de equipos colombianos.\n2. Generar archivo de tabla de posiciones.\n3. Buscar equipos por n número de goles marcados.\n4. Estado API.\nDigite el número de la opción: ')
    print("\n\n")
    try:
        if int(op) == 1:
            obj.colombianTeams()
        elif int(op) == 2:
            obj.colombianStandings()
        elif int(op) == 3:
            gol = input('\nGoles marcado: ')
            obj.binarySearch(int(gol))
        elif int(op) == 4:
            obj.status()
        else:
            print('Digite una opción valida') 
    except:
        print('Digite una opción valida')
