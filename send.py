
import smtplib
from datetime import datetime
from email.mime import text, multipart, application

def enviar_datos(fichero, user):
    # Variables de envio de mail
    mailorigen = 'bigdata.sqlite@gmail.com'
    maildestino = 'bigdata.sqlite@gmail.com'

    # Contruimos partes del mensaje
    ahora = datetime.now()
    asunto = str(user)+' '+str(ahora)
    texto = 'Aqui va la base de datos! de '+str(user)+' de '+str(ahora)

    # Establecemos conexion con el servidor smtp de gmail
    mailServer = smtplib.SMTP('smtp.gmail.com',587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login('bigdata.sqlite@gmail.com','sebduny11')

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
