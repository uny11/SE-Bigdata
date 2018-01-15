
import smtplib
from datetime import datetime
from email.mime import text, multipart, application
from colorama import init, Fore, Back, Style

def enviar_datos(fichero, user):
    # Variables de envio de mail
    mailorigen = 'bigdata@gmx.es'
    maildestino = 'bigdata.sqlite@gmail.com'

    # Contruimos partes del mensaje
    ahora = datetime.now()
    asunto = str(ahora)+'%'+str(user)
    texto = 'Aqui va la base de datos! de '+str(user)+' de '+str(ahora)

    # Establecemos conexion con el servidor smtp de gmail
    try:
        mailServer = smtplib.SMTP('smtp.gmx.es',587)
    except:
        print(Fore.RED + Style.BRIGHT+'ERROR INESPERADO! '+'De momento, la base no ha podido ser enviada.\nAsegurate de estar conectado a internet y/o de no usar un proxy (habitual si te conectas en el trabajo).\nSi lo anterior es ok, por favor, avisa a uny11 en el hattrick del problema.\nSGracias de antemano y perdona las molestias')
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    try:
        mailServer.login('bigdata@gmx.es','bduny11Parma')
    except:
        print(Fore.RED + Style.BRIGHT+'ERROR!' +'De momento, no tienes autorización para enviar la base al servidor. \n'+Fore.YELLOW+'uny11 '+ Style.RESET_ALL + 'acaba de recibir una notificación para autorizar tu usuario '+Fore.YELLOW+Style.BRIGHT+str(user)+Style.RESET_ALL+'\nGracias por esperar su respuesta (en el foro de la federación BigData) para volver a intentar de nuevo más tarde\n')

    # Construimos un mensaje Multipart
    mensaje = multipart.MIMEMultipart()
    mensaje['From']=mailorigen
    mensaje['To']=maildestino
    mensaje['Subject']=asunto
    mensaje.attach(text.MIMEText(texto))
    # adjuntamos fichero
    file = open(fichero,'rb')
    contenido = application.MIMEApplication(file.read())
    contenido.add_header('Content-Disposition', 'attachment; filename = "bigdata.sqlite"')
    mensaje.attach(contenido)

    # Enviamos el correo, con los campos from y to.
    mailServer.sendmail(mailorigen,maildestino, mensaje.as_string())
    # Cierre de la conexion
    mailServer.close()
