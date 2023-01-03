# main.py
#
# Este es el programa principal 

import os
import openpyxl
from rich import print
from rich.prompt import Prompt
from modulos import procesamiento_poblacion

#############################################################################
#
# Procesamiento del conjunto de datos de población

print(" ")
print("[bold medium_purple3] A. Estructurando los datos de población [/bold medium_purple3]")

procesamiento_poblacion.corregir_cve_inegi(procesamiento_poblacion.tabla)
procesamiento_poblacion.columnas_geo(procesamiento_poblacion.tabla)

print(" ")
eleccionUsuario = Prompt.ask("Nivel de segregación que desea: ", choices=["estatal", "municipal"])
print(" ")

def nivel_seg(eleccion):
    """
    Función para elegir el procesamiento de datos de acuerdo con el nivel de segregación de interés.

    Parámetro: respuesta de usuarix.
    """
    if eleccion == "estatal":
        a = procesamiento_poblacion.genera_tabla_est()
        b = procesamiento_poblacion.genera_tabla_quin_est()

        return a, b
    
    elif eleccion == "municipal":
        a = procesamiento_poblacion.genera_tabla_mun()
        b = procesamiento_poblacion.genera_tabla_quin_mun()
    
        return a, b

x, y = nivel_seg(eleccionUsuario)

def estructuracion_totales():
    """
    Función que estructura los datos totales de acuerdo al nivel de segregación elegido.

    Parámetros: ninguno
    Regresa: Dataframe con los datos estructurados. 
    """
    resultado1 = procesamiento_poblacion.estructura_totales(x)
      
    return resultado1

def estructuracion_quinquenales():
    """
    Función que estructura los datos quinquenales de acuerdo al nivel de segregación elegido.

    Parámetros: ninguno
    Regresa: Dataframe con los datos estructurados. 
    """
    resultado2= procesamiento_poblacion.estructura_quinquenios(y)
    
    return resultado2

print("[bold medium_purple3] ... Haciendo la magia ... :heart: [/bold medium_purple3]")
print(" ")

resultados_totales = estructuracion_totales()
resultados_quinquenales = estructuracion_quinquenales()

r1= resultados_totales.to_excel('output_pob_total_' + '{}'.format(eleccionUsuario) +'.xlsx', index=False)
r2= resultados_quinquenales.to_excel('output_pob_quinquenio_' + '{}'.format(eleccionUsuario) +'.xlsx', index=False) 

r1= os.path.join('.', 'datos', 'datos_procesados')
r2= os.path.join('.', 'datos', 'datos_procesados')