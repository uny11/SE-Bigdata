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

    # tabla info del user
    cur.execute('''
                CREATE TABLE IF NOT EXISTS info
                (id INTEGER PRIMARY KEY, idHT INTEGER, type TEXT, descripcion TEXT)
                ''')

    # tabla partidos
    cur.execute('''
                CREATE TABLE IF NOT EXISTS partidos
                (MatchID INTEGER PRIMARY KEY, MatchType INTEGER, MatchDate TEXT, HomeTeamID INTEGER,
                HomeGoals INTEGER, AwayTeamID INTEGER, AwayGoals INTEGER, TacticTypeHome INTEGER,
                TacticSkillHome INTEGER, TacticTypeAway INTEGER, TacticSkillAway INTEGER, expulsiones INTEGER,
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

    # tabla tarjetas
    cur.execute('''
                CREATE TABLE IF NOT EXISTS tarjetas
                (MatchID INTEGER, IndexTarjeta INTEGER, PlayerID INTEGER, TeamID INTEGER, BookingType INTEGER, BookingMinute INTEGER,
                UNIQUE(MatchID, IndexTarjeta))
                ''')

    # tabla lesiones
    cur.execute('''
                CREATE TABLE IF NOT EXISTS lesiones
                (MatchID INTEGER, IndexInjury INTEGER, PlayerID INTEGER, TeamID INTEGER, InjuryType INTEGER, InjuryMinute INTEGER,
                UNIQUE(MatchID, IndexInjury))
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
                (PlayerID INTEGER PRIMARY KEY, Agreeability INTEGER, Aggressiveness INTEGER, Honesty INTEGER, Leadership INTEGER, Specialty INTEGER)
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
        # Recuperamos jugadores actuales de los equipos home team
        xmljug = helper.request_resource_with_key(  user_key,
                                                    user_secret,
                                                    'players',
                                                    {
                                                     'version' : 2.3,
                                                     'teamID' : teamidHome
                                                    }
                                                 )
        rootjug = ET.fromstring(xmljug)
        for player in rootjug.findall('Team/PlayerList/Player'):
            idplayer = player.find('PlayerID').text
            agree = player.find('Agreeability').text
            aggre = player.find('Aggressiveness').text
            hones = player.find('Honesty').text
            leade = player.find('Leadership').text
            speci = player.find('Specialty').text
            try:
                cur.execute('INSERT INTO jugadores (PlayerID, Agreeability, Aggressiveness, Honesty, Leadership, Specialty) VALUES (?, ?, ?, ?, ?, ?)',
                (idplayer, agree, aggre, hones, leade, speci))
            except:
                continue
        # Recuperamos jugadores actuales de los equipos away team
        xmljug = helper.request_resource_with_key(  user_key,
                                                    user_secret,
                                                    'players',
                                                    {
                                                     'version' : 2.3,
                                                     'teamID' : teamidAway
                                                    }
                                                 )
        rootjug = ET.fromstring(xmljug)
        for player in rootjug.findall('Team/PlayerList/Player'):
            idplayer = player.find('PlayerID').text
            agree = player.find('Agreeability').text
            aggre = player.find('Aggressiveness').text
            hones = player.find('Honesty').text
            leade = player.find('Leadership').text
            speci = player.find('Specialty').text
            try:
                cur.execute('INSERT INTO jugadores (PlayerID, Agreeability, Aggressiveness, Honesty, Leadership, Specialty) VALUES (?, ?, ?, ?, ?, ?)',
                (idplayer, agree, aggre, hones, leade, speci))
            except:
                continue
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
        expulsiones = 0
        for target in match.findall('Bookings/Booking'):
            try:
                indextarget = target.get("Index")
                idplayer = target.find('BookingPlayerID').text
                idteam = target.find('BookingTeamID').text
                typebooking = target.find('BookingType').text
                if typebooking == '2': expulsiones = 1
                minutebooking = target.find('BookingMinute').text
                cur.execute('''INSERT INTO tarjetas (MatchID, IndexTarjeta, PlayerID, TeamID, BookingType, BookingMinute)
                            VALUES (?, ?, ?, ?, ?, ?)''', (idpartido, indextarget, idplayer, idteam, typebooking, minutebooking))
            except:
                None
        lesiones = 0
        for inj in match.findall('Injuries/Injury'):
            try:
                indexinjury = inj.get("Index")
                idplayer = inj.find('InjuryPlayerID').text
                idteam = inj.find('InjuryTeamID').text
                typeinjury = inj.find('InjuryType').text
                if typeinjury == '2': lesiones = 1
                minuteinjury = inj.find('InjuryMinute').text
                cur.execute('''INSERT INTO lesiones (MatchID, IndexInjury, PlayerID, TeamID, InjuryType, InjuryMinute)
                            VALUES (?, ?, ?, ?, ?, ?)''',(idpartido, indexinjury, idplayer, idteam, typeinjury, minuteinjury))
            except:
                None
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
                    expulsiones=?, lesiones=?, PossessionFirstHalfHome=?, PossessionFirstHalfAway=?, PossessionSecondHalfHome=?,
                    PossessionSecondHalfAway=?, RatingIndirectSetPiecesDefHome=?, RatingIndirectSetPiecesAttHome=?,
                    RatingIndirectSetPiecesDefAway=?, RatingIndirectSetPiecesAttAway=? WHERE MatchID= ?''',
                    (typetactichome, skilltactichome, typetacticaway, skilltacticaway, expulsiones, lesiones, homeFpos, awayFpos, homeSpos, awaySpos, ratIndDefhome, ratIndAtthome, ratIndDefaway, ratIndAttaway, idpartido))
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
    hteamname = root.find('HomeTeam/HomeTeamName').text
    ateamid = root.find('AwayTeam/AwayTeamID').text
    ateamname = root.find('AwayTeam/AwayTeamName').text
    teamNamelineaup = root.find('Team/TeamName').text
    if hteamname == teamNamelineaup:
        teamrole = 1
        rival = ateamid
    if ateamname == teamNamelineaup:
        teamrole = 2
        rival = hteamid
    for player in root.findall('Team/StartingLineup/Player'):
        idplayer = player.find('PlayerID').text
        idrole = player.find('RoleID').text
        try:
            cur.execute('''INSERT INTO alineacion (MatchID, RoleTeam, RoleID, PlayerID)
                        VALUES (?, ?, ?, ?)''', (idpartido, teamrole, idrole, idplayer))
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
        except:
            continue

    conn.commit()
    cur.close()
