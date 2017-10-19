# Copyright (C) 2017, Isaac Porta "uny11"
#
# This file is part of SE-Bigdata.
#
# SE-Bigdata is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SE-Bigdata is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SE-Bigdata.  If not, see <http://www.gnu.org/licenses/>.

from chpp import CHPPhelp
import bbdd
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import sqlite3
from colorama import init, Fore, Back, Style

# print Bienvenida
init(autoreset=True)
print('\n')
print(Fore.WHITE + Back.GREEN + '''SE-BIGDATA v0.0''')
print('Copyright (C) 2017, "uny11" Isaac Porta \nEste programa es software libre bajo la licencia GPL-v3')
print('\n')
print(Fore.GREEN + Style.BRIGHT + 'Bienvenido y Gracias por participar en este estudio!')
print('y no dudes en reportar algun fallo o duda (uny11)\n')

#Iniciamos base de datos de SE-Bigdata
basedatos = 'bigdata.sqlite'
bbdd.init_base(basedatos)

# Iniciamos claves y funciones para acceder a los recursos CHPP de la API de Hatrick
helper = CHPPhelp()

# Buscamos si la App tiene la autorizacion CHPP del usuario
conn = sqlite3.connect(basedatos)
cur = conn.cursor()
try:
    cur.execute('SELECT key FROM keys WHERE id = 1')
    test = cur.fetchone()[0]
    # El test es OK! nada que hacer
except:
    # El test es NO OK -> lanzamos proceso de autorizacion
    print('\n')
    print('Antes de nada, es necesario tu autorizacion-CHPP para recoger datos Hattrick!')
    print('Sigue las instruciones: \n')
    helper.get_auth(basedatos)

# Recuperamos tokens, user y equipos del user
cur.execute('SELECT key FROM keys WHERE id = 1 LIMIT 1')
user_key = cur.fetchone()[0]
cur.execute('SELECT key FROM keys WHERE id = 2 LIMIT 1')
user_secret = cur.fetchone()[0]
cur.execute('SELECT descripcion FROM info WHERE id = 1 LIMIT 1')
user = cur.fetchone()[0]
cur.execute('SELECT idHT,descripcion FROM info WHERE id > 1 LIMIT 3')
listaEquiposID = []
listaEquiposNombre = []
for row in cur:
    listaEquiposID.append(row[0])
    listaEquiposNombre.append(row[1])

cur.close()

# Lanzamos MENU de la aplicacion
while True:
    print('\n')
    print(Fore.CYAN + Style.BRIGHT + 'Que te apetece hacer', Fore.CYAN + Style.BRIGHT+str(user),Fore.CYAN + Style.BRIGHT+'?\n')
    print('     1.- Obtener datos de Hattrick')
    print('     2.- Enviar datos al servidor para enriquecer el estudio')
    print('     3.- Ver tus estadisticas')
    print('     4.- Salir\n')
    opcion = input('(por defecto 4) >> ')

    if opcion == '1':
        # Paso0 - Miramos si hay partidos en la base y si hay miramos fecha del ultimo
        conn = sqlite3.connect(basedatos)
        cur = conn.cursor()
        try:
            cur.execute( 'SELECT max(MatchDate) FROM partidos')
            fechamax = cur.fetchone()[0]
        except:
            fechamax = datetime.today() - timedelta(days=20)
        cur.close()

        # Paso1 - Recuperamos lista de partidos nuevos
        print('\n')
        print('Buscando partidos en www.hattrick.org... ')
        print('Paciencia, puede tardar un poco..\n')
        num = 0
        for team in listaEquiposID:
            print('Para tu equipo "',listaEquiposNombre[num],'"')
            listaPartidos = bbdd.new_partidos(helper, basedatos, user_key, user_secret, fechamax, team)
            # Paso1.2 - Recuperar detalle de los partidos nuevos para cada equipo
            if len(listaPartidos) > 0:
                print('Recuperando los datos de los ',Back.WHITE + Fore.BLACK + str(len(listaPartidos)), Style.RESET_ALL + ' partidos nuevos de www.hattrick.org... \n')
                for partido in listaPartidos:
                    # detalle partido, alineacion y sustituciones
                    bbdd.get_partido(helper, basedatos, user_key, user_secret, partido)
            else:
                None
            num = num + 1

        print(Back.GREEN + Fore.WHITE + 'Hecho!' + Style.RESET_ALL)

    elif opcion == '2':
        print('\n')
        print(Back.RED + Fore.WHITE + 'Perdón! Esta parte esta en contrucción' + Style.RESET_ALL)
        print('\n')

    elif opcion == '3':
        print('\n')
        print(Back.RED + Fore.WHITE + 'Perdón! Esta parte esta en contrucción' + Style.RESET_ALL)
        print('\n')

    elif opcion == '4':
        print('\n')
        break
    elif len(opcion) < 1:
        print('\n')
        break

    else:
        print('\n')
        print(Back.RED + Fore.WHITE + 'Perdón! Esta parte esta en contrucción' + Style.RESET_ALL)
        print('\n')
