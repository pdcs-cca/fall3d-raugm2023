# fall3d-raugm2023

Usar binderhub o repo2docker

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pdcs-cca/fall3d-raugm2023/HEAD?labpath=FALL3Dv8.1.ipynb)

# Entorno para el procesamiento de archivos de salida del modelo Fall3d

Trabajo basado en el pronóstico de caida de ceniza volcánica disponible en el página 

https://lamca.atmosfera.unam.mx/

## Creditos

- Configuración del modelo: **Dr. José Agustín García Reynoso**
- Código para generar productos: **M.C. Dulce Rosario Herrera Moro**
- Configuración y creación de entorno: **Esp. Pedro Damián Cruz Santiago**


# Ejecución
El entorno puede ser replicado en **binderhub**  o de forma local utilizando **repo2docker**.

## 1. Desempaquetar los archivos **archivos_extra.tgz** y **entradas.tgz**

~~~bash
tar xzf archivos_extra.tgz
tar xzf entradas.tgz
~~~


## 2. Ejecutar la celda con el procesamiento de los datos

Solo se entregar un archivo con datos a procesar, este archivo corresponde a una evento hipotético ocurrido el 18 de octubre del 2023  a las  09 hrs y con una altitud de 3km

Al final se genera un archivo **FL100.gif** a partir de la imágenes generadas en el directorio de salida **./salidas/20231018/Hora_09/Altura_03/C_FL100**  correspondiente a la nivel de vuelo de 10000 pies.


