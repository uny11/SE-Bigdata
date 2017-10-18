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

import sqlite3
from  chpp import CHPPhelp
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from colorama import init, Fore, Back, Style

def init_base(base):
    # Creamos las tablas necesarias sino estan creadas
    conn = sqlite3.connect(base)
    cur = conn.cursor()

    # tabla keys
    cur.execute('''
                CREATE TABLE IF NOT EXISTS keys
                (id INTEGER PRIMARY KEY, key TEXT)
                ''')
    try:
        cur.execute('SELECT key FROM keys WHERE id = 1')
        test = cur.fetchone()[0]
    except:
        cur.execute('INSERT INTO keys (id,key) VALUES (?,?)', (1,'1Pg9hSfo5mkli2zaT8Hprr'))
        cur.execute('INSERT INTO keys (id,key) VALUES (?,?)', (2,'ERhrDhuV2uIEHG75QtHnHXDrOOYMixXzBS1V9yy3EZ6'))
        conn.commit()

    # tabla info del user
    cur.execute('''
                CREATE TABLE IF NOT EXISTS info
                (id INTEGER PRIMARY KEY, type TEXT, descripcion TEXT)
                ''')

    # tabla partidos
    cur.execute('''
                CREATE TABLE IF NOT EXISTS partidos
                (MatchID INTEGER PRIMARY KEY, MatchType INTEGER, MatchDate TEXT, HomeTeamID INTEGER,
                HomeGoals INTEGER, AwayTeamID INTEGER, AwayGoals INTEGER, TacticTypeHome INTEGER,
                TacticSkillHome INTEGER, TacticTypeAway INTEGER, TacticSkillAway INTEGER, tarjetas INTEGER,
                lesiones INTEGER, PossessionFirstHalfHome INTEGER,
                PossessionFirstHalfAway INTEGER, PossessionSecondHalfHome INTEGER, PossessionSecondHalfAway INTEGER,
                RatingIndirectSetPiecesDefHome INTEGER, RatingIndirectSetPiecesAttHome INTEGER, RatingIndirectSetPiecesDefAway INTEGER,
                RatingIndirectSetPiecesAttAway INTEGER)
                ''')

    # tabla eventos
    cur.execute('''
                CREATE TABLE IF NOT EXISTS eventos
                (MatchID INTEGER, IndexEv INTEGER, Minute INTEGER, EventTypeID INTEGER,
                SubjectTeamID INTEGER, SubjectPlayerID INTEGER, ObjectPlayerID INTEGER, SubPorteria INTEGER,
                SubDefensa INTEGER, SubJugadas INTEGER, SubLateral INTEGER, SubPases INTEGER,
                SubAnotacion INTEGER, SubXP INTEGER, SubFidelidad INTEGER, SubForma INTEGER,
                SubResistencia INTEGER, ObjPorteria INTEGER, ObjDefensa INTEGER,
                ObjJugadas INTEGER, ObjLateral INTEGER, ObjPases INTEGER,
                ObjAnotacion INTEGER, ObjXP INTEGER, ObjFidelidad INTEGER, ObjForma INTEGER, ObjResistencia INTEGER,
                UNIQUE(MatchID, IndexEv))
                ''')

    # tabla alineacion
    cur.execute('''
                CREATE TABLE IF NOT EXISTS alineacion
                (MatchID INTEGER, RoleTeam INTEGER, RoleID INTEGER, PlayerID INTEGER,
                UNIQUE(MatchID, RoleTeam, RoleID))
                ''')

    # tabla sustituciones
    cur.execute('''
                CREATE TABLE IF NOT EXISTS sustituciones
                (MatchID INTEGER, TeamID INTEGER, SubjectPlayerID INTEGER, ObjectPlayerID INTEGER, NewPositionId INTEGER, MatchMinute INTEGER,
                UNIQUE(MatchID, TeamID, SubjectPlayerID))
                ''')

    # tabla jugadores
    cur.execute('''
                CREATE TABLE IF NOT EXISTS jugadores
                (PlayerID INTEGER PRIMARY KEY, Agreeability INTEGER, Aggressiveness INTEGER, Honesty INTEGER, Leadership INTEGER, Specialty INTEGER))
                ''')

    cur.close()

