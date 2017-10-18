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
init(autoreset=True) #activar colorama para windows, no efecto en el resto de plataformas
print('\n')
print(Fore.WHITE + Back.GREEN + '''BIENVENIDO a SE-BIGDATA! v0.0''')
print('''Copyright (C) 2017  Isaac Porta "uny11"
    Este programa es software libre (licencia GPL-v3)''')
print('\n\n')
print(Style.BRIGHT + 'Gracias por participar en este estudio!')
print('no dudes en reportar algun fallo y/o duda (uny11)')
print('\n')

# Iniciamos claves y funciones para acceder a los recursos CHPP de la API de Hatrick
helper = CHPPhelp()

#Iniciamos base de datos de SE-Bigdata
basedatos = 'bigdata.sqlite'
bbdd.init_base(basedatos)

# Buscamos si la App tiene la autorizacion CHPP del usuario
conn = sqlite3.connect(basedatos)
cur = conn.cursor()
try:
    cur.execute('SELECT key FROM keys WHERE id = 3')
    test = cur.fetchone()[0]
    # El test es ok, recuperamos claves de los usuarios para interactuar con la API
    cur.execute('SELECT key FROM keys WHERE id = 3 LIMIT 1')
    user_key = cur.fetchone()[0]
    cur.execute('SELECT key FROM keys WHERE id = 4 LIMIT 1')
    user_secret = cur.fetchone()[0]
    try:
        cur.execute( 'SELECT max(MatchDate) FROM partidos')
        fechamax = cur.fetchone()[0]
        if fechamax == None:
            fechamax = datetime.today() - timedelta(days=90)
        else:
            fechamax = fechamax + timedelta(minutes=1)
    except:
        fechamax = datetime.today() - timedelta(days=90)
except:
    # El test es NO OK -> lanzamos proceso de autorizacion
    print('Antes de nada, es necesario tu autorizacion-CHPP para recoger datos Hattrick!')
    print('Sigue las instruciones:')
    helper.get_auth(basedatos)
cur.close()

# Lanzamos MENU de la aplicacion
while True:
    print('\n')
    print(Back.WHITE + Fore.BLACK + 'Que quieres hacer?? ')
    print('     1.- Obtener datos de Hattrick')
    print('     2.- Enviar datos al servidor para enriquecer el estudio')
    print('     3.- Ver tus estadisticas')
    print('     4.- Salir\n')
    opcion = input(Back.WHITE + Fore.BLACK + '(por defecto 4) >> ')

    if opcion == '1':
        #Paso1 - Recuperar lista de partidos nuevos
        print('\n')
        print('Buscando partidos en www.hattrick.org... ')
        listaPartidos = bbdd.new_partidos(helper, basedatos, user_key, user_secret, fechamax)

        #Paso2 - Recuperar detalle de los partidos nuevos
        if len(listaPartidos) > 0:
            print('Recuperando los datos de los ',Back.WHITE + Fore.BLACK + str(len(listaPartidos)), Style.RESET_ALL + ' partidos nuevos en www.hattrick.org... ')
            print('Paciencia, puede tardar un poco..')
            for partido in listaPartidos:
                bbdd.get_partido(helper, basedatos, user_key, user_secret, partido)
            print(Back.GREEN + Fore.WHITE + 'Hecho!' + Style.RESET_ALL)

    elif opcion == '2':
        print('\n')
        print(Back.RED + Fore.WHITE + 'Perdón! Esta parte esta en contrucción' + Style.RESET_ALL)
        print('\n')

    elif opcion == '3':
        print('\n')
        print(Back.RED + Fore.WHITE + 'Perdón! Esta parte esta en contrucción' + Style.RESET_ALL)
        print('\n')

    elif opcion == '4': break
    elif len(opcion) < 1: break

    else:
        print('\n')
        print(Back.RED + Fore.WHITE + 'Perdón! Esta parte esta en contrucción' + Style.RESET_ALL)
        print('\n')
