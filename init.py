# App con interface de consola

from  chpp import CHPPhelp
import xml.etree.ElementTree as ET
import sqlite3

# Bienvenida
print('\n')
print('BIENVENIDO a SE-Bigdata!')
print('\n')
print('Gracias por participar en este estudio!')
print('y no dudes en preguntar cualquier duda o reportar algun fallo (uny11)')
print('\n')

# Iniciamos claves para acceder a los recursos CHPP de la API de Hatrick
helper = CHPPhelp()

# Buscamos si la App ya esta autorizada por el usuario para conectarse
conn = sqlite3.connect('bigdata.sqlite')
cur = conn.cursor()
try:
    cur.execute('SELECT key FROM keys WHERE id = 3')
    test = cur.fetchone()[0]
    cur.execute('SELECT key FROM keys WHERE id = 3 LIMIT 1')
    user_key = cur.fetchone()[0]
    cur.execute('SELECT key FROM keys WHERE id = 4 LIMIT 1')
    user_secret = cur.fetchone()[0]
except:
    # Si el test da un valor de ERROR, lanzamos proceso de autorizacion
    # print('\n')
    print('Para usar SE-Bigdata, es necesario tu autorizacion CHPP para el uso de esta aplicacion')
    print('Por favor, sigue las instruciones:')
    print('\n')
    helper.get_auth()
cur.close()




# # Example to get the list of youth players
# xmldoc = helper.request_resource_with_key(     user_key,
#                                                user_secret,
#                                                'youthplayerlist',
#                                                {
#                                                 'actionType' : 'details',
#                                                 'showScoutCall' : 'true',
#                                                 'showLastMatch' : 'true'
#                                                }
#                                               )
# print(xmldoc)
