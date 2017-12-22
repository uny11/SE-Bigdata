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

def init_base(baseprincipal, baseauth):
    # Creamos las tablas necesarias sino estan creadas
    conn = sqlite3.connect(baseprincipal)
    conn2 = sqlite3.connect(baseauth)
    cur = conn.cursor()
    cur2 = conn2.cursor()

    # tabla keys
    cur2.execute('''
                CREATE TABLE IF NOT EXISTS keys
                (id INTEGER PRIMARY KEY, key TEXT)
                ''')

    # tabla info del user
    cur2.execute('''
                CREATE TABLE IF NOT EXISTS info
                (id INTEGER PRIMARY KEY, idHT INTEGER, type TEXT, descripcion TEXT)
                ''')

    # tabla partidos
    cur.execute('''
                CREATE TABLE IF NOT EXISTS partidos
                (MatchID INTEGER PRIMARY KEY, MatchType INTEGER, SourceSystem TEXT, MatchDate TEXT, HomeTeamID INTEGER,
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
                SubAnotacion INTEGER, SubBP INTEGER, SubXP INTEGER, SubForma INTEGER, SubResistencia INTEGER, SubSpecialty INTEGER, SubLoyalty INTEGER, SubMotherClubBonus TEXT, ObjPorteria INTEGER, ObjDefensa INTEGER,
                ObjJugadas INTEGER, ObjLateral INTEGER, ObjPases INTEGER,
                ObjAnotacion INTEGER, ObjXP INTEGER, ObjForma INTEGER, ObjResistencia INTEGER, ObjSpecialty INTEGER, ObjLoyalty INTEGER, ObjMotherClubBonus TEXT, ObjBP INTEGER,
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

    # tabla SE
    cur.execute('''
                CREATE TABLE IF NOT EXISTS SE
                (EventTypeID INTEGER PRIMARY KEY, EventName TEXT, TypeSEBD TEXT)
                ''')
    try:
        cur.execute('SELECT EventTypeID FROM SE WHERE EventTypeID = 19')
        test = cur.fetchone()[0]
    except:
        fhand = open('doc/EventList.txt')
        for line in fhand:
            valores = line.split(';')
            if valores[2][:2] == 'SE':
                cur.execute('INSERT INTO SE (EventTypeID, EventName, TypeSEBD) VALUES (?, ?, ?)',(valores[0], valores[1], valores[2][:2]))
            else:
                cur.execute('INSERT INTO SE (EventTypeID, EventName, TypeSEBD) VALUES (?, ?, ?)',(valores[0], valores[1], valores[2]))

    # vista alineacion_all con minutos jugados de todos los jugadores incluidas las susticiones!
    cur.execute('''
                CREATE VIEW IF NOT EXISTS alineacion_all as
                select a.MatchID, a.RoleTeam, a.RoleID as Pos, a.PlayerID as Player, b.Specialty,
                case when c.MatchMinute is null then 90 when c.MatchMinute > 90 then 90 else c.MatchMinute end as Minutos
                from alineacion as a
                left join jugadores as b ON a.PlayerID = b.PlayerID
                left join sustituciones as c ON a.MatchID = c.MatchID AND a.PlayerID = c.SubjectPlayerID
                UNION ALL
                select a.MatchID, a.RoleTeam, c.NewPositionId as Pos, c.ObjectPlayerID as Player, d.Specialty,
                case when c.MatchMinute is null then 0 when c.MatchMinute > 90 then 0 else 90-c.MatchMinute end as Minutos
                from alineacion as a
                left join jugadores as b ON a.PlayerID = b.PlayerID
                left join sustituciones as c ON a.MatchID = c.MatchID AND a.PlayerID = c.SubjectPlayerID
                left join jugadores as d ON c.ObjectPlayerID = d.PlayerID
                where Minutos > 0
                ''')

    # vista anterior con posiciones contrarias exactas en letras
    cur.execute('''
                CREATE VIEW IF NOT EXISTS alineacion_all_contrarios as
                select * from ( select *, case	when RoleTeam = 1 then 2 when RoleTeam = 2 then 1 end as RoleContrario,
                case when Pos = 106 then "ED" when Pos > 106 and Pos < 110 then "Inner" when Pos = 110 then "EI" when Pos > 110 then "F" when Pos = 101 then "DLD" when Pos = 105 then "DLI" when Pos > 101 and Pos < 105 then "DC" end as PosLetras,
                case when Pos = 106 then "DLI" when Pos > 106 and Pos < 110 then "Inner" when Pos = 110 then "DLD" when Pos > 110 then "DC" when Pos = 101 then "EI" when Pos = 105 then "ED" when Pos > 101 and Pos < 105 then "F" end as PosConLetras
                from alineacion_all) as a
                left join ( select *, case	when RoleTeam = 1 then 2 when RoleTeam = 2 then 1 end as RoleContrario,
                case when Pos = 106 then "ED" when Pos > 106 and Pos < 110 then "Inner" when Pos = 110 then "EI" when Pos > 110 then "F" when Pos = 101 then "DLD" when Pos = 105 then "DLI" when Pos > 101 and Pos < 105 then "DC" end as PosLetras,
                case when Pos = 106 then "DLI" when Pos > 106 and Pos < 110 then "Inner" when Pos = 110 then "DLD" when Pos > 110 then "DC" when Pos = 101 then "EI" when Pos = 105 then "ED" when Pos > 101 and Pos < 105 then "F" end as PosConLetras
                from alineacion_all) as b ON a.MatchID = b.MatchID and a.RoleContrario = b.RoleTeam and a.PosConLetras = b.PosLetras
                ''')

    cur.execute('''
                CREATE VIEW IF NOT EXISTS alineacion_all_contrarios_tec_cab as
                select * from ( select *, case	when RoleTeam = 1 then 2 when RoleTeam = 2 then 1 end as RoleContrario,
                case when Pos > 105 then "E_I_F" else "no" end as PosLetras,
                case when Pos > 100 and Pos < 110 and Pos <> 106 then "D_I" else "no" end as PosConLetras
                from alineacion_all) as a
                left join ( select *, case	when RoleTeam = 1 then 2 when RoleTeam = 2 then 1 end as RoleContrario,
                case when Pos > 105 then "E_I_F" else "no" end as PosLetras,
                case when Pos > 100 and Pos < 110 and Pos <> 106 then "D_I" else "no" end as PosConLetras
                from alineacion_all) as b ON a.MatchID = b.MatchID and a.RoleContrario = b.RoleTeam and a.PosConLetras = b.PosLetras
                ''')

    conn.commit()
    conn2.commit()
    cur.close()
    cur2.close()

def new_partidos(helper, base, user_key, user_secret, fecha, team):
    listaPartidosNuevos = []
    conn = sqlite3.connect(base)
    cur = conn.cursor()

    # Haremos 2 pasadas en lista de aprtidos. En matchesarchives solo hay partidos con Source=Hattrick (no torneos)
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

    countMatchNuevos = 0

    root = ET.fromstring(xmldoc)
    for match in root.findall('Team/MatchList/Match'):
        idmatch = match.find('MatchID').text
        typematch = match.find('MatchType').text
        datematch = match.find('MatchDate').text
        goalshome = match.find('HomeGoals').text
        goalsaway = match.find('AwayGoals').text
        teamidHome= match.find('HomeTeam/HomeTeamID').text
        teamidAway = match.find('AwayTeam/AwayTeamID').text
        systemsource = 'Hattrick'
        try:
            cur.execute('INSERT INTO partidos (MatchID, SourceSystem, MatchType, MatchDate, HomeTeamID, HomeGoals, AwayTeamID, AwayGoals) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (idmatch, systemsource, typematch, datematch, teamidHome, goalshome, teamidAway, goalsaway))
            countMatchNuevos = countMatchNuevos + 1
            listaPartidosNuevos.append(idmatch)
        except:
            None
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

    # Segunda pasada en lista de partidos. Ahora en matches para buscar los partidos Source=htointegrated
    hoy = datetime.now()
    xmldoc2 = helper.request_resource_with_key(  user_key,
                                                user_secret,
                                                'matches',
                                                {
                                                 'version' : 2.8,
                                                 'teamID' : team,
                                                 'isYouth' : 'false',
                                                 'LastMatchDate' : hoy
                                                }
                                             )

    root = ET.fromstring(xmldoc2)
    for match in root.findall('Team/MatchList/Match'):
        statusmatch = match.find('Status').text
        if statusmatch != 'FINISHED': continue
        idmatch = match.find('MatchID').text
        typematch = match.find('MatchType').text
        datematch = match.find('MatchDate').text
        goalshome = match.find('HomeGoals').text
        goalsaway = match.find('AwayGoals').text
        teamidHome= match.find('HomeTeam/HomeTeamID').text
        teamidAway = match.find('AwayTeam/AwayTeamID').text
        systemsource = match.find('SourceSystem').text
        try:
            datematch_string = datetime.strptime(datematch, '%Y-%m-%d %H:%M:%S')
            if systemsource == 'HTOIntegrated' and datematch_string > datetime(2017,12,20,0,0,0):
                cur.execute('INSERT INTO partidos (MatchID, SourceSystem, MatchType, MatchDate, HomeTeamID, HomeGoals, AwayTeamID, AwayGoals) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (idmatch, systemsource, typematch, datematch, teamidHome, goalshome, teamidAway, goalsaway))
                countMatchNuevos = countMatchNuevos + 1
                listaPartidosNuevos.append(idmatch)
            else:
                None
        except:
            None
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
    print(Back.GREEN + Fore.BLACK + str(countMatchNuevos), Style.RESET_ALL + ' partidos nuevos han sido encontrados!')

    return listaPartidosNuevos

def get_partido(helper, base, user_key, user_secret, idpartido):
    global rival
    global teamrole

    # Guardamos la info ordenadamente dentro la base de datos de la App
    conn = sqlite3.connect(base)
    cur = conn.cursor()
    cur.execute('SELECT SourceSystem FROM partidos WHERE MatchID = ?',(idpartido,))
    source = cur.fetchone()[0]
    if source == 'HTOIntegrated':
        source = 'htointegrated'
    else:
        source = 'hattrick'

    #Consulta a la API
    xmldoc = helper.request_resource_with_key(     user_key,
                                                   user_secret,
                                                   'matchdetails',
                                                   {
                                                    'version' : 2.9,
                                                    'matchEvents' : 'true',
                                                    'matchID' : idpartido,
                                                    'sourceSystem' : source
                                                   }
                                                  )
    root = ET.fromstring(xmldoc)



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
                                                    'matchID' : idpartido,
                                                    'sourceSystem' : source
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
                                                    'teamID' : rival,
                                                    'sourceSystem' : source
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

def get_habilidades(helper, base, user_key, user_secret, idpartido):

    conn = sqlite3.connect(base)
    cur = conn.cursor()
    cur2 = conn.cursor()

    # Recuperamos eventos del partido en base de datos
    cur.execute('''SELECT a.MatchID, a.IndexEv, a.EventTypeID, a.SubjectPlayerID, a.ObjectPlayerID, b.TypeSEBD
                FROM eventos as a
                LEFT JOIN SE as b ON a.EventTypeID = b.EventTypeID
                WHERE b.TypeSEBD = 'SE' AND a.MatchID=?
                ''',(idpartido,))
    for row in cur:
        # row[3] SubjectPlayerID i row[4] ObjectPlayerID
        xmlSub = helper.request_resource_with_key(     user_key,
                                                       user_secret,
                                                       'playerdetails',
                                                       {
                                                        'version' : 2.7,
                                                        'playerID' : row[3]
                                                       }
                                                      )
        Subplayer = ET.fromstring(xmlSub)
        try:
            specialtysub = Subplayer.find('Player/Specialty').text
            formsub = Subplayer.find('Player/PlayerForm').text
            loyalsub = Subplayer.find('Player/Loyalty').text
            mothersub = Subplayer.find('Player/MotherClubBonus').text
            xpsub = Subplayer.find('Player/Experience').text
            ressub = Subplayer.find('Player/PlayerSkills/StaminaSkill').text
            porsub = Subplayer.find('Player/PlayerSkills/KeeperSkill').text
            defsub = Subplayer.find('Player/PlayerSkills/DefenderSkill').text
            jugsub = Subplayer.find('Player/PlayerSkills/PlaymakerSkill').text
            latsub = Subplayer.find('Player/PlayerSkills/WingerSkill').text
            passub = Subplayer.find('Player/PlayerSkills/PassingSkill').text
            anosub = Subplayer.find('Player/PlayerSkills/ScorerSkill').text
            bpsub = Subplayer.find('Player/PlayerSkills/SetPiecesSkill').text
        except:
            specialtysub = -99
            formsub = -99
            loyalsub = -99
            mothersub = 'false'
            xpsub = -99
            ressub = -99
            porsub = -99
            defsub = -99
            jugsub = -99
            latsub = -99
            passub = -99
            anosub = -99
            bpsub = -99

        if row[4] == '0':
            specialtyobj = -99
            formobj = -99
            loyalobj = -99
            motherobj = 'false'
            xpobj = -99
            resobj = -99
            porobj = -99
            defobj = -99
            jugobj = -99
            latobj = -99
            pasobj = -99
            anoobj = -99
            bpobj = -99
        else:
            xmlObj = helper.request_resource_with_key(     user_key,
                                                           user_secret,
                                                           'playerdetails',
                                                           {
                                                            'version' : 2.7,
                                                            'playerID' : row[4]
                                                           }
                                                          )
            Objplayer = ET.fromstring(xmlObj)
            try:
                specialtyobj = Objplayer.find('Player/Specialty').text
                formobj = Objplayer.find('Player/PlayerForm').text
                loyalobj = Objplayer.find('Player/Loyalty').text
                motherobj = Objplayer.find('Player/MotherClubBonus').text
                xpobj = Objplayer.find('Player/Experience').text
                resobj = Objplayer.find('Player/PlayerSkills/StaminaSkill').text
                porobj = Objplayer.find('Player/PlayerSkills/KeeperSkill').text
                defobj = Objplayer.find('Player/PlayerSkills/DefenderSkill').text
                jugobj = Objplayer.find('Player/PlayerSkills/PlaymakerSkill').text
                latobj = Objplayer.find('Player/PlayerSkills/WingerSkill').text
                pasobj = Objplayer.find('Player/PlayerSkills/PassingSkill').text
                anoobj = Objplayer.find('Player/PlayerSkills/ScorerSkill').text
                bpobj = Objplayer.find('Player/PlayerSkills/SetPiecesSkill').text
            except:
                specialtyobj = -99
                formobj = -99
                loyalobj = -99
                motherobj = -99
                xpobj = -99
                resobj = -99
                porobj = -99
                defobj = -99
                jugobj = -99
                latobj = -99
                pasobj = -99
                anoobj = -99
                bpobj = -99

        cur2.execute('''UPDATE eventos SET SubPorteria=?, SubDefensa=?, SubJugadas=?, SubLateral=?, SubPases=?, SubAnotacion=?, SubBP=?, SubXP=?, SubForma=?, SubResistencia=?, SubSpecialty=?, SubLoyalty=?, SubMotherClubBonus=?,
                        ObjPorteria=?, ObjDefensa=?, ObjJugadas=?, ObjLateral=?, ObjPases=?, ObjAnotacion=?, ObjBP=?, ObjXP=?, ObjForma=?, ObjResistencia=?, ObjSpecialty=?, ObjLoyalty=?, ObjMotherClubBonus=?
                        WHERE MatchID = ? AND IndexEv = ?''',(porsub, defsub, jugsub, latsub, passub, anosub, bpsub, xpsub, formsub, ressub, specialtysub, loyalsub, mothersub,
                        porobj, defobj, jugobj, latobj, pasobj, anoobj, bpobj, xpobj, formobj, resobj, specialtyobj, loyalobj, motherobj, idpartido, row[1]))

    conn.commit()
    cur.close()
    cur2.close()
