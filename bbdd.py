# Contiene clases y funciones para trabajar con la bbdd de la App

import sqlite3
from  chpp import CHPPhelp
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta


def init_base(base):
    # Creamos las tablas necesarias sino estan creadas
    conn = sqlite3.connect(base)
    cur = conn.cursor()

    # tabla partidos
    cur.execute('''
                CREATE TABLE IF NOT EXISTS partidos
                (MatchID INTEGER PRIMARY KEY, MatchType INTEGER, MatchDate TEXT, HomeTeamID INTEGER,
                HomeGoals INTEGER, AwayTeamID INTEGER, AwayGoals INTEGER, TacticTypeHome INTEGER,
                TacticSkillHome INTEGER, TacticTypeAway INTEGER, TacticSkillAway INTEGER, tarjetas INTEGER,
                lesiones INTEGER, SUS_Home INTEGER, SUS_Away INTEGER, PossessionFirstHalfHome INTEGER,
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

    cur.close()

def new_partidos(helper, base, user_key, user_secret, fecha):
    # Peticion a la API
    xmldoc = helper.request_resource_with_key(  user_key,
                                                user_secret,
                                                'matchesarchive',
                                                {
                                                 'version' : 1.3,
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
    print(countMatchNuevos, ' partidos nuevos han sido recuperados!')
    print(countMatchBBDD, ' partidos ya existian en SE-Bigdata')
    print('\n')

    return listaPartidosNuevos


def get_partido(helper, base, user_key, user_secret, idpartido):
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

    cur.close()
