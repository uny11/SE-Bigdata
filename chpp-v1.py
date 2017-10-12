#Esta version del archivo chpp.py contiene los chpp_key/chpp_secret dentro de la clase CHPPhelp

import oauth2 as oauth
from contextlib import closing
from urllib.request import urlopen
from urllib.parse import parse_qsl
from urllib.parse import urlencode

#Vamos a definir una clase que contenga todas las constantes y funciones con sus variables inicializadas
class CHPPhelp(object):
    request_token_url     = 'https://chpp.hattrick.org/oauth/request_token.ashx'
    authorize_path        = 'https://chpp.hattrick.org/oauth/authorize.aspx'
    authenticate_path     = 'https://chpp.hattrick.org/oauth/authenticate.aspx'
    access_token_path     = 'https://chpp.hattrick.org/oauth/access_token.ashx'
    check_token_path      = 'https://chpp.hattrick.org/oauth/check_token.ashx'
    invalidate_token_path = 'https://chpp.hattrick.org/oauth/invalidate_token.ashx'
    resources_path        = 'http://chpp.hattrick.org/chppxml.ashx'
    chpp_key              = 'XXXX'
    chpp_secret           = 'XXXX'

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

        connection = urlopen(req.to_url())
        data = connection.read().decode("utf-8")
        request_token = dict(parse_qsl(data))

        token = oauth.Token(request_token['oauth_token'],
                            request_token['oauth_token_secret'])
        return token

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