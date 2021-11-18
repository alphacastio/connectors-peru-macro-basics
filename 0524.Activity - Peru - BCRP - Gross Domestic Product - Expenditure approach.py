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


##### Producto bruto interno (millones US$) desde 1980
# PN02635BQ	PBI (millones US$)

##### Producto bruto interno por tipo de gasto (millones S/ 2007) desde 1979
# PN02528AQ	Demanda Interna
# PN02529AQ	Demanda Interna - Consumo Privado
# PN02530AQ	Demanda Interna - Consumo Público
# PN02531AQ	Demanda Interna - Inversión Bruta Interna
# PN02532AQ	Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija
# PN02533AQ	Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija - Privada
# PN02534AQ	Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija - Pública
# PN02535AQ	Demanda Interna - Inversión Bruta Interna - Variación de Inventarios    desde 1980
# PN02536AQ	Exportaciones
# PN02537AQ	Importaciones
# PN02538AQ	PBI
# PN02539AQ	Demanda Interna sin Inventarios    desde 1980


#Lado Gasto
##### Producto bruto interno por tipo de gasto (millones S/)
# PN02540AQ	Demanda Interna
# PN02541AQ	Demanda Interna - Consumo Privado
# PN02542AQ	Demanda Interna - Consumo Público
# PN02543AQ	Demanda Interna - Inversión Bruta Interna
# PN02544AQ	Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija
# PN02545AQ	Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija - Privada
# PN02546AQ	Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija - Pública
# PN02547AQ	Demanda Interna - Inversión Bruta Interna - Variación de Inventarios
# PN02548AQ	Exportaciones
# PN02549AQ	Importaciones
# PN02550AQ	PBI


##### Producto bruto interno por tipo de gasto (variaciones porcentuales reales anualizadas)
# PN02517AQ	Demanda Interna
# PN02518AQ	Demanda Interna - Consumo Privado
# PN02519AQ	Demanda Interna - Consumo Público
# PN02520AQ	Demanda Interna - Inversión Bruta Interna
# PN02521AQ	Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija
# PN02522AQ	Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija - Privada
# PN02523AQ	Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija - Pública
# PN02524AQ	Exportaciones
# PN02525AQ	Importaciones
# PN02526AQ	PBI
# PN02527AQ	Demanda Interna sin Inventarios



list1 = ['PN02635BQ']
list2 = ['PN02528AQ','PN02529AQ','PN02530AQ','PN02531AQ','PN02532AQ','PN02533AQ','PN02534AQ','PN02535AQ','PN02536AQ','PN02537AQ','PN02538AQ','PN02539AQ']
list3 = ['PN02540AQ','PN02541AQ','PN02542AQ','PN02543AQ','PN02544AQ','PN02545AQ','PN02546AQ','PN02547AQ','PN02548AQ','PN02549AQ','PN02550AQ']
list4 = ['PN02517AQ','PN02518AQ','PN02519AQ','PN02520AQ','PN02521AQ','PN02522AQ','PN02523AQ','PN02524AQ','PN02525AQ','PN02526AQ','PN02527AQ']

#El orden de los nombres puede diferir respecto al request, pero es como lo devuelve la api
names1 = ['Date', 'Producto bruto interno (millones US$) - PBI (millones US$)']

names2 = ['Date', 'Producto bruto interno por tipo de gasto (millones S/ 2007) - Demanda Interna',
          'Producto bruto interno por tipo de gasto (millones S/ 2007) - Demanda Interna - Consumo Privado',
          'Producto bruto interno por tipo de gasto (millones S/ 2007) - Demanda Interna - Consumo Público',
          'Producto bruto interno por tipo de gasto (millones S/ 2007) - Demanda Interna - Inversión Bruta Interna',
          'Producto bruto interno por tipo de gasto (millones S/ 2007) - Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija',
          'Producto bruto interno por tipo de gasto (millones S/ 2007) - Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija - Privada',
          'Producto bruto interno por tipo de gasto (millones S/ 2007) - Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija - Pública',
          'Producto bruto interno por tipo de gasto (millones S/ 2007) - Demanda Interna - Inversión Bruta Interna - Variación de Inventarios',
          'Producto bruto interno por tipo de gasto (millones S/ 2007) - Exportaciones',
          'Producto bruto interno por tipo de gasto (millones S/ 2007) - Importaciones',
          'Producto bruto interno por tipo de gasto (millones S/ 2007) - PBI',
          'Producto bruto interno por tipo de gasto (millones S/ 2007) - Demanda Interna sin Inventarios']

    
