# Contiene clases y funciones para trabajar con la bbdd de la App

import sqlite3
from  chpp import CHPPhelp
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def guardar_partidos(helper, user_key, user_secret, fecha):
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
    #Guardamos la lista de partidos en la BBDD
    conn = sqlite3.connect('bigdata.sqlite')
    cur = conn.cursor()
    cur.execute('''
                CREATE TABLE IF NOT EXISTS partidos
                (MatchID INTEGER PRIMARY KEY, MatchType INTEGER, MatchDate TEXT, HomeTeamID INTEGER,
                HomeGoals INTEGER, AwayTeamID INTEGER, AwayGoals INTEGER, TacticTypeHome INTEGER,
                TacticSkillHome INTEGER, TacticTypeAway INTEGER, TacticSkillAway INTEGER, tarjetas INTEGER
                lesiones INTEGER, SUS_Home INTEGER, SUS_Away INTEGER, PossessionFirstHalfHome INTEGER,
                PossessionFirstHalfAway INTEGER, PossessionSecondHalfHome INTEGER, PossessionSecondHalfAway INTEGER,
                RatingIndirectSetPiecesDefHome INTEGER, RatingIndirectSetPiecesAttHome INTEGER, RatingIndirectSetPiecesDefAway INTEGER,
                RatingIndirectSetPiecesAttAway INTEGER)
                ''')
    root = ET.fromstring(xmldoc)
    countmatch = 0
    countmatchguardado = 0
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
            countmatch = countmatch + 1
        except:
            countmatchguardado = countmatchguardado + 1
    conn.commit()
    cur.close()
    print(countmatch, ' partidos nuevos han sido recuperados!')
    print(countmatchguardado, ' partidos ya existian en SE-Bigdata')
    print('\n')