def new_partidos(helper, base, user_key, user_secret, fecha, team):
    # Peticion a la API
    xmldoc = helper.request_resource_with_key(  user_key,
                                                user_secret,
                                                'matchesarchive',
                                                {
                                                 'version' : 1.3,
                                                 'teamID' : team,
                                                 'isYouth' : 'false',
                                                 'FirstMatchDate' : fecha
                                                 #LastMatchDate no especificada, coge 3 temporadas maximo
                                                }
                                             )
    #Guardamos la lista de partidos en la BBDD (file=matchsarchive)
    conn = sqlite3.connect(base)
    cur = conn.cursor()

    countMatchNuevos = 0
    countMatchBBDD = 0
    listaPartidosNuevos = []

    root = ET.fromstring(xmldoc)
    for match in root.findall('Team/MatchList/Match'):
        idmatch = match.find('MatchID').text
        typematch = match.find('MatchType').text
        datematch = match.find('MatchDate').text
        goalshome = match.find('HomeGoals').text
        goalsaway = match.find('AwayGoals').text
        teamidHome= match.find('HomeTeam/HomeTeamID').text
        teamidAway = match.find('AwayTeam/AwayTeamID').text
        try:
            cur.execute('INSERT INTO partidos (MatchID, MatchType, MatchDate, HomeTeamID, HomeGoals, AwayTeamID, AwayGoals) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (idmatch, typematch, datematch, teamidHome, goalshome, teamidAway, goalsaway))
            countMatchNuevos = countMatchNuevos + 1
            listaPartidosNuevos.append(idmatch)
        except:
            countMatchBBDD = countMatchBBDD + 1
    conn.commit()
    cur.close()
    init()
    print(Back.GREEN + Fore.WHITE + str(countMatchNuevos), Style.RESET_ALL + ' partidos nuevos han sido encontrados!')
    print(countMatchBBDD, ' partidos encontrados ya existian en SE-Bigdata')
    print('\n')

    return listaPartidosNuevos

def get_partido(helper, base, user_key, user_secret, idpartido):
    global rival
    global teamrole
    #Consulta a la API
    xmldoc = helper.request_resource_with_key(     user_key,
                                                   user_secret,
                                                   'matchdetails',
                                                   {
                                                    'version' : 2.9,
                                                    'matchEvents' : 'true',
                                                    'matchID' : idpartido
                                                   }
                                                  )
    root = ET.fromstring(xmldoc)

    # Guardamos la info ordenadamente dentro la base de datos de la App
    conn = sqlite3.connect(base)
    cur = conn.cursor()

    for match in root.findall('Match'):
        typetactichome = match.find('HomeTeam/TacticType').text
        skilltactichome = match.find('HomeTeam/TacticSkill').text
        typetacticaway = match.find('AwayTeam/TacticType').text
        skilltacticaway = match.find('AwayTeam/TacticSkill').text
        try:
            test = match.find('Bookings/Booking/BookingPlayerID').text
            tarjetas = 1
        except:
            tarjetas = 0
        try:
            test = match.find('Injuries/Injury/InjuryPlayerID').text
            lesiones = 1
        except:
            lesiones = 0
        homeFpos = match.find('PossessionFirstHalfHome').text
        awayFpos = match.find('PossessionFirstHalfAway').text
        homeSpos = match.find('PossessionSecondHalfHome').text
        awaySpos = match.find('PossessionSecondHalfAway').text
        ratIndDefhome = match.find('HomeTeam/RatingIndirectSetPiecesDef').text
        ratIndAtthome = match.find('HomeTeam/RatingIndirectSetPiecesAtt').text
        ratIndDefaway = match.find('AwayTeam/RatingIndirectSetPiecesDef').text
        ratIndAttaway = match.find('AwayTeam/RatingIndirectSetPiecesAtt').text
        try:
            cur.execute('''UPDATE partidos SET TacticTypeHome=?, TacticSkillHome=?, TacticTypeAway=?, TacticSkillAway=?,
                    tarjetas=?, lesiones=?, PossessionFirstHalfHome=?, PossessionFirstHalfAway=?, PossessionSecondHalfHome=?,
                    PossessionSecondHalfAway=?, RatingIndirectSetPiecesDefHome=?, RatingIndirectSetPiecesAttHome=?,
                    RatingIndirectSetPiecesDefAway=?, RatingIndirectSetPiecesAttAway=? WHERE MatchID= ?''',
                    (typetactichome, skilltactichome, typetacticaway, skilltacticaway, tarjetas, lesiones, homeFpos, awayFpos, homeSpos, awaySpos, ratIndDefhome, ratIndAtthome, ratIndDefaway, ratIndAttaway, idpartido))
            conn.commit()
        except:
            continue

    for event in root.findall('Match/EventList/Event'):
        indexevent = event.get("Index")
        minute = event.find('Minute').text
        idtypeevent = event.find('EventTypeID').text
        subteam = event.find('SubjectTeamID').text
        subplayer = event.find('SubjectPlayerID').text
        objplayer = event.find('ObjectPlayerID').text
        try:
            cur.execute('''INSERT INTO eventos (MatchID, IndexEv, Minute, EventTypeID, SubjectTeamID, SubjectPlayerID, ObjectPlayerID)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', (idpartido, indexevent, minute, idtypeevent, subteam, subplayer, objplayer))
            conn.commit()
        except:
            continue

    xmldoc = helper.request_resource_with_key(     user_key,
                                                   user_secret,
                                                   'matchlineup',
                                                   {
                                                    'version' : 2.0,
                                                    'matchID' : idpartido
                                                   }
                                                  )
    root = ET.fromstring(xmldoc)

    hteamid = root.find('HomeTeam/HomeTeamID').text
    ateamid = root.find('AwayTeam/AwayTeamID').text
    teamidlineaup = root.find('Team/TeamID').text
    if hteamid == teamidlineaup:
        teamrole = 1
        rival = ateamid
    if ateamid == teamidlineaup:
        teamrole = 2
        rival = hteamid
    for player in root.findall('Team/StartingLineup/Player'):
        idplayer = player.find('PlayerID').text
        idrole = player.find('RoleID').text
        try:
            cur.execute('''INSERT INTO alineacion (MatchID, RoleTeam, RoleID, PlayerID)
                        VALUES (?, ?, ?, ?)''', (idpartido, teamrole, idrole, idplayer))
            conn.commit()
        except:
            continue

    for sus in root.findall('Team/Substitutions/Substitution'):
        idteam = sus.find('TeamID').text
        subplaid = sus.find('SubjectPlayerID').text
        objplaid = sus.find('ObjectPlayerID').text
        minutematch = sus.find('MatchMinute').text
        posid = sus.find('NewPositionId').text
        try:
            cur.execute('''INSERT INTO sustituciones (MatchID, TeamID, SubjectPlayerID, ObjectPlayerID, MatchMinute, NewPositionId)
                        VALUES (?, ?, ?, ?, ?, ?)''', (idpartido, idteam, subplaid, objplaid, minutematch, posid))
            conn.commit()
        except:
            continue

    xmldoc = helper.request_resource_with_key(   user_key,
                                                 user_secret,
                                                 'matchlineup',
                                                   {
                                                    'version' : 2.0,
                                                    'matchID' : idpartido,
                                                    'teamID' : rival
                                                   }
                                             )
    root = ET.fromstring(xmldoc)
    if teamrole == 1:
        teamrole = 2
    else:
        teamrole = 1
    for player in root.findall('Team/StartingLineup/Player'):
        idplayer = player.find('PlayerID').text
        idrole = player.find('RoleID').text
        try:
            cur.execute('''INSERT INTO alineacion (MatchID, RoleTeam, RoleID, PlayerID)
                        VALUES (?, ?, ?, ?)''', (idpartido, teamrole, idrole, idplayer))
            conn.commit()
        except:
            continue

    for sus in root.findall('Team/Substitutions/Substitution'):
        idteam = sus.find('TeamID').text
        subplaid = sus.find('SubjectPlayerID').text
        objplaid = sus.find('ObjectPlayerID').text
        minutematch = sus.find('MatchMinute').text
        posid = sus.find('NewPositionId').text
        try:
            cur.execute('''INSERT INTO sustituciones (MatchID, TeamID, SubjectPlayerID, ObjectPlayerID, MatchMinute, NewPositionId)
                        VALUES (?, ?, ?, ?, ?, ?)''', (idpartido, idteam, subplaid, objplaid, minutematch, posid))
            conn.commit()
        except:
            continue

    cur.close()
