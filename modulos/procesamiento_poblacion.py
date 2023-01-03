# procesamiento_poblacion.py
# 
# Este módulo tiene por objetivo estructurar el conjunto de datos de las proyecciones de población recuperado de la 
# fuente del Consejo Nacional de la Población (CONAPO) y el Instituto Nacional de Salup Pública (INSP) para el 
# procesamiento de datos necesario para el cálculo de tasas de mortalidad.

import os
import pandas as pd
import openpyxl
from auxiliares import tabla_estatal, tabla_municipal

ruta = os.path.join('.','datos','datos_origen','poblacion_2000-2020_conapo_insp.xlsx')

tabla = pd.read_excel(ruta)
tabla.rename(columns={'clave':'cvegeomun'}, inplace=True)

#############################################################################

def corregir_cve_inegi(df):
    """
    Función que estructura los valores de las columnas que contienen un identificador geográfico a partir
    de las claves sugeridas por INEGI.
    
    Parámetros: dataframe. 
    Regresa: las columnas de dataframe estructurada de acuerdo con el nivel estatal o municipal. 
    """
    assert isinstance (df, pd.core.frame.DataFrame), 'El argumento debería ser un "Dataframe"!!'

    if 'cve_ent' in df.columns:
        df['cve_ent'] = df['cve_ent'].apply(lambda x: '{0:0>2}'.format(x))
    if 'cve_mun' in df.columns:
        df['cve_mun'] = df['cve_mun'].apply(lambda x: '{0:0>3}'.format(x))    
    if 'cvegeomun' in df.columns:
        df['cvegeomun'] = df['cvegeomun'].apply(lambda x: '{0:0>5}'.format(x))
    
    return df

#############################################################################

def columnas_geo(df):
    """
    Función que segrega en columnas las claves geográficas correspondientes a nivel estatal o municipal
    de acuerdo con las claves del INEGI.
    
    Parámetros: dataframe. 
    Regresa: Genera las columnas geo de acuerdo al nivel de segregación de la clave.
    """
    assert isinstance (df, pd.core.frame.DataFrame), 'El argumento debería ser un "Dataframe"!!'
    assert [type(i) == 'str' for i in df[df.columns[0]]], 'Los valores de la serie deberían ser tipo "string"!!'
    
    if len(df[df.columns[0]].iloc[0]) ==5:
        df['cve_ent'] = df[df.columns[0]].str[:2]
        df['cve_mun'] = df[df.columns[0]].str[-3:]
    
    return df

#############################################################################

def genera_tabla_est():
    """
    Función que genera una tabla conforme al total de población a nivel estatal por año conforme a los datos originales.    
    """
    pob_tot_ent = tabla[tabla_estatal.pob_tot_entidad]
    pob_tot_ent = pd.pivot_table(pob_tot_ent, index='cve_ent', aggfunc=sum).reset_index()
    return pob_tot_ent

def genera_tabla_mun():
    """
    Función que genera una tabla conforme al total de población a nivel municipal por año conforme a los datos originales. 
    """
    pob_tot_mun = tabla[tabla_municipal.pob_tot_municipal]
    return pob_tot_mun

def genera_tabla_quin_est():
    """
    Función que genera una tabla conforme al total de población a nivel estatal por quinquenio por año conforme a los datos originales.
    """
    pob_quinquenio_ent = tabla[tabla_estatal.pob_quinquenio_entidad]
    pob_quinquenio_ent = pd.pivot_table(pob_quinquenio_ent, index='cve_ent', aggfunc=sum).reset_index()
    return pob_quinquenio_ent

def genera_tabla_quin_mun():
    """
    Función que genera una tabla conforme al total de población a nivel municipal por quinquenio por año conforme a los datos originales.
    """
    pob_quinquenio_mun = tabla[tabla_municipal.pob_quinquenio_municipal]
    return pob_quinquenio_mun

#############################################################################

def estructura_totales(df):
    '''
    Función para estructurar el conjunto de datos con los valores de población totales por año.
    
    Parámetros: dataframe. 
    Regresa: un dataframe estructurado a nivel estatal o municipal, de acuerdo con el parámetro de entrada.
    '''
    if 'cve_ent' in df.columns:
        estructura = df.melt(id_vars=['cve_ent'])
        estructura = estructura.groupby(by=['cve_ent','variable']).sum()
        estructura = estructura.reset_index()
        estructura = estructura.astype({ 'cve_ent': 'string', 'variable': 'string', 'value': 'Int64'})
        estructura['anio'] = estructura['variable']

        for idx, row in estructura.iterrows():
            estructura['anio'].iloc[idx] = estructura['anio'].iloc[idx][:4]

        estructura.rename(columns={'value':'cantidad_pob'}, inplace=True)
        estructura = estructura[['cve_ent', 'anio', 'cantidad_pob']]
        
        return estructura
        
    if 'cvegeomun' in df.columns:
        estructura = df.melt(id_vars=['cvegeomun'])
        estructura = estructura.groupby(by=['cvegeomun','variable']).sum()
        estructura = estructura.reset_index()
        estructura = estructura.astype({ 'cvegeomun': 'string', 'variable': 'string', 'value': 'Int64'})
        estructura['anio'] = estructura['variable']

        for idx, row in estructura.iterrows():
            estructura['anio'].iloc[idx] = estructura['anio'].iloc[idx][:4]

        estructura.rename(columns={'value':'cantidad_pob'}, inplace=True)
        estructura = estructura[['cvegeomun', 'anio', 'cantidad_pob']]
        
        return estructura

#############################################################################

def estructura_quinquenios(df):
    if 'cve_ent' in df.columns:
        estructura = df.melt(id_vars=['cve_ent'])
        estructura = estructura.groupby(by=['cve_ent','variable']).sum()
        estructura = estructura.reset_index()
        estructura = estructura.astype({ 'cve_ent': 'string', 'variable': 'string', 'value': 'Int64'})
        estructura['anio'] = estructura['variable']
        estructura['quinquenio'] = estructura['variable']
        
        for idx, row in estructura.iterrows():
            estructura['anio'].iloc[idx] = estructura['anio'].iloc[idx][:4]
            estructura['quinquenio'].iloc[idx] = estructura['quinquenio'].iloc[idx][5:]
        
        estructura.rename(columns={'value':'cantidad_pob'}, inplace=True)
        estructura = estructura[['cve_ent', 'anio', 'quinquenio', 'cantidad_pob']]
        
        return estructura
    
    if 'cvegeomun' in df.columns:
        estructura = df.melt(id_vars=['cvegeomun'])
        estructura = estructura.groupby(by=['cvegeomun','variable']).sum()
        estructura = estructura.reset_index()
        estructura = estructura.astype({ 'cvegeomun': 'string', 'variable': 'string', 'value': 'Int64'})
        estructura['anio'] = estructura['variable']
        estructura['quinquenio'] = estructura['variable']
        
        for idx, row in estructura.iterrows():
            estructura['anio'].iloc[idx] = estructura['anio'].iloc[idx][:4]
            estructura['quinquenio'].iloc[idx] = estructura['quinquenio'].iloc[idx][5:]
        
        estructura.rename(columns={'value':'cantidad_pob'}, inplace=True)
        estructura = estructura[['cvegeomun', 'anio', 'quinquenio', 'cantidad_pob']]
        
        return estructura