names3 = ['Date', 'Producto bruto interno por tipo de gasto (millones S/) - Demanda Interna',
          'Producto bruto interno por tipo de gasto (millones S/) - Demanda Interna - Consumo Privado',
          'Producto bruto interno por tipo de gasto (millones S/) - Demanda Interna - Consumo Público',
          'Producto bruto interno por tipo de gasto (millones S/) - Demanda Interna - Inversión Bruta Interna',
          'Producto bruto interno por tipo de gasto (millones S/) - Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija',
          'Producto bruto interno por tipo de gasto (millones S/) - Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija - Privada',
          'Producto bruto interno por tipo de gasto (millones S/) - Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija - Pública',
          'Producto bruto interno por tipo de gasto (millones S/) - Demanda Interna - Inversión Bruta Interna - Variación de Inventarios',
          'Producto bruto interno por tipo de gasto (millones S/) - Exportaciones',
          'Producto bruto interno por tipo de gasto (millones S/) - Importaciones',
          'Producto bruto interno por tipo de gasto (millones S/) - PBI']

#Son las variaciones
names4 = ['Date','Producto bruto interno por tipo de gasto (variaciones porcentuales reales anualizadas) - Demanda Interna',
          'Producto bruto interno por tipo de gasto (variaciones porcentuales reales anualizadas) - Demanda Interna - Consumo Privado',
          'Producto bruto interno por tipo de gasto (variaciones porcentuales reales anualizadas) - Demanda Interna - Consumo Público',
          'Producto bruto interno por tipo de gasto (variaciones porcentuales reales anualizadas) - Demanda Interna - Inversión Bruta Interna',
          'Producto bruto interno por tipo de gasto (variaciones porcentuales reales anualizadas) - Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija',
          'Producto bruto interno por tipo de gasto (variaciones porcentuales reales anualizadas) - Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija - Privada',
          'Producto bruto interno por tipo de gasto (variaciones porcentuales reales anualizadas) - Demanda Interna - Inversión Bruta Interna - Inversión Bruta Fija - Pública',
          'Producto bruto interno por tipo de gasto (variaciones porcentuales reales anualizadas) - Exportaciones',
          'Producto bruto interno por tipo de gasto (variaciones porcentuales reales anualizadas) - Importaciones',
          'Producto bruto interno por tipo de gasto (variaciones porcentuales reales anualizadas) - PBI',
          'Producto bruto interno por tipo de gasto (variaciones porcentuales reales anualizadas) - Demanda Interna sin Inventarios']


# In[4]:


url = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/'


# In[5]:


#Creo los dataframes
#En el primero la mayoria de las series tienen datos desde 1979, solo en la de inventarios es desde 1980

df1 = pd.read_xml(url + '-'.join(list1) + '/xml/1980-1/' + fecha_actual,
                 xpath=".//period", names = names1)

df2 = pd.read_xml(url + '-'.join(list2) + '/xml/1979-1/' + fecha_actual,
                 xpath=".//period", names = names2)

df3 = pd.read_xml(url + '-'.join(list3) + '/xml/1980-1/' + fecha_actual,
                 xpath=".//period", names = names3)

df4 = pd.read_xml(url + '-'.join(list4) + '/xml/1980-1/' + fecha_actual,
                 xpath=".//period", names = names4)


# In[6]:


#hago el merge entre df1 y df2
df = df1.merge(df2, on='Date', how='outer')
#hago el merge entre df y df3
df = df.merge(df3, on='Date', how='outer')

#Hago los otros merge
df = df.merge(df4, on='Date', how='outer')

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

alphacast.datasets.dataset(524).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)

