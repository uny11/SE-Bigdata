
*Copyright (C) 2017, Isaac Porta "uny11" en hattrick*

# SE-BIGDATA

![Logo](/images/logo.png)


> (language: spanish)

Este programa permite para participar en el estudio del nuevo sistema de eventos especiales del juego online Hattrick (www.hattrick.org).
Básicamente el programa permite recoger todos los datos importantes de los partidos de los usuarios y almacenar dichos datos en una base de datos (tipo SQLite para ser exactos).
Esta base de datos puede ser revisada por el usuario si lo desea (se require conocimientos de SQL).
Al mismo tiempo el programa permite enviar los datos al servidor para enriquecer el estudio global.

Los resultados del estudio se publicarán en la federación "BigData" de Hattrick.


### Estado de desarrollo : Terminado!
> 12/01/2018: La aplicación esta lista para ser usada.
> 16/01/2018: v0.1.2 lanzada, corregido el fallo de envio al servidor y algun error menor.


## Instalación y Uso de la aplicación

NOTA:
Esta aplicación funciona bajo PC con windows y linux instalado, puede que tambien bajo Mac (este último NO ha sido probado aún)
No funciona en moviles android/apple.

### Intalación para usuarios que tengan GIT instalado.

Para los usuarios con GIT instalado solamente hay que ir a la carpeta donde se quiera guardar la aplicación y clonar el repositorio:

> git clone git://https://github.com/uny11/SE-Bigdata

### Instalación para usuarios que NO usan GIT habitualmente

1.- Bajar los archivos de la aplicación del repositorio. Para ello ir a https://github.com/uny11/SE-Bigdata y dar en "DownloadZIP".
![Bajar los arichivos](/images/download.png)
2.- Descomprimir el archivo "SE-Bigdata-master.zip" en la carpeta donde se quiera guardar la aplicación.

3.- La carpeta "SE-Bigdata-master" contiene los archivos de la aplicación. Puede ser renombrada a cualquier otro nombre si el usuario lo desea.


### Ejecutar la aplicacion en WINDOWS

1.- Para lanzar la aplicación hay que ir a la subcarpeta /SE-Bigdata-master/windows/v012 (actualmente la ultima versión).

2.- Y ejecutar el archivo "bigdata.exe".

Se puede hacer a través del powershell (windows10) o el CMD (windows7) con:
> cd SE-Bigdata-master

> cd windows

> cd v012

> .\bigdata.exe

O directamente desde la ventana de archivos con doble-click en el archivo bigdata.exe
![doble-click](/images/dobleclick.png)

### Ejecutar la aplicacion en LINUX

1.- Para lanzar la aplicación hay que ir a la subcarpeta /SE-Bigdata-master/linux/v012 (actualmente la ultima versión).

2.- Y ejecutar el archivo "bigdata". Desde la consola de tu distribucion:
> cd SE-Bigdata-master

> cd linux

> cd v012

> ./bigdata


### Uso de la aplicacion

1.- La primera vez que se use el programa, se deberá autorizar el acesso CHPP como cualquier aplicación de hattrick.
Para ello abra que seguir las instruciones que se van mostrando, este proceso es identico a cualquier aplicación CHPP.
![Autorización_CHPP](/images/chpp.png)

2.- Una vez la aplicación hay sido autorizada se podrá usar con normalidad.
![menu](/images/menu.png)

3.- La opción "1" servirá para buscar nuevos partidos en hattrick. Serán rescatados todos los partidos con fecha 20/12/17 incluido,
que son aquellos con el nuevo sistema de eventos. Se incluyen partidos de torneo, escaladas etc...
![partidos](/images/partidos.png)

En este momento, el archivo "/SE-Bigdata-master/windows/v012/bigdata.sqlite" contiene la base de partidos con todos los datos descargados de hattrick.
Si tienes conocimientos de SQL, puedes verificar su contenido por ejemplo con la aplicación gratuita "DB Browser".

4.- La opción "2" servirà para enviar el archivo ""/SE-Bigdata-master/windows/v012/bigdata.sqlite" al servidor.
*Es necesario que uny11 te de acceso para completar dicha tarea la primera vez*
uny11 te confirmara por el foro de la federación BigData que dicha autorización ha sido concedida.

![Opcion2](/images/envio.png)

5.- La opción "3" mostrara por cada tipo de especialista tus estadisticas personales. Recordad que estos datos son orientativos y no sirven de mucho.
En la federacion se irán colgando los resultados y estudios realizados con los datos de TODOS los usuarios.
Este apartado es simplemente para que los usuarios sin conocimientos de SQL o estadistica puedan ver sus partidos de forma orientativa.

![Estadisticas](/images/esta.png)

6.- La opción "4" es para salir de la aplicación.


### Screenshoot:
![ejemplo](/images/ejemplo.png)

## Bug o problemas

Reportar cualquier duda, comentario, problema o similar en la federación BigData.
