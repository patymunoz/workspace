# main.py
#
# Este es el programa principal 

import os
from rich import print
from rich.prompt import Prompt
from modulos import procesamiento_poblacion

#############################################################################
#
# Procesamiento del conjunto de datos de población

print("[bold medium_purple3] A. Estructurando los datos de población [/bold medium_purple3]")

procesamiento_poblacion.corregir_cve_inegi(procesamiento_poblacion.tabla)
procesamiento_poblacion.columnas_geo(procesamiento_poblacion.tabla)

eleccionUsuario = Prompt.ask("Nivel de segregación que desea: ", choices=["Estatal", "Municipal"])

def nivel_seg(eleccion):
    """
    Función para elegir el procesmiento de datos de acuerdo con el nivel de segregación de interés.

    Parámetro: respuesta de usuarix.
    """
    if eleccion == "Estatal":
        datos1 = procesamiento_poblacion.genera_tabla_est()
        datos2 = procesamiento_poblacion.genera_tabla_quin_est()
    
    elif eleccion == "Municipal":
        datos3 = procesamiento_poblacion.genera_tabla_mun()
        datos4 = procesamiento_poblacion.genera_tabla_quin_mun()

segregacion = nivel_seg(eleccionUsuario)

def estructuracion_totales():
    if datos1:
        resultado1 = procesamiento_poblacion.estructura_totales(nivel_seg.datos1)
    else:
        resultado3 = procesamiento_poblacion.estructura_totales(nivel_seg.datos3)
      
    return resultado1, resultado3

def estructuracion_quinquenales():
    if datos2:
        resultado2= procesamiento_poblacion.estructura_quinquenios(nivel_seg.datos2)
    else:
        resultado4 = procesamiento_poblacion.estructura_quinquenios(nivel_seg.datos4)
    
    return resultado2, resultado4

resultados_totales = estructuracion_totales()
resultados_quinquenales = estructuracion_quinquenales()

for i in resultados_totales:
    output_file = os.path.join('.', 'datos', 'datos_procesados', 'output_poblacion_totales.xlsx')
for i in resultados_quinquenales:
    output_file = os.path.join('.', 'datos', 'datos_procesados', 'output_poblacion_quinquenales.xlsx')