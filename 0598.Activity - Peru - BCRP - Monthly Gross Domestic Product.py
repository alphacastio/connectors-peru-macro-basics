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


### Producto bruto interno y demanda interna (índice 2007=100) Comienza en 2003
# PN01755AM	Agropecuario
# PN01756AM	Agropecuario - Agrícola
# PN01757AM	Agropecuario - Pecuario
# PN01758AM	Pesca
# PN01759AM	Minería e Hidrocarburos
# PN01760AM	Minería e Hidrocarburos - Minería Metálica
# PN01761AM	Minería e Hidrocarburos - Hidrocarburos
# PN01762AM	Manufactura
# PN01763AM	Manufactura - Procesadores Recursos Primarios
# PN01764AM	Manufactura - Manufactura no Primaria
# PN01765AM	Electricidad y Agua
# PN01766AM	Construcción
# PN01767AM	Comercio
# PN01768AM	Otros Servicios
# PN01769AM	Derechos de Importación y Otros Impuestos
# PN01770AM	PBI
# PN01771AM	Sectores Primarios
# PN01772AM	Sectores no Primarios
# PN01773AM	PBI Desestacionalizado - mensual
# PN38081AM	PBI Desestacionalizado - Promedio móvil 3 meses
# PN14206AM	Indicador de Demanda Interna sin inventarios
# PN01774AM	Indicador de Demanda Interna


list1= ['PN01755AM','PN01756AM','PN01757AM','PN01758AM','PN01759AM','PN01760AM','PN01761AM','PN01762AM',
        'PN01763AM','PN01764AM','PN01765AM','PN01766AM','PN01767AM','PN01768AM','PN01769AM','PN01770AM',
        'PN01771AM','PN01772AM','PN01773AM','PN38081AM','PN14206AM','PN01774AM']

names1 = ['Date', 'Producto bruto interno y demanda interna (índice 2007=100) - Agropecuario',
          'Producto bruto interno y demanda interna (índice 2007=100) - Agropecuario - Agrícola',
          'Producto bruto interno y demanda interna (índice 2007=100) - Agropecuario - Pecuario',
          'Producto bruto interno y demanda interna (índice 2007=100) - Pesca',
          'Producto bruto interno y demanda interna (índice 2007=100) - Minería e Hidrocarburos',
          'Producto bruto interno y demanda interna (índice 2007=100) - Minería e Hidrocarburos - Minería Metálica',
          'Producto bruto interno y demanda interna (índice 2007=100) - Minería e Hidrocarburos - Hidrocarburos',
          'Producto bruto interno y demanda interna (índice 2007=100) - Manufactura',
          'Producto bruto interno y demanda interna (índice 2007=100) - Manufactura - Procesadores Recursos Primarios',
          'Producto bruto interno y demanda interna (índice 2007=100) - Manufactura - Manufactura no Primaria',
          'Producto bruto interno y demanda interna (índice 2007=100) - Electricidad y Agua',
          'Producto bruto interno y demanda interna (índice 2007=100) - Construcción',
          'Producto bruto interno y demanda interna (índice 2007=100) - Comercio',
          'Producto bruto interno y demanda interna (índice 2007=100) - Otros Servicios',
          'Producto bruto interno y demanda interna (índice 2007=100) - Derechos de Importación y Otros Impuestos',
          'Producto bruto interno y demanda interna (índice 2007=100) - PBI',
          'Producto bruto interno y demanda interna (índice 2007=100) - Sectores Primarios',
          'Producto bruto interno y demanda interna (índice 2007=100) - Sectores no Primarios',
          'Producto bruto interno y demanda interna (índice 2007=100) - PBI Desestacionalizado - mensual',
          'Producto bruto interno y demanda interna (índice 2007=100) - Indicador de Demanda Interna',
          'Producto bruto interno y demanda interna (índice 2007=100) - Indicador de Demanda Interna sin inventarios',
          'Producto bruto interno y demanda interna (índice 2007=100) - PBI Desestacionalizado - Promedio móvil 3 meses']


# In[4]:


url = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/'


# In[5]:


#Comienza en 2003
df = pd.read_xml(url + '-'.join(list1) + '/xml/2003-1/' + fecha_actual, xpath=".//period",
                 names = names1)


# In[6]:


#Hago el reemplazo de los nombres de los meses por números
meses ={'Ene':'01', 'Feb':'02', 'Mar':'03','Abr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Ago':'08',
       'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dic':'12'}
df['Date'] = df['Date'].replace(meses, regex=True)

#Reemplazo los n.d. por NaN
df.replace('n.d.', np.nan, inplace=True)


# In[7]:


#Cambio el formato de la fecha
df['Date'] = pd.to_datetime(df['Date'], format = '%m.%y').dt.strftime('%Y-%m-%d')

#Cambio el índice
df.set_index('Date', inplace=True)
#Agrego el nombre de la entidad
df['country'] = 'Peru'


# In[9]:


alphacast.datasets.dataset(598).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)


# In[ ]:




