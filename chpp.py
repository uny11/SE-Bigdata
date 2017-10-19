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

import oauth2 as oauth
from contextlib import closing
from urllib.request import urlopen
from urllib.parse import parse_qsl
from urllib.parse import urlencode
import sqlite3
from colorama import init, Fore, Back, Style
import xml.etree.ElementTree as ET
import webbrowser

#Vamos a definir una clase que contenga todas las constantes y funciones con sus variables inicializadas
class CHPPhelp(object):
    request_token_url     = 'https://chpp.hattrick.org/oauth/request_token.ashx'
    authorize_path        = 'https://chpp.hattrick.org/oauth/authorize.aspx'
    authenticate_path     = 'https://chpp.hattrick.org/oauth/authenticate.aspx'
    access_token_path     = 'https://chpp.hattrick.org/oauth/access_token.ashx'
    check_token_path      = 'https://chpp.hattrick.org/oauth/check_token.ashx'
    invalidate_token_path = 'https://chpp.hattrick.org/oauth/invalidate_token.ashx'
    resources_path        = 'http://chpp.hattrick.org/chppxml.ashx'
    chpp_key = '1Pg9hSfo5mkli2zaT8Hprr'
    chpp_secret = 'ERhrDhuV2uIEHG75QtHnHXDrOOYMixXzBS1V9yy3EZ6'

    def __init__(self):
        self.consumer = oauth.Consumer(key=self.chpp_key,
                            secret=self.chpp_secret)
        self.client = oauth.Client(self.consumer)
        self.signature_method = oauth.SignatureMethod_HMAC_SHA1()

    def get_request_token_url(self):
        # build the token request
        req = oauth.Request(method='GET',
                            url=self.request_token_url,
                            parameters={
                                        'oauth_callback': 'oob',
                                        'oauth_nonce': oauth.generate_nonce(),
                                        'oauth_timestamp': oauth.generate_timestamp(),
                                        'oauth_version': '1.0',
                                        },
                            is_form_encoded=True # needed to avoid oauth_body_hash
                            )

        # sign it
        req.sign_request(self.signature_method, self.consumer, None)

        connection = urlopen(req.to_url())
        data = connection.read().decode("utf-8")
        request_token = dict(parse_qsl(data))

        # parse the response
        self.oauth_req_token = request_token['oauth_token']
        self.oauth_req_token_secret = request_token['oauth_token_secret']

        # return the authorization url, with the token
        return "%s?oauth_token=%s" % (self.authorize_path, request_token['oauth_token'])

    def get_access_token(self, pin):
        # build the request
        req = oauth.Request(method='GET',
                            url=self.access_token_path,
                            parameters={
                                        'oauth_nonce': oauth.generate_nonce(),
                                        'oauth_timestamp': oauth.generate_timestamp(),
                                        'oauth_version': '1.0',
                                        'oauth_verifier': pin
                                        },
                            is_form_encoded=True # needed to avoid oauth_body_hash
                            )

        token = oauth.Token(self.oauth_req_token,
                            self.oauth_req_token_secret)
        token.set_verifier(pin)

        # sign it
        req.sign_request(self.signature_method, self.consumer, token)

        try:
            connection = urlopen(req.to_url())
            data = connection.read().decode("utf-8")
            request_token = dict(parse_qsl(data))

            token = oauth.Token(request_token['oauth_token'],
                            request_token['oauth_token_secret'])
            return token
        except:
            print(Style.BRIGHT + Fore.RED + 'El PIN no es correcto, prueba otra vez')
            pin = input('Entrar PIN de acesso: ')
            access_token = self.get_access_token(pin)
            return access_token

    def request_resource(self, token, filename, query=[]):
        # build the request
        url = "%s?file=%s&%s" % (self.resources_path, filename, urlencode(query))
        req = oauth.Request(method='GET',
                            url=url,
                            parameters={
                                        'oauth_nonce': oauth.generate_nonce(),
                                        'oauth_timestamp': oauth.generate_timestamp(),
                                        'oauth_version': '1.0',
                                        },
                            is_form_encoded=True # needed to avoid oauth_body_hash
                            )

        # sign it
        req.sign_request(self.signature_method, self.consumer, token)
        connection = urlopen(req.to_url())
        data = connection.read().decode("utf-8")

        return data

    def request_resource_with_key(self, token, token_secret, filename, query=[]):
        token = oauth.Token(token, token_secret)

        return self.request_resource(token, filename, query)

    def get_auth(self, base):        # Archivo auth.py
        # Generamos la url para obtener el pin de autorizacion CHPP
        registration_url = self.get_request_token_url()
        print (' - Abre esta direccion en tu navegador (sino se ha abierto automaticamente) \n   para obtener el PIN de acceso: \n')
        webbrowser.open(registration_url, new=0, autoraise=True)
        print(Fore.GREEN + Style.BRIGHT + registration_url,'\n')

        # recuperamos el pin del usuario
        pin = input('Entrar PIN de acesso (y pulse "Enter"): ')

        # Obtenemos los tokens con el pin obtenido
        access_token = self.get_access_token(pin)
        user_key = access_token.key
        user_secret = access_token.secret

        # Guardamos los tokens en la base de datos
        conn = sqlite3.connect(base)
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO keys (id,key) VALUES (?,?)', (1,user_key))
        except:
            None
        try:
            cur.execute('INSERT INTO keys (id,key) VALUES (?,?)', (2,user_secret))
        except:
            None

        # Recuperamos user y teams
        user = self.get_user(user_key, user_secret)
        teams = self.get_teams(user_key, user_secret)
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

        print('\n')
        print(Fore.GREEN + Style.BRIGHT + 'SE-Bigdata ha sido autorizado con éxito!' + Style.RESET_ALL)
        print(Style.BRIGHT + 'Disfruta de tus estadisticas! xD' + Style.RESET_ALL)
        print('\n')

    def get_user(self, token, token_secret):
        # Buscamos nickname del usuario
        xmldoc = self.request_resource_with_key( token,
                                                 token_secret,
                                                 'managercompendium',
                                                 {
                                                    'version' : 1.1,
                                                 }
                                                )
        root = ET.fromstring(xmldoc)
        user = root.find('Manager/Loginname').text

        return user

    def get_teams(self, token, token_secret):
        # Buscamos nickname del usuario
        xmldoc = self.request_resource_with_key( token,
                                                 token_secret,
                                                 'managercompendium',
                                                 {
                                                    'version' : 1.1,
                                                 }
                                                )
        root = ET.fromstring(xmldoc)
        listaTeams = []
        for team in root.findall('Manager/Teams/Team'):
            teamid = team.find('TeamId').text
            listaTeams.append(teamid)

        return listaTeams
