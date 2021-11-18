#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from datetime import datetime

from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)



# In[2]:


#Esto es para que siempre traiga el último disponible
fecha_actual = str(datetime.now().year) + '-' + str(datetime.now().month)


# In[3]:


#Lado produccion
#### Producto bruto interno (millones de soles constantes de 2007) desde 1979
# PN37684AQ	Agropecuario
# PN37685AQ	Pesca
# PN37686AQ	Minería e Hidrocarburos
# PN37687AQ	Manufactura
# PN37688AQ	Electricidad y Agua
# PN37689AQ	Construcción
# PN37690AQ	Comercio
# PN37691AQ	Servicios
# PN37692AQ	PBI Global
# PN37693AQ	Sectores primarios
# PN37694AQ	Sectores no primarios

#### Producto bruto interno (índice 2007 = 100) desde 1980
# PN02508AQ	Agropecuario
# PN02509AQ	Pesca
# PN02510AQ	Minería e Hidrocarburos
# PN02511AQ	Manufactura
# PN02512AQ	Electricidad y Agua
# PN02513AQ	Construcción
# PN02514AQ	Comercio
# PN02515AQ	Servicios
# PN02516AQ	PBI Global
# PN37682AQ	Sectores primarios
# PN37683AQ	Sectores no primarios


list1 = ['PN37684AQ','PN37685AQ','PN37686AQ','PN37687AQ','PN37688AQ','PN37689AQ','PN37690AQ','PN37691AQ','PN37692AQ','PN37693AQ','PN37694AQ']
list2 = ['PN02508AQ','PN02509AQ','PN02510AQ','PN02511AQ','PN02512AQ','PN02513AQ','PN02514AQ','PN02515AQ','PN02516AQ','PN37682AQ','PN37683AQ']


#Lado de la produccion
names1 = ['Date', 'Producto bruto interno (millones de soles constantes de 2007) - Agropecuario',
          'Producto bruto interno (millones de soles constantes de 2007) - Pesca',
          'Producto bruto interno (millones de soles constantes de 2007) - Minería e Hidrocarburos',
          'Producto bruto interno (millones de soles constantes de 2007) - Manufactura',
          'Producto bruto interno (millones de soles constantes de 2007) - Electricidad y Agua',
          'Producto bruto interno (millones de soles constantes de 2007) - Construcción',
          'Producto bruto interno (millones de soles constantes de 2007) - Comercio',
          'Producto bruto interno (millones de soles constantes de 2007) - Servicios',
          'Producto bruto interno (millones de soles constantes de 2007) - PBI Global',
          'Producto bruto interno (millones de soles constantes de 2007) - Sectores primarios',
          'Producto bruto interno (millones de soles constantes de 2007) - Sectores no primarios']

names2 = ['Date', 'Producto bruto interno (índice 2007 = 100) - Agropecuario',
          'Producto bruto interno (índice 2007 = 100) - Pesca',
          'Producto bruto interno (índice 2007 = 100) - Minería e Hidrocarburos',
          'Producto bruto interno (índice 2007 = 100) - Manufactura',
          'Producto bruto interno (índice 2007 = 100) - Electricidad y Agua',
          'Producto bruto interno (índice 2007 = 100) - Construcción',
          'Producto bruto interno (índice 2007 = 100) - Comercio',
          'Producto bruto interno (índice 2007 = 100) - Servicios',
          'Producto bruto interno (índice 2007 = 100) - PBI Global',
          'Producto bruto interno (índice 2007 = 100) - Sectores primarios',
          'Producto bruto interno (índice 2007 = 100) - Sectores no primarios']


# In[4]:


url = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/'


# In[5]:


#Creo los dataframes
#En el primero la mayoria de las series tienen datos desde 1979, solo en la de inventarios es desde 1980
df1 = pd.read_xml(url + '-'.join(list1) + '/xml/1979-1/' + fecha_actual,
                 xpath=".//period", names = names1)

df2 = pd.read_xml(url + '-'.join(list2) + '/xml/1980-1/' + fecha_actual,
                 xpath=".//period", names = names2)


# In[6]:


#hago el merge entre df1 y df2
df = df1.merge(df2, on='Date', how='outer')

#Reemplazo los trimestres por el mes inicio de cada mes
trimestre ={'T1':'01', 'T2':'04', 'T3':'07','T4':'10'}

df['Date'] = df['Date'].replace(trimestre, regex=True)

#Reemplazo los n.d. (no data) por NaN
df.replace('n.d.', np.nan, inplace=True)


# In[7]:


#Cambio el formato de la fecha
df['Date'] = pd.to_datetime(df['Date'], format = '%m.%y').dt.strftime('%Y-%m-%d')

#Cambio el índice
df.set_index('Date', inplace=True)
#Agrego el nombre de la entidad
df['country'] = 'Peru'

#Ordeno los valores en base al índice
df.sort_index(axis='index', ascending=True, inplace=True)


alphacast.datasets.dataset(560).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)

