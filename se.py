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
import send
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import sqlite3
import os
from colorama import init, Fore, Back, Style

# print Bienvenida
init(autoreset=True)
print('\n')
print(Fore.GREEN + Back.BLACK + '''SE-BIGDATA v0.0''')
print('Copyright (C) 2017, "uny11"\nEste sencillo programa es software libre bajo la licencia GPL-v3')
print('\n')
print(Fore.GREEN + 'Bienvenido y Gracias por participar en este estudio!')
print('y no dudes en reportar algun fallo o duda (uny11)\n')

#Iniciamos base de datos de SE-Bigdata
bbddauth = 'auth.sqlite'
basedatos = 'bigdata.sqlite'
bbdd.init_base(basedatos, bbddauth)

# Iniciamos claves y funciones para acceder a los recursos CHPP de la API de Hatrick
helper = CHPPhelp()

# Buscamos si la App tiene la autorizacion CHPP del usuario
conn = sqlite3.connect(bbddauth)
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
    helper.get_auth(bbddauth)

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
conn = sqlite3.connect(basedatos)
cur = conn.cursor()
cur.execute( 'SELECT max(MatchDate) FROM partidos')
fechamax = cur.fetchone()[0]
cur.close()

# Lanzamos MENU de la aplicacion
while True:
    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat('bigdata.sqlite')
    size = size/1024
    print('\n')
    print(Fore.GREEN + 'Que quieres hacer', Fore.YELLOW + Style.BRIGHT+str(user),Fore.GREEN + '?\n')
    if fechamax == None: fechamax = 'Ningun partido en la base'
    print('     1.- Recuperar datos de Hattrick - Ultimo partido recuperado: '+Fore.GREEN+fechamax)
    print('     2.- Enviar datos al servidor para enriquecer el estudio')
    print('     3.- Ver tus estadisticas')
    print('     4.- Salir\n')
    opcion = input('(por defecto 4) >> ')

    if opcion == '1':
        # Paso0 - Miramos si hay partidos en la base y si hay miramos fecha del ultimo
        conn = sqlite3.connect(basedatos)
        cur = conn.cursor()
        if fechamax == None: fechamax = datetime.today() - timedelta(days=30)
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
                print('Recuperando datos de los ',Back.WHITE + Fore.BLACK + Style.BRIGHT + str(len(listaPartidos)), Style.RESET_ALL + ' partidos nuevos de www.hattrick.org...')
                for partido in listaPartidos:
                    # detalle partido, alineacion y sustituciones
                    bbdd.get_partido(helper, basedatos, user_key, user_secret, partido)
            else:
                None

            # Paso 1.3 - Recuperamos habilidades de jugadores implicados en eventos
            if len(listaPartidos) > 0:
                print('Recuperando habilidades de nuestros jugadores implicados en eventos en los ',Back.WHITE + Fore.BLACK + Style.BRIGHT + str(len(listaPartidos)), Style.RESET_ALL + ' partidos nuevos de www.hattrick.org... \n')
                for partido in listaPartidos:
                    # habilidades jugadores
                    bbdd.get_habilidades(helper, basedatos, user_key, user_secret, partido)
            else:
                None

            num = num + 1

        print(Fore.GREEN + 'SE-Bigdata ha sido actualizado con éxito!!')

        conn = sqlite3.connect(basedatos)
        cur = conn.cursor()
        cur.execute( 'SELECT max(MatchDate) FROM partidos')
        fechamax = cur.fetchone()[0]
        cur.close()

    elif opcion == '2':
        # Recuperamos algunos datos de la base de datos
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat('bigdata.sqlite')
        size = size/1024
        conn = sqlite3.connect(basedatos)
        cur = conn.cursor()
        cur.execute('SELECT count(MatchID) FROM partidos')
        numpartidos = cur.fetchone()[0]
        cur.execute('SELECT count(SubPorteria) FROM eventos')
        numeventos = cur.fetchone()[0]
        cur.execute('SELECT count(PlayerID) FROM jugadores')
        numjugadores = cur.fetchone()[0]
        cur.execute('SELECT count(MatchID) FROM lesiones')
        numlesiones = cur.fetchone()[0]
        cur.execute('SELECT count(MatchID) FROM sustituciones')
        numsus = cur.fetchone()[0]
        cur.execute('SELECT count(MatchID) FROM tarjetas')
        numtarjetas = cur.fetchone()[0]
        cur.execute( 'SELECT max(MatchDate) FROM partidos')
        fechamax = cur.fetchone()[0]
        cur.close()

        print('\n')
        print('Vamos a enviar el archivo '+Back.BLACK+Fore.GREEN+'"bigdata.sqlite"'+Style.RESET_ALL+' al servidor.')
        print('Este archivo es la base de datos generada por SE-Bigdata con toda la información recogida de Hattrick.\n')
        print('La base tiene un tamaño de',Back.BLACK+Fore.GREEN+str(size),'KB y contiene:')
        print(Back.BLACK+Fore.GREEN+str(numpartidos),'  partidos, el mas reciente de: '+Back.BLACK+Fore.GREEN+fechamax)
        print(Back.BLACK+Fore.GREEN+str(numeventos),'  eventos especiales (con las habilidades de tus jugadores implicados, no las rivales)')
        print(Back.BLACK+Fore.GREEN+str(numjugadores),' jugadores (su especialidad y caracter)')
        print(Back.BLACK+Fore.GREEN+str(numlesiones),'  lesiones')
        print(Back.BLACK+Fore.GREEN+str(numsus),'  sustituciones')
        print(Back.BLACK+Fore.GREEN+str(numtarjetas),'  tarjetas\n')
        print('Recuerda que si tienes conocimientos de "SQLite" puedes abrir dicho archivo para "jugar" con tus datos xDDD')
        print('Por ejemplo, con la aplicacion gratuita "DB Browser", la puedes encontrar aqui: http://sqlitebrowser.org/ \n')
        print('Por otro lado, solo comentar que '+Fore.RED+Back.WHITE+Style.BRIGHT+'NO'+Style.RESET_ALL+' se envian tu claves personales CHPP.')
        print('Estas claves se encuentran a salvo en otro archivo (auth.sqlite) y no se enviaran\n')

        print('Enviamos pues '+Fore.GREEN+'"bigdata.sqlite"'+Style.RESET_ALL+' al servidor (s/n)?')
        seguir = input('(por defecto n) >> ')
        if seguir == 's' or seguir == 'S':
            send.enviar_datos(basedatos, user)
            print(Back.GREEN + Fore.BLACK + 'Envio completado con éxito!!' + Style.RESET_ALL)
            print(Fore.GREEN+'Muchas Gracias por participar!')
        else:
            print('\nOk, pues mejor en otro momento..')

    elif opcion == '3':

        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat('bigdata.sqlite')
        size = size/1024
        conn = sqlite3.connect(basedatos)
        cur = conn.cursor()
        cur.execute('SELECT count(MatchID) FROM partidos')
        numpartidos = cur.fetchone()[0]
        cur.execute('SELECT count(SubPorteria) FROM eventos')
        numeventos = cur.fetchone()[0]
        cur.execute('SELECT count(PlayerID) FROM jugadores')
        numjugadores = cur.fetchone()[0]
        cur.execute('SELECT count(MatchID) FROM lesiones')
        numlesiones = cur.fetchone()[0]
        cur.execute('SELECT count(MatchID) FROM sustituciones')
        numsus = cur.fetchone()[0]
        cur.execute('SELECT count(MatchID) FROM tarjetas')
        numtarjetas = cur.fetchone()[0]
        cur.execute( 'SELECT max(MatchDate) FROM partidos')
        fechamax = cur.fetchone()[0]
        cur.close()

        print('\n')
        print(Back.RED + Fore.WHITE + 'Perdón! Esta parte sigue esta en contrucción\n' + Style.RESET_ALL)
        print('De momento, solo te puedo decir que:')
        print('La base de partidos tiene un tamaño de',Back.BLACK+Fore.GREEN+str(size),'KB y contiene:')
        print(Back.BLACK+Fore.GREEN+str(numpartidos),'  partidos, el mas reciente de: '+Back.BLACK+Fore.GREEN+fechamax)
        print(Back.BLACK+Fore.GREEN+str(numeventos),'  eventos especiales (con las habilidades de tus jugadores implicados, no las rivales)')
        print(Back.BLACK+Fore.GREEN+str(numjugadores),' jugadores (su especialidad y caracter)')
        print(Back.BLACK+Fore.GREEN+str(numlesiones),'  lesiones')
        print(Back.BLACK+Fore.GREEN+str(numsus),'  sustituciones')
        print(Back.BLACK+Fore.GREEN+str(numtarjetas),'  tarjetas\n')

    elif opcion == '4':
        print(Fore.YELLOW + Style.BRIGHT + '\nHasta la proxima!\n')
        break
    elif len(opcion) < 1:
        print(Fore.YELLOW + Style.BRIGHT + '\nHasta la proxima!\n')
        break

    else:
        print(Back.RED + Fore.WHITE + '\nUps, no he entendido que quieres hacer..prueba otra vez' + Style.RESET_ALL)
