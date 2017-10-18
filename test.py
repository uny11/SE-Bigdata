
# from datetime import datetime, timedelta
import sqlite3
from  chpp import CHPPhelp
import xml.etree.ElementTree as ET
# from colorama import init, Fore, Back, Style

helper = CHPPhelp()
token = 'XXX'
token_secret = 'XXX'

user = helper.get_user(token, token_secret)
teams = helper.get_teams(token, token_secret)

conn = sqlite3.connect('bigdata.sqlite')
cur = conn.cursor()

try:
    cur.execute('INSERT INTO info (id,type,descripcion) VALUES (?,?,?)', (1,'user',str(user)))
    i = 2
    for team in teams:
        cur.execute('INSERT INTO info (id,type,descripcion) VALUES (?,?,?)', (i,'team',team))
        i = i + 1
except:
    None

conn.commit()
cur.close()
