# -*- coding: utf-8 -*-
import contextlib
import oauth2 as oauth
import urllib.request
import urllib.parse
import urllib.error
from urllib.parse import urlencode

class OAuthHelper(object):
    '''
    classdocs
    '''
    request_token_url     = 'https://chpp.hattrick.org/oauth/request_token.ashx'
    authorize_path        = 'https://chpp.hattrick.org/oauth/authorize.aspx'
    authenticate_path     = 'https://chpp.hattrick.org/oauth/authenticate.aspx'
    access_token_path     = 'https://chpp.hattrick.org/oauth/access_token.ashx'
    check_token_path      = 'https://chpp.hattrick.org/oauth/check_token.ashx'
    invalidate_token_path = 'https://chpp.hattrick.org/oauth/invalidate_token.ashx'
    resources_path        = 'http://chpp.hattrick.org/chppxml.ashx'
    chpp_key              = 'XXXXXX'
    chpp_secret           = 'XXXXXX'

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

        with contextlib.closing(urllib.request.urlopen(req.to_url())) as x:
            # send the request
            responseData = x.read()
            request_token = dict(urllib.parse.parse_qsl(responseData))

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

        with contextlib.closing(urllib.request.urlopen(req.to_url())) as x:
            # send the request
            responseData = x.read()
            request_token = dict(urllib.parse.parse_qsl(responseData))

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

        with contextlib.closing(urllib.request.urlopen(req.to_url(), timeout=10)) as x:
            # send the request
            responseData = x.read()

            return responseData

    def request_resource_with_key(self, token, token_secret, filename, query=[]):
        token = oauth.Token(token, token_secret)

        return self.request_resource(token, filename, query)
