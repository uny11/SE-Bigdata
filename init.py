# App con interface de consola

from chpp import CHPPhelp
import bbdd
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import sqlite3

# Bienvenida
print('\n')
print('BIENVENIDO a SE-Bigdata! v0.0')
print('\n')
print('Gracias por participar en este estudio!')
print('y no dudes en preguntar cualquier duda o reportar algun fallo (uny11)')
print('\n')

# Iniciamos claves y funciones para acceder a los recursos CHPP de la API de Hatrick
helper = CHPPhelp()

#Iniciamos base de datos de SE-Bigdata
basedatos = 'bigdata.sqlite'
init_bbdd(basedatos)

# Buscamos si la App ya esta autorizada por el usuario para conectarse
conn = sqlite3.connect(basedatos)
cur = conn.cursor()
try:
    cur.execute('SELECT key FROM keys WHERE id = 3')
    test = cur.fetchone()[0]
    cur.execute('SELECT key FROM keys WHERE id = 3 LIMIT 1')
    user_key = cur.fetchone()[0]
    cur.execute('SELECT key FROM keys WHERE id = 4 LIMIT 1')
    user_secret = cur.fetchone()[0]
    try:
        cur.execute( 'SELECT max(MatchDate) FROM partidos')
        fechamax = cur.fetchone()[0]
    except:
        fechamax = datetime.today() - timedelta(days=90)
except:
    # Si el test da un valor de ERROR, lanzamos proceso de autorizacion
    # print('\n')
    print('Para usar SE-Bigdata, es necesario tu autorizacion CHPP para el uso de esta aplicacion')
    print('Por favor, sigue las instruciones:')
    print('\n')
    helper.get_auth(basedatos)
cur.close()

# Lanzamos MENU de la aplicacion
while True:
    print('Que quieres hacer? Elige una opción (por defecto 4): ')
    print('     1.- Obtener datos de Hattrick')
    print('     2.- Enviar datos al servidor para enriquecer el estudio')
    print('     3.- Ver tus estadisticas')
    print('     4.- Salir')
    opcion = input('>> ')

    if opcion == '1':
        #Paso1 - Recuperar lista de partidos nuevos
        print('\n')
        print('Buscando partidos en www.hattrick.org... ')
        listaPartidos = bbdd.guardar_lista_partidos(helper, basedatos, user_key, user_secret, fechamax)

        #Paso2 - Recuperar detalle de los partidos nuevos
        if len(listaPartidos) > 0:
            print('\n')
            print('Recuperamos los datos de los ',len(listaPartidos),' partidos nuevos en www.hattrick.org... ')
            for partido in listaPartidos:
                bbdd.recopilar_un_partido(helper, basedatos, user_key, user_secret, partido)

    elif opcion == '2':
        print('\n')
        print('Perdón! Esta parte esta en contrucción')
        print('\n')

    elif opcion == '3':
        print('\n')
        print('Perdón! Esta parte esta en contrucción')
        print('\n')

    elif opcion == '4': break
    elif len(opcion) < 1: break

    else:
        print('\n')
        print('No has elegido una opcion valida! Prueba otra vez..')
        print('\n')







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
