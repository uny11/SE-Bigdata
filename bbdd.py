# Contiene clases y funciones para trabajar con la bbdd de la App

import sqlite3
from  chpp import CHPPhelp
import xml.etree.ElementTree as ET

class BBDDhelp(object):

    def lista_partidos(self, helper, user_key, user_secret, fecha):
        # Peticion a la API
        xmldoc = helper.request_resource_with_key(  user_key,
                                                    user_secret,
                                                   'matches',
                                                   {
                                                   'version' : 2.8,
                                                   'isYouth' : 'false'
                                                #    'LastMatchDate' : fecha
                                                   }
                                               )
        #Accion con el xml, de momento solo imprime por pantalla la lista de partidos
        root = ET.fromstring(xmldoc)

        for match in root.findall('Team/MatchList/Match'):
            idmatch = match.find('MatchID').text
            print(idmatch)
