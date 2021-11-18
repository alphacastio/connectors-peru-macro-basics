#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import io
from zipfile import ZipFile
import pandas as pd

from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)



# In[2]:


url_file = 'https://www.inei.gob.pe/media/principales_indicadores/CalculoPBI_95.zip'
response = requests.get(url_file, stream=True)
zip_file = ZipFile(io.BytesIO(response.content))


# In[3]:


#Genero un listado con los nombres de los archivos dentro del zip
names = zip_file.namelist()
#Determino el nombre del archivo de VAB
name_file = [string for string in names if 'VA-PBI' in string][0]


# In[4]:


#Extraigo el archivo excel y lo paso a un dataframe
df = pd.read_excel(zip_file.open(name_file), header=None)


# In[5]:


#Elimino las columnas que tienen todo NaN
df.dropna(axis='columns', how='all', inplace=True)

#En la primera fila completo los NaN con el contenido de la columna previa
df.iloc[0] = df.iloc[0].fillna(method='ffill')
#Reemplazos en la clasificacion/categorizacion
df.iloc[0] = df.iloc[0].str.replace('Valor Agregado Bruto', 'VAB')
df.iloc[0] = df.iloc[0].str.replace(' - PBI ', '')
df.iloc[0] = df.iloc[0].str.replace(' - PBI', '')


# In[6]:


#Elimino las filas que están vacías segun la columna de PBI
df.dropna(subset=[df.columns[1]], how='all', inplace =True)


# In[7]:


#Cambio el nombre de las columnas para que concatenen la categoria, sector y en que unidad esta expresada
df.columns = df.iloc[0] + ' - ' + df.iloc[1]
#Remuevo las 2 primeras filas
df = df.iloc[2:]


# In[8]:


#Renombro la primera columnas como 'Date'
df.rename(columns = {df.columns[0]: 'Date'}, inplace=True)

#Cambio el formato a datetime
df['Date'] = pd.to_datetime(df['Date'], format = '%Y%m').dt.strftime('%Y-%m-%d')


# In[9]:


#Creo una lista a partir de las columnas y voy eliminando las que contengan ciertos strings
#VARIACION MENSUAL DEL INDICE DEL VAB
#VARIACION ACUMULADA DEL INDICE DEL VAB
#Año y Mes
columnas = [s for s in list(df.columns) if 'VARIACION MENSUAL DEL INDICE DEL VAB' not in s]
columnas = [s for s in columnas if 'VARIACION ACUMULADA DEL INDICE DEL VAB' not in s]
columnas = [s for s in columnas if 'Año y Mes' not in s]


# In[10]:


#Mantengo las columnas que pasaron el filtro anterior
df = df[columnas]


# In[11]:


#Seteo el indice y la entidad
df.set_index('Date', inplace=True)
df['country'] = 'Peru'

alphacast.datasets.dataset(561).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)

