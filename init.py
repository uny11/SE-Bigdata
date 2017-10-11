#Este es el programa base de la App
#Empezaremos con algunos test basicos con la API de hattrick (o CHPP)

from  chpp import CHPPhelp
import hidden
import xml.etree.ElementTree as ET

#Iniciamos claves para acceder a los recursos CHPP de la API de Hatrick
helper = CHPPhelp()
secrets = hidden.keys_app()
user_key = secrets['token_key']
user_secret = secrets['token_secret']

#Example: get the list of youth players
#xmldoc = helper.request_resource_with_key(      user_key,
#                                                user_secret,
#                                                'youthplayerlist',
#                                                {
#                                                 'actionType' : 'details',
#                                                 'showScoutCall' : 'true',
#                                                 'showLastMatch' : 'true'
#                                                }
#                                               )
