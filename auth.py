# Esta version se guardan los tokens dentro la base de datos de la App

from  chpp import CHPPhelp

# create a new helper object with all info
helper = CHPPhelp()

# Generamos la url para obtener el pin de autorizacion CHPP
registration_url = helper.get_request_token_url()
print ('Abrir este url en tu navegador preferido para obtener el PIN: ',registration_url)

# recuperamos el pin del usuario
pin = input('Entrar PIN: ')

# Obtenemos los tokens con el pin obtenido
access_token = helper.get_access_token(pin)
user_key = access_token.key
user_secret = access_token.secret

#Guardamos los tokens en la base de datos
conn = sqlite3.connect('bigdata.sqlite')
cur = conn.cursor()
try:
    cur.execute('INSERT INTO keys (id,key) VALUES (?,?)', (3,user_key))
except:
    None
try:
    cur.execute('INSERT INTO keys (id,key) VALUES (?,?)', (4,user_secret))
except:
    None
conn.commit()
cur.close()

print('SE-Bigdata ha sido autorizado con éxito!')
print('Disfruta de tus estadisticas!')
print('    by uny11')
