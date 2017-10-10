
import urllib.request
import urllib.parse
import urllib.error
from  doc.oauthhelper.oauthhelper import OAuthHelper

# create a new helper object
oauth_helper = OAuthHelper()

user_key = 'nnch734d00sl2jdk'
user_secret = 'pfkkdhi9sl3r4s00'

# 2) Access protected resources
# Once a valid Access Token for a particular user is obtained, it is used for
# retrieving the information needed for the application.
# The oauth_helper.request_resource_with_key() method wraps the needed logic.
# diagram: steps G, H

# example: get the list of youth players
xmldoc = oauth_helper.request_resource_with_key(
                                                user_key,
                                                user_secret,
                                                'youthplayerlist',
                                                {
                                                 'actionType' : 'details',
                                                 'showScoutCall' : 'true',
                                                 'showLastMatch' : 'true'
                                                }
                                               )
