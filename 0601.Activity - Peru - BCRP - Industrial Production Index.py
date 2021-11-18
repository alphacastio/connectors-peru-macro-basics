#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
from datetime import datetime
from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("ALPHACAST_API_KEY")
alphacast = Alphacast(API_KEY)

#Esto es para que siempre traiga el último disponible
fecha_actual = str(datetime.now().year) + '-' + str(datetime.now().month)

#Armo listas con los ids de las variables y sus nombres
list1 = ['PN02020AM','PN02028AM','PN02029AM','PN02040AM','PN02048AM','PN02056AM',
          'PN02066AM','PN02071AM','PN02072AM','PN02077AM','PN02078AM','PN02079AM']

names1 = ['Date', 'Producción manufacturera - Procesadores de Recursos Primarios',
          'Producción manufacturera - Manufactura no Primaria',
          'Producción manufacturera - Manufactura No Primaria - Alimentos y Bebidas',
          'Producción manufacturera - Manufactura No Primaria - Textil, Cuero y Calzado',
          'Producción manufacturera - Manufactura No Primaria - Madera y Muebles',
          'Producción manufacturera - Manufactura No Primaria - Productos Químicos, Caucho y Plástico',
          'Producción manufacturera - Manufactura No Primaria - Minerales no Metálicos',
          'Producción manufacturera - Manufactura No Primaria - Industria del Hierro y Acero',
          'Producción manufacturera - Manufactura No Primaria - Productos Metálicos, Maquinaria y Equipo',
          'Producción manufacturera - Manufactura No Primaria - Manufacturas Diversas',
          'Producción manufacturera - Manufactura No Primaria - Servicios Industriales',
          'Producción manufacturera - Total']


# In[5]:


url = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/'


# In[6]:


#Comienza en 1994, es mensual
df = pd.read_xml(url + '-'.join(list1) + '/xml/1994-1/' + fecha_actual, xpath=".//period",
                 names = names1)

#Hago el reemplazo de los nombres de los meses por números
meses ={'Ene':'01', 'Feb':'02', 'Mar':'03','Abr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Ago':'08',
       'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dic':'12'}
df['Date'] = df['Date'].replace(meses, regex=True)

#Reemplazo los n.d. por NaN
df.replace('n.d.', np.nan, inplace=True)

#Cambio el formato de la fecha
df['Date'] = pd.to_datetime(df['Date'], format = '%m.%y').dt.strftime('%Y-%m-%d')

#Cambio el índice
df.set_index('Date', inplace=True)
#Agrego el nombre de la entidad
df['country'] = 'Peru'

#Cargo la data a Alphacast
alphacast.datasets.dataset(601).upload_data_from_df(df, 
                 deleteMissingFromDB = False, onConflictUpdateDB = True, uploadIndex=True)

