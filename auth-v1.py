# Esta version obtienes los tokens y solamente los muestra en pantalla

from  chpp import CHPPhelp

# create a new helper object with all info
helper = CHPPhelp()

# Obtain and URL for a Request Token that will be passed to the end user
# diagram: steps A, B
registration_url = helper.get_request_token_url()
print ('Abrir este url en el navegador para obtener el PIN: ',registration_url)

# At this point, the user needs to open the 'registration_url' (which points
# to chpp.hattrick.org) and enter his username and password. At the end of the
# process, a PIN is presented on their browser ('pin').
# diagram: steps C, D
pin = input('Entrar PIN: ')

# Get a valid Access Token, by using the generated pin.
# diagram: steps E, F
access_token = helper.get_access_token(pin)

# The Access Token is now ready to be used. For convenience, the key and
# secret should be stored on a database or permanent storage:
user_key = access_token.key
user_secret = access_token.secret
print('access_token es: ',user_key)
print('user_secret es: ',user_secret)
