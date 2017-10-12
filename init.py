
from  chpp import CHPPhelp
import xml.etree.ElementTree as ET
import sqlite3

# Iniciamos claves para acceder a los recursos CHPP de la API de Hatrick
helper = CHPPhelp()
conn = sqlite3.connect('bigdata.sqlite')
cur = conn.cursor()
cur.execute('SELECT key FROM keys WHERE id = 3 LIMIT 1')
user_key = cur.fetchone()[0]
cur.execute('SELECT key FROM keys WHERE id = 4 LIMIT 1')
user_secret = cur.fetchone()[0]
cur.close()

# Example to get the list of youth players
# xmldoc = helper.request_resource_with_key(      user_key,
#                                                user_secret,
#                                                'youthplayerlist',
#                                                {
#                                                 'actionType' : 'details',
#                                                 'showScoutCall' : 'true',
#                                                 'showLastMatch' : 'true'
#                                                }
#                                               )
# print(xmldoc)

# #Buscamos si la App ya conoce las claves para conectarse
# conn = sqlite3.connect('bigdata.sqlite')
# cur = conn.cursor()
# try:
#     cur.execute('SELECT key FROM keys WHERE id = 3')
#     print('Las claves existen, GENIAL')
# except:
#     print('Las claves NO existen, hay que lanzar proceso de Auth')
#
# cur.close()
