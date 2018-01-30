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
print(Fore.GREEN + Back.BLACK + '''SE-BIGDATA v1.0.1''')
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
    print('Antes de nada, es necesario tu autorizacion-CHPP para recoger datos de www.hattrick.org')
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
    print('     3.- Ver tus estadisticas generales')
    print('     4.- Salir\n')
    opcion = input('(por defecto 4) >> ')

    if opcion == '1':
        # Paso0 - Miramos si hay partidos en la base y si hay miramos fecha del ultimo
        conn = sqlite3.connect(basedatos)
        cur = conn.cursor()
        if fechamax == 'Ningun partido en la base': fechamax = datetime(2017,12,20,0,0,0)
            # fechamax = datetime.today() - timedelta(days=90)
        cur.close()

        # Paso1 - Recuperamos lista de partidos nuevos
        print('\n')
        print('Buscando partidos en www.hattrick.org... ')
        print('Paciencia, puede tardar un poco (sobretodo la primera vez)..\n')
        num = 0
        for team in listaEquiposID:
            print('Para tu equipo <',Fore.YELLOW + Style.BRIGHT + str(listaEquiposNombre[num]),'>')
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
                print('Recuperando habilidades de tus jugadores implicados en eventos de los ',Back.WHITE + Fore.BLACK + Style.BRIGHT + str(len(listaPartidos)), Style.RESET_ALL + ' partidos nuevos encontrados.. \n')
                for partido in listaPartidos:
                    # habilidades jugadores
                    bbdd.get_habilidades(helper, basedatos, user_key, user_secret, partido)
            else:
                None

            num = num + 1

        print(Fore.GREEN + 'SE-Bigdata está ahora actualizada!!')

        conn = sqlite3.connect(basedatos)
        cur = conn.cursor()
        cur.execute( 'SELECT max(MatchDate) FROM partidos')
        fechamax = cur.fetchone()[0]
        cur.close()

        conn = sqlite3.connect(basedatos)
        cur = conn.cursor()
        cur.execute('UPDATE eventos SET SubSpecialty=(SELECT Specialty FROM jugadores WHERE PlayerID=eventos.SubjectPlayerID) WHERE SubSpecialty=-99')
        conn.commit()
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

        if numpartidos == 0:
            fechamax = 'Ningun partido en la base'

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
        if numpartidos == 0:
            print(Fore.RED + Style.BRIGHT + 'Pero antes de nada, deberiamos recuperar algun partido de www.hattrick.org... (opción 1)')
        else:
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

        if numpartidos == 0:
            fechamax = 'Ningun partido en la base'

        print('\nLa base de partidos tiene un tamaño de',Back.BLACK+Fore.GREEN+str(size),'KB y contiene:')
        print(Back.BLACK+Fore.GREEN+str(numpartidos),'  partidos, el mas reciente de: '+Back.BLACK+Fore.GREEN+fechamax)
        print(Back.BLACK+Fore.GREEN+str(numeventos),'  eventos especiales (con las habilidades de tus jugadores implicados, no las rivales)')
        print(Back.BLACK+Fore.GREEN+str(numjugadores),' jugadores (su especialidad y caracter)')
        print(Back.BLACK+Fore.GREEN+str(numlesiones),'  lesiones')
        print(Back.BLACK+Fore.GREEN+str(numsus),'  sustituciones')
        print(Back.BLACK+Fore.GREEN+str(numtarjetas),'  tarjetas\n')
        print(Style.BRIGHT+Fore.GREEN+'IMPORTANTE, recuerda que:')
        print('Las estadisticas mostradas a continuación son meramente orientativas.')
        print('En esta primera versión del programa, no se pondera por el numero de slots ocupados!!')
        print('Es decir, el % de aparicion mostrado no es fiable para ser extrapolado a nivel global.')
        print('Además, se necesita una base de partidos más grande para llegar a buenas conclusiones.')
        print('Pasa por la ',Style.BRIGHT+Fore.GREEN + 'federación "BigData"',' para ver/comentar/participar en los resultados del estudio en detalle\n')

        # Menu del estudio
        while True:

            if numpartidos == 0:
                print(Fore.RED + Style.BRIGHT + 'Pero antes de nada, deberiamos recuperar algun partido de www.hattrick.org... (opción 1)')
                break

            print('Que tipo de especialistas quieres ver?')
            print('     1.- Imprevisibles')
            print('     2.- Rápidos')
            print('     3.- Técnicos')
            print('     4.- Potentes')
            print('     5.- Extremos')
            print('     6.- Eventos de Equipo')
            print('     7.- Salir')
            selecion = input('(por defecto 7) >> ')

            if selecion == '1':

                conn = sqlite3.connect(basedatos)
                cur = conn.cursor()
                cur.execute('SELECT count(MatchID) as Partidos_e05 from (select distinct MatchID from alineacion_all where Specialty = 4 and Pos < 106 and Pos > 99)')
                Partidos_e05 = cur.fetchone()[0]
                cur.execute('SELECT sum(maxMin) from (select MatchID, max(Minutos) as maxMin from (select * from alineacion_all where Specialty = 4 and Pos < 106 and Pos > 99) group by MatchID)')
                Minutos_e05 = cur.fetchone()[0]
                Partidos05_PondMin = Minutos_e05 / 90
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 105')
                Gols05 = cur.fetchone()[0]
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 205')
                Fallos05 = cur.fetchone()[0]

                if Partidos05_PondMin == 0:
                    App = 0.0
                else:
                    App = ((Gols05+Fallos05) / Partidos05_PondMin) * 100
                if Gols05+Fallos05 == 0:
                    Con = 0.0
                else:
                    Con = ((Gols05) / (Gols05+Fallos05)) * 100

                print(Fore.YELLOW + Style.BRIGHT + '\nEv. Individual ID=05: Imprevisible Pase Largo - Porteros y defensas')
                print(Minutos_e05, 'minutos en',Partidos_e05, 'partidos, es decir, en', Fore.GREEN + str("%.2f" % Partidos05_PondMin), 'partidos reales:')
                print('Un total de',Fore.GREEN + str(Gols05+Fallos05),'eventos. Con', Fore.GREEN + str(Gols05),'goles.')
                print('Es decir un',Fore.GREEN + str("%.2f" % App),'% de aparicion y un',Fore.GREEN + str("%.2f" % Con),'% de conversion global.\n')

                cur.execute('SELECT count(MatchID) as Partidos_e06 from (select distinct MatchID from alineacion_all where Specialty = 4 and Pos > 105)')
                Partidos_e06 = cur.fetchone()[0]
                cur.execute('SELECT sum(maxMin) from (select MatchID, max(Minutos) as maxMin from (select * from alineacion_all where Specialty = 4 and Pos > 105) group by MatchID)')
                Minutos_e06 = cur.fetchone()[0]
                Partidos06_PondMin = Minutos_e06 / 90
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 106')
                Gols06 = cur.fetchone()[0]
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 206')
                Fallos06 = cur.fetchone()[0]

                if Partidos06_PondMin == 0:
                    App = 0.0
                else:
                    App = ((Gols06+Fallos06) / Partidos06_PondMin) * 100
                if Gols06+Fallos06 == 0:
                    Con = 0.0
                else:
                    Con = ((Gols06) / (Gols06+Fallos06)) * 100

                print(Fore.YELLOW + Style.BRIGHT + '\nEv. Individual ID=06: Imprevisible Anotación - Extremos, Inners y Delanteros')
                print(Minutos_e06, 'minutos en',Partidos_e06, 'partidos, es decir, en', Fore.GREEN + str("%.2f" % Partidos06_PondMin), 'partidos reales:')
                print('Un total de',Fore.GREEN + str(Gols06+Fallos06),'eventos. Con', Fore.GREEN + str(Gols06),'goles.')
                print('Es decir un',Fore.GREEN + str("%.2f" % App),'% de aparicion y un',Fore.GREEN + str("%.2f" % Con),'% de conversion global.\n')

                cur.execute('SELECT count(MatchID) as Partidos_e08 from (select distinct MatchID from alineacion_all where Specialty = 4 and Pos > 100)')
                Partidos_e08 = cur.fetchone()[0]
                cur.execute('SELECT sum(maxMin) from (select MatchID, max(Minutos) as maxMin from (select * from alineacion_all where Specialty = 4 and Pos > 100) group by MatchID)')
                Minutos_e08 = cur.fetchone()[0]
                Partidos08_PondMin = Minutos_e08 / 90
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 108')
                Gols08 = cur.fetchone()[0]
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 208')
                Fallos08 = cur.fetchone()[0]

                if Partidos08_PondMin == 0:
                    App = 0.0
                else:
                    App = ((Gols08+Fallos08) / Partidos08_PondMin) * 100
                if Gols08+Fallos08 == 0:
                    Con = 0.0
                else:
                    Con = ((Gols08) / (Gols08+Fallos08)) * 100

                print(Fore.YELLOW + Style.BRIGHT + '\nEv. Individual ID=08: Imprevisible - Todos menos Porteros')
                print(Minutos_e08, 'minutos en',Partidos_e08, 'partidos, es decir, en', Fore.GREEN + str("%.2f" % Partidos08_PondMin), 'partidos reales:')
                print('Un total de',Fore.GREEN + str(Gols08+Fallos08),'eventos. Con', Fore.GREEN + str(Gols08),'goles.')
                print('Es decir un',Fore.GREEN + str("%.2f" % App),'% de aparicion y un',Fore.GREEN + str("%.2f" % Con),'% de conversion global.\n')

                cur.execute('SELECT count(MatchID) as Partidos_e08 from (select distinct MatchID from alineacion_all where Specialty = 4 and Pos > 100 and Pos < 110 and Pos <> 106)')
                Partidos_e09 = cur.fetchone()[0]
                cur.execute('SELECT sum(maxMin) from (select MatchID, max(Minutos) as maxMin from (select * from alineacion_all where Specialty = 4 and Pos > 100 and Pos < 110 and Pos <> 106) group by MatchID)')
                Minutos_e09 = cur.fetchone()[0]
                Partidos09_PondMin = Minutos_e09 / 90
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 109')
                Gols09 = cur.fetchone()[0]
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 209')
                Fallos09 = cur.fetchone()[0]

                if Partidos09_PondMin == 0:
                    App = 0.0
                else:
                    App = ((Gols09+Fallos09) / Partidos09_PondMin) * 100
                if Gols09+Fallos09 == 0:
                    Con = 0.0
                else:
                    Con = ((Gols09) / (Gols09+Fallos09)) * 100

                print(Fore.YELLOW + Style.BRIGHT + '\nEv. Individual ID=09: Error Imprevisible - Defensas y Inners')
                print(Minutos_e09, 'minutos en',Partidos_e09, 'partidos, es decir, en', Fore.GREEN + str("%.2f" % Partidos09_PondMin), 'partidos reales:')
                print('Un total de',Fore.GREEN + str(Gols09+Fallos09),'eventos. Con', Fore.GREEN + str(Gols09),'goles.')
                print('Es decir un',Fore.GREEN + str("%.2f" % App),'% de aparicion y un',Fore.GREEN + str("%.2f" % Con),'% de conversion global.\n')

                cur.execute('SELECT count(MatchID) as Partidos_e25 from (select distinct MatchID from alineacion_all where Specialty = 4 and (Pos = 106 or Pos > 109))')
                Partidos_e25 = cur.fetchone()[0]
                cur.execute('SELECT sum(maxMin) from (select MatchID, max(Minutos) as maxMin from (select * from alineacion_all where Specialty = 4 and (Pos = 106 or Pos > 109)) group by MatchID)')
                Minutos_e25 = cur.fetchone()[0]
                Partidos25_PondMin = Minutos_e25 / 90
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 125')
                Gols25 = cur.fetchone()[0]
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 225')
                Fallos25 = cur.fetchone()[0]

                if Partidos25_PondMin == 0:
                    App = 0.0
                else:
                    App = ((Gols25+Fallos25) / Partidos25_PondMin) * 100
                if Gols25+Fallos25 == 0:
                    Con = 0.0
                else:
                    Con = ((Gols25) / (Gols25+Fallos25)) * 100

                print(Fore.YELLOW + Style.BRIGHT + '\nEv. Individual ID=25: Imprevisible en propia puerta - Extremos y Delanteros')
                print(Minutos_e25, 'minutos en',Partidos_e25, 'partidos, es decir, en', Fore.GREEN + str("%.2f" % Partidos25_PondMin), 'partidos reales:')
                print('Un total de',Fore.GREEN + str(Gols25+Fallos25),'eventos. Con', Fore.GREEN + str(Gols25),'goles.')
                print('Es decir un',Fore.GREEN + str("%.2f" % App),'% de aparicion y un',Fore.GREEN + str("%.2f" % Con),'% de conversion global.\n')

                cur.close()

            elif selecion == '2':
                conn = sqlite3.connect(basedatos)
                cur = conn.cursor()

                cur.execute('SELECT count(MatchID) as Partidos_e15 from (select distinct MatchID from alineacion_all where Specialty = 2 and Pos > 105)')
                Partidos_e15 = cur.fetchone()[0]
                cur.execute('SELECT sum(maxMin) from (select MatchID, max(Minutos) as maxMin from (select * from alineacion_all where Specialty = 2 and Pos > 105) group by MatchID)')
                Minutos_e15 = cur.fetchone()[0]
                Partidos15_PondMin = Minutos_e15 / 90
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 115')
                Gols15 = cur.fetchone()[0]
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 215')
                Fallos15 = cur.fetchone()[0]

                if Partidos15_PondMin == 0:
                    App = 0.0
                else:
                    App = ((Gols15+Fallos15) / Partidos15_PondMin) * 100
                if Gols15+Fallos15 == 0:
                    Con = 0.0
                else:
                    Con = ((Gols15) / (Gols15+Fallos15)) * 100

                print(Fore.YELLOW + Style.BRIGHT + '\nEv. Individual ID=15: Rápido + Anotación - Extremos, Inners y Delanteros')
                print(Minutos_e15, 'minutos en',Partidos_e15, 'partidos, es decir, en', Fore.GREEN + str("%.2f" % Partidos15_PondMin), 'partidos reales:')
                print('Un total de',Fore.GREEN + str(Gols15+Fallos15),'eventos. Con', Fore.GREEN + str(Gols15),'goles.')
                print('Es decir un',Fore.GREEN + str("%.2f" % App),'% de aparicion y un',Fore.GREEN + str("%.2f" % Con),'% de conversion global.\n')

                cur.execute('SELECT count(MatchID) as Partidos_e16 from (select distinct MatchID from alineacion_all where Specialty = 2 and Pos > 105)')
                Partidos_e16 = cur.fetchone()[0]
                cur.execute('SELECT sum(maxMin) from (select MatchID, max(Minutos) as maxMin from (select * from alineacion_all where Specialty = 2 and Pos > 105) group by MatchID)')
                Minutos_e16 = cur.fetchone()[0]
                if Minutos_e16 == None:
                    Partidos16_PondMin = 0
                else:
                    Partidos16_PondMin = Minutos_e16 / 90
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 116')
                Gols16 = cur.fetchone()[0]
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 216')
                Fallos16 = cur.fetchone()[0]

                if Partidos16_PondMin == 0:
                    App = 0.0
                else:
                    App = ((Gols16+Fallos16) / Partidos16_PondMin) * 100
                if Gols16+Fallos16 == 0:
                    Con = 0.0
                else:
                    Con = ((Gols16) / (Gols16+Fallos16)) * 100

                print(Fore.YELLOW + Style.BRIGHT + '\nEv. Individual ID=16: Rápido + Pases - Extremos, Inners y Delanteros')
                print(Minutos_e16, 'minutos en',Partidos_e16, 'partidos, es decir, en', Fore.GREEN + str("%.2f" % Partidos16_PondMin), 'partidos reales:')
                print('Un total de',Fore.GREEN + str(Gols16+Fallos16),'eventos. Con', Fore.GREEN + str(Gols16),'goles.')
                print('Es decir un',Fore.GREEN + str("%.2f" % App),'% de aparicion y un',Fore.GREEN + str("%.2f" % Con),'% de conversion global.\n')

                cur.close()

            elif selecion == '3':
                conn = sqlite3.connect(basedatos)
                cur = conn.cursor()

                # cur.execute('SELECT count(MatchID) as Partidos_e39 from (select distinct MatchID from alineacion_all_contrarios where Pos > 105 and Specialty = 1 and "Specialty:1" = 5)')
                # Partidos_e39 = cur.fetchone()[0]
                # cur.execute('SELECT sum (MaxMinutos) as Minutos_e39 from(select MatchID, max (Minutos) as MaxMinutos from (select MatchID, Pos, Specialty, "Specialty:1" as SpeContraria, Minutos from alineacion_all_contrarios where Pos > 105 and Specialty = 1 and "Specialty:1" = 5) group by MatchID)')
                # Minutos_e39 = cur.fetchone()[0]
                # if Minutos_e39 == None:
                #     Partidos39_PondMin = 0
                # else:
                #     Partidos39_PondMin = Minutos_e39 / 90
                # cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 139')
                # Gols39 = cur.fetchone()[0]
                # cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 239')
                # Fallos39 = cur.fetchone()[0]
                #
                # if Partidos39_PondMin == 0:
                #     App = 0.0
                # else:
                #     App = ((Gols39+Fallos39) / Partidos39_PondMin) * 100
                # if Gols39+Fallos39 == 0:
                #     Con = 0.0
                # else:
                #     Con = ((Gols39) / (Gols39+Fallos39)) * 100
                #
                # print(Fore.YELLOW + Style.BRIGHT + '\nEv. Individual ID=39: Técnico vs Cabezón - Extremos, Inners y Delanteros vs posición contraria')
                # print(Minutos_e39, 'minutos en',Partidos_e39, 'partidos, es decir, en', Fore.GREEN + str("%.2f" % Partidos39_PondMin), 'partidos reales:')
                # print('Un total de',Fore.GREEN + str(Gols39+Fallos39),'eventos. Con', Fore.GREEN + str(Gols39),'goles.')
                # print('Es decir un',Fore.GREEN + str("%.2f" % App),'% de aparicion y un',Fore.GREEN + str("%.2f" % Con),'% de conversion global.\n')

                cur.execute('SELECT count(MatchID) as Partidos_e39 from (select distinct MatchID from alineacion_all_contrarios_tec_cab where Pos > 105 and Specialty = 1 and "Specialty:1" = 5)')
                Partidos_e39 = cur.fetchone()[0]
                cur.execute('SELECT sum (MaxMinutos) as Minutos_e39 from(select MatchID, max (Minutos) as MaxMinutos from (select MatchID, Pos, Specialty, "Specialty:1" as SpeContraria, Minutos from alineacion_all_contrarios_tec_cab where Pos > 105 and Specialty = 1 and "Specialty:1" = 5) group by MatchID)')
                Minutos_e39 = cur.fetchone()[0]
                if Minutos_e39 == None:
                    Partidos39_PondMin = 0
                else:
                    Partidos39_PondMin = Minutos_e39 / 90
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 139')
                Gols39 = cur.fetchone()[0]
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 239')
                Fallos39 = cur.fetchone()[0]

                if Partidos39_PondMin == 0:
                    App = 0.0
                else:
                    App = ((Gols39+Fallos39) / Partidos39_PondMin) * 100
                if Gols39+Fallos39 == 0:
                    Con = 0.0
                else:
                    Con = ((Gols39) / (Gols39+Fallos39)) * 100

                print(Fore.YELLOW + Style.BRIGHT + '\nEv. Individual ID=39: Técnico vs Cabezón - Extremos, Inners y Delanteros vs posición contraria')
                print(Minutos_e39, 'minutos en',Partidos_e39, 'partidos, es decir, en', Fore.GREEN + str("%.2f" % Partidos39_PondMin), 'partidos reales:')
                print('Un total de',Fore.GREEN + str(Gols39+Fallos39),'eventos. Con', Fore.GREEN + str(Gols39),'goles.')
                print('Es decir un',Fore.GREEN + str("%.2f" % App),'% de aparicion y un',Fore.GREEN + str("%.2f" % Con),'% de conversion global.\n')

                cur.close()

            elif selecion == '4':
                # print(Fore.RED + '\nperdón, esta parte sigue en construccion\n')
                conn = sqlite3.connect(basedatos)
                cur = conn.cursor()

                cur.execute('SELECT count(MatchID) as Partidos_e90 from (select distinct MatchID from alineacion_all where Specialty = 3 and Pos > 110)')
                Partidos_e90 = cur.fetchone()[0]
                cur.execute('SELECT sum(maxMin) from (select MatchID, max(Minutos) as maxMin from (select * from alineacion_all where Specialty = 3 and Pos > 110) group by MatchID)')
                Minutos_e90 = cur.fetchone()[0]
                if Minutos_e90 == None:
                    Partidos90_PondMin = 0
                else:
                    Partidos90_PondMin = Minutos_e90 / 90
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 190')
                Gols90 = cur.fetchone()[0]
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 290')
                Fallos90 = cur.fetchone()[0]

                if Partidos90_PondMin == 0:
                    App = 0.0
                else:
                    App = ((Gols90+Fallos90) / Partidos90_PondMin) * 100
                if Gols90+Fallos90 == 0:
                    Con = 0.0
                else:
                    Con = ((Gols90) / (Gols90+Fallos90)) * 100

                print(Fore.YELLOW + Style.BRIGHT + '\nEv. Individual ID=90: Delantero Potente')
                print(Minutos_e90, 'minutos en',Partidos_e90, 'partidos, es decir, en', Fore.GREEN + str("%.2f" % Partidos90_PondMin), 'partidos reales:')
                print('Un total de',Fore.GREEN + str(Gols90+Fallos90),'eventos. Con', Fore.GREEN + str(Gols90),'goles.')
                print('Es decir un',Fore.GREEN + str("%.2f" % App),'% de aparicion y un',Fore.GREEN + str("%.2f" % Con),'% de conversion global.\n')


                cur.execute('SELECT count(MatchID) as Partidos_e310 from (select distinct MatchID from alineacion_all where Specialty = 3 and Pos > 106 and Pos < 110 )')
                Partidos_e310 = cur.fetchone()[0]
                cur.execute('SELECT sum(maxMin) from (select MatchID, max(Minutos) as maxMin from (select * from alineacion_all where Specialty = 3 and Pos > 106 and Pos < 110) group by MatchID)')
                Minutos_e310 = cur.fetchone()[0]
                if Minutos_e310 == None:
                    Partidos310_PondMin = 0
                else:
                    Partidos310_PondMin = Minutos_e310 / 90

                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 310')
                Gols310 = cur.fetchone()[0]

                if Partidos310_PondMin == 0:
                    App = 0.0
                else:
                    App = ((Gols310) / Partidos310_PondMin) * 100
                if Gols310 == 0:
                    Con = 0.0
                else:
                    Con = ((Gols310) / (Gols310)) * 100

                print(Fore.YELLOW + Style.BRIGHT + '\nEv. Individual ID=310: Inner Potente Corta ocasión')
                print(Minutos_e310, 'minutos en',Partidos_e310, 'partidos, es decir, en', Fore.GREEN + str("%.2f" % Partidos310_PondMin), 'partidos reales:')
                print('Un total de',Fore.GREEN + str(Gols310),'eventos.')
                print('Es decir un',Fore.GREEN + str("%.2f" % App),'% de aparicion.\n')


                cur.close()

            elif selecion == '5':
                conn = sqlite3.connect(basedatos)
                cur = conn.cursor()

                cur.execute('SELECT count(MatchID) as Partidos_e38 from (select distinct MatchID from alineacion_all where Pos = 106 or Pos = 110 and (Pos > 105 and Specialty=5))')
                Partidos_e38 = cur.fetchone()[0]
                cur.execute('SELECT sum(maxMin) from (select MatchID, max(Minutos) as maxMin from (select * from alineacion_all where Pos = 106 or Pos = 110 and (Pos > 105 and Specialty=5)) group by MatchID)')
                Minutos_e38 = cur.fetchone()[0]
                Partidos38_PondMin = Minutos_e38 / 90
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 137')
                Gols38 = cur.fetchone()[0]
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 237 and SubSpecialty = 5')
                Fallos38 = cur.fetchone()[0]

                if Partidos38_PondMin == 0:
                    App = 0.0
                else:
                    App = ((Gols38+Fallos38) / Partidos38_PondMin) * 100
                if Gols38+Fallos38 == 0:
                    Con = 0.0
                else:
                    Con = ((Gols38) / (Gols38+Fallos38)) * 100

                print(Fore.YELLOW + Style.BRIGHT + '\nEv. Individual ID=37: Extremos + Cabezon - Extremos')
                print(Minutos_e38, 'minutos en',Partidos_e38, 'partidos, es decir, en', Fore.GREEN + str("%.2f" % Partidos38_PondMin), 'partidos reales:')
                print('Un total de',Fore.GREEN + str(Gols38+Fallos38),'eventos. Con', Fore.GREEN + str(Gols38),'goles.')
                print('Es decir un',Fore.GREEN + str("%.2f" % App),'% de aparicion y un',Fore.GREEN + str("%.2f" % Con),'% de conversion global.\n')

                cur.execute('SELECT count(MatchID) as Partidos_e37 from (select distinct MatchID from alineacion_all where Pos = 106 or Pos = 110)')
                Partidos_e37 = cur.fetchone()[0]
                cur.execute('SELECT sum(maxMin) from (select MatchID, max(Minutos) as maxMin from (select * from alineacion_all where Pos = 106 or Pos = 110) group by MatchID)')
                Minutos_e37 = cur.fetchone()[0]
                Partidos37_PondMin = Minutos_e37 / 90
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 138')
                Gols37 = cur.fetchone()[0]
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 237 and SubSpecialty <> 5')
                Fallos37 = cur.fetchone()[0]

                if Partidos37_PondMin == 0:
                    App = 0.0
                else:
                    App = ((Gols37+Fallos37) / Partidos37_PondMin) * 100
                if Gols37+Fallos37 == 0:
                    Con = 0.0
                else:
                    Con = ((Gols37) / (Gols37+Fallos37)) * 100

                print(Fore.YELLOW + Style.BRIGHT + '\nEv. Individual ID=38: Extremos + Anotación - Extremos')
                print(Minutos_e37, 'minutos en',Partidos_e37, 'partidos, es decir, en', Fore.GREEN + str("%.2f" % Partidos37_PondMin), 'partidos reales:')
                print('Un total de',Fore.GREEN + str(Gols37+Fallos37),'eventos. Con', Fore.GREEN + str(Gols37),'goles.')
                print('Es decir un',Fore.GREEN + str("%.2f" % App),'% de aparicion y un',Fore.GREEN + str("%.2f" % Con),'% de conversion global.\n')


                cur.close()

            elif selecion == '6':
                conn = sqlite3.connect(basedatos)
                cur = conn.cursor()

                cur.execute('SELECT count(MatchID) as Partidos_e18 from (select distinct MatchID from alineacion_all)')
                Partidos_e18 = cur.fetchone()[0]
                cur.execute('SELECT sum(maxMin) from (select MatchID, max(Minutos) as maxMin from (select * from alineacion_all) group by MatchID)')
                Minutos_e18 = cur.fetchone()[0]
                Partidos18_PondMin = Minutos_e18 / 90
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 118')
                Gols18 = cur.fetchone()[0]
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 218')
                Fallos18 = cur.fetchone()[0]

                if Partidos18_PondMin == 0:
                    App = 0.0
                else:
                    App = ((Gols18+Fallos18) / Partidos18_PondMin) * 100
                if Gols18+Fallos18 == 0:
                    Con = 0.0
                else:
                    Con = ((Gols18) / (Gols18+Fallos18)) * 100

                print(Fore.YELLOW + Style.BRIGHT + '\nEv. Equipo ID=18: Corners + Anotación')
                print(Minutos_e18, 'minutos en',Partidos_e18, 'partidos, es decir, en', Fore.GREEN + str("%.2f" % Partidos18_PondMin), 'partidos reales:')
                print('Un total de',Fore.GREEN + str(Gols18+Fallos18),'eventos. Con', Fore.GREEN + str(Gols18),'goles.')
                print('Es decir un',Fore.GREEN + str("%.2f" % App),'% de aparicion y un',Fore.GREEN + str("%.2f" % Con),'% de conversion global.\n')

                cur.execute('SELECT count(MatchID) as Partidos_e19 from (select distinct MatchID from alineacion_all where Specialty = 5)')
                Partidos_e19 = cur.fetchone()[0]
                cur.execute('SELECT sum(maxMin) from (select MatchID, max(Minutos) as maxMin from (select * from alineacion_all where Specialty = 5) group by MatchID)')
                Minutos_e19 = cur.fetchone()[0]
                Partidos19_PondMin = Minutos_e19 / 90
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 119')
                Gols19 = cur.fetchone()[0]
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 219')
                Fallos19 = cur.fetchone()[0]

                if Partidos19_PondMin == 0:
                    App = 0.0
                else:
                    App = ((Gols19+Fallos19) / Partidos19_PondMin) * 100
                if Gols19+Fallos19 == 0:
                    Con = 0.0
                else:
                    Con = ((Gols19) / (Gols19+Fallos19)) * 100

                print(Fore.YELLOW + Style.BRIGHT + '\nEv. Equipo ID=19: Corners + Cabezones')
                print(Minutos_e19, 'minutos en',Partidos_e19, 'partidos, es decir, en', Fore.GREEN + str("%.2f" % Partidos19_PondMin), 'partidos reales:')
                print('Un total de',Fore.GREEN + str(Gols19+Fallos19),'eventos. Con', Fore.GREEN + str(Gols19),'goles.')
                print('Es decir un',Fore.GREEN + str("%.2f" % App),'% de aparicion y un',Fore.GREEN + str("%.2f" % Con),'% de conversion global.\n')

                cur.execute('SELECT count(MatchID) as Partidos_e35 from (select distinct MatchID from alineacion_all where Pos > 110)')
                Partidos_e35 = cur.fetchone()[0]
                cur.execute('SELECT sum(maxMin) from (select MatchID, max(Minutos) as maxMin from (select * from alineacion_all where Pos > 110) group by MatchID)')
                Minutos_e35 = cur.fetchone()[0]
                Partidos35_PondMin = Minutos_e35 / 90
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 135')
                Gols35 = cur.fetchone()[0]
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 235')
                Fallos35 = cur.fetchone()[0]

                if Partidos35_PondMin == 0:
                    App = 0.0
                else:
                    App = ((Gols35+Fallos35) / Partidos35_PondMin) * 100
                if Gols35+Fallos35 == 0:
                    Con = 0.0
                else:
                    Con = ((Gols35) / (Gols35+Fallos35)) * 100

                print(Fore.YELLOW + Style.BRIGHT + '\nEv. Equipo ID=35: Delantero Experimentado - Delanteros')
                print(Minutos_e35, 'minutos en',Partidos_e35, 'partidos, es decir, en', Fore.GREEN + str("%.2f" % Partidos35_PondMin), 'partidos reales:')
                print('Un total de',Fore.GREEN + str(Gols35+Fallos35),'eventos. Con', Fore.GREEN + str(Gols35),'goles.')
                print('Es decir un',Fore.GREEN + str("%.2f" % App),'% de aparicion y un',Fore.GREEN + str("%.2f" % Con),'% de conversion global.\n')

                cur.execute('SELECT count(MatchID) as Partidos_e36 from (select distinct MatchID from alineacion_all where Pos > 100 and Pos < 106)')
                Partidos_e36 = cur.fetchone()[0]
                cur.execute('SELECT sum(maxMin) from (select MatchID, max(Minutos) as maxMin from (select * from alineacion_all where Pos > 100 and Pos < 106) group by MatchID)')
                Minutos_e36 = cur.fetchone()[0]
                Partidos36_PondMin = Minutos_e36 / 90
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 136')
                Gols36 = cur.fetchone()[0]
                cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 236')
                Fallos36 = cur.fetchone()[0]

                if Partidos36_PondMin == 0:
                    App = 0.0
                else:
                    App = ((Gols36+Fallos36) / Partidos36_PondMin) * 100
                if Gols36+Fallos36 == 0:
                    Con = 0.0
                else:
                    Con = ((Gols36) / (Gols36+Fallos36)) * 100

                print(Fore.YELLOW + Style.BRIGHT + '\nEv. Equipo ID=36: Defensa No-Experimentado - Defensas')
                print(Minutos_e36, 'minutos en',Partidos_e36, 'partidos, es decir, en', Fore.GREEN + str("%.2f" % Partidos36_PondMin), 'partidos reales:')
                print('Un total de',Fore.GREEN + str(Gols36+Fallos36),'eventos. Con', Fore.GREEN + str(Gols36),'goles.')
                print('Es decir un',Fore.GREEN + str("%.2f" % App),'% de aparicion y un',Fore.GREEN + str("%.2f" % Con),'% de conversion global.\n')

                cur.close()


            elif selecion == '7':
                break

            elif len(selecion) < 1:
                break


    elif opcion == '4':
        print(Fore.YELLOW + Style.BRIGHT + '\nHasta la proxima!\n')
        break
    elif len(opcion) < 1:
        print(Fore.YELLOW + Style.BRIGHT + '\nHasta la proxima!\n')
        break

    else:
        print(Back.RED + Fore.WHITE + '\nUps, no he entendido que quieres hacer..prueba otra vez' + Style.RESET_ALL)
