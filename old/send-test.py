
import smtplib
from email.mime import text, multipart, application

# Establecemos conexion con el servidor smtp de gmail
mailServer = smtplib.SMTP('smtp.gmail.com',587)
mailServer.ehlo()
mailServer.starttls()
mailServer.ehlo()
mailServer.login('bigdata.sqlite@gmail.com','XXXXXX')

# Construimos un mensaje Multipart, con un texto y una imagen adjunta
mensaje = multipart.MIMEMultipart()
mensaje['From']="bigdata.sqlite@gmail.com"
mensaje['To']="bigdata.sqlite@gmail.com"
mensaje['Subject']="Tienes un segundo correo"
# Adjuntamos el texto
mensaje.attach(text.MIMEText("Este es el seungo mensaje de las narices"""))
# adjuntamos fichero
file = open('README.md')
contenido = application.MIMEApplication(file.read())
contenido.add_header('Content-Disposition', 'attachment; filename = "README.md"')
mensaje.attach(contenido)
# Enviamos el correo, con los campos from y to.
mailServer.sendmail("bigdata.sqlite@gmail.com","bigdata.sqlite@gmail.com", mensaje.as_string())
# Cierre de la conexion
mailServer.close()
