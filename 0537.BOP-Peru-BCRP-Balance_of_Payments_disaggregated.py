#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import datetime
import time
import requests  

from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)



# In[ ]:


# list1

# PN02581BQ	Balanza en Cuenta Corriente
# PN02582BQ	Balanza en Cuenta Corriente - Balanza Comercial
# PN02583BQ	Balanza en Cuenta Corriente - Balanza Comercial - Exportaciones FOB
# PN02584BQ	Balanza en Cuenta Corriente - Balanza Comercial - Importaciones FOB
# PN02585BQ	Balanza en Cuenta Corriente - Servicios
# PN02586BQ	Balanza en Cuenta Corriente - Servicios - Exportaciones
# PN02587BQ	Balanza en Cuenta Corriente - Servicios - Importaciones
# PN02588BQ	Balanza en Cuenta Corriente - Renta de Factores
# PN02589BQ	Balanza en Cuenta Corriente - Renta de Factores - Privado
# PN02590BQ	Balanza en Cuenta Corriente - Renta de Factores - Público
# PN02591BQ	Balanza en Cuenta Corriente - Transferencias Corrientes
# PN02592BQ	Balanza en Cuenta Corriente - Remesas del Exterior

# list2
# PN02593BQ	Cuenta Financiera
# PN02594BQ	Cuenta Financiera - Sector Privado
# PN02595BQ	Cuenta Financiera - Sector Privado - Activos
# PN02596BQ	Cuenta Financiera - Sector Privado - Pasivos
# PN02597BQ	Cuenta Financiera - Sector Público
# PN02598BQ
# PN02599BQ
# PN02600BQ
# PN02601BQ
# PN02602BQ


# PN02603BQ
# PN02604BQ
# PN02605BQ
# PN02606BQ
# PN02607BQ

list1 = ['PN02581BQ','PN02582BQ','PN02583BQ','PN02584BQ','PN02585BQ','PN02586BQ','PN02587BQ','PN02588BQ','PN02589BQ',
         'PN02590BQ','PN02591BQ','PN02592BQ']

list2 = ['PN02593BQ','PN02594BQ','PN02595BQ','PN02596BQ','PN02597BQ','PN02598BQ','PN02599BQ','PN02600BQ','PN02601BQ',
         'PN02602BQ']
         
list3 = ['PN02603BQ','PN02604BQ','PN02605BQ','PN02606BQ','PN02607BQ']


names1=['Date', 'Balanza en Cuenta Corriente', 'Balanza en Cuenta Corriente - Balanza comercial',
        'Balanza en Cuenta Corriente - Balanza comercial - Exportaciones FOB',
        'Balanza en Cuenta Corriente - Balanza comercial - Importaciones FOB',
        'Balanza en Cuenta Corriente - Servicios','Balanza en Cuenta Corriente - Servicios - Exportaciones',
        'Balanza en Cuenta Corriente - Servicios - Importaciones',
        'Balanza en Cuenta Corriente - Renta de factores',
        'Balanza en Cuenta Corriente - Renta de factores - Privado',
        'Balanza en Cuenta Corriente - Renta de factores - Público', 
        'Balanza en Cuenta Corriente - Transferencias corrientes',
        'Balanza en Cuenta Corriente - Transferencias corrientes -  del cual: Remesas del exterior']


names2 = ['Date', 'Cuenta Financiera', 'Cuenta Financiera - Sector privado', 
          'Cuenta Financiera - Sector privado - Activos', 'Cuenta Financiera - Sector privado - Pasivos',
          'Cuenta Financiera - Sector público', 'Cuenta Financiera - Sector público - Activos',
          'Cuenta Financiera - Sector público - Pasivos', 'Cuenta Financiera - Capitales de corto plazo', 
          'Cuenta Financiera - Capitales de corto plazo - Activos', 
          'Cuenta Financiera - Capitales de corto plazo - Pasivos']

names3 = ['Date', 'Financiamiento Excepcional', 'Errores y Omisiones', 'Resultado de la balanza de pagos',
          'Resultado de la balanza de pagos - Efecto valuación', 
          'Resultado de la balanza de pagos - Variación del saldo de RIN']


# In[ ]:


url = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/'


# In[ ]:


df1 = pd.read_xml(url + '-'.join(list1) + '/xml/', xpath=".//period",
                 names = names1)

df2 = pd.read_xml(url + '-'.join(list2) + '/xml/', xpath=".//period",
                 names = names2)

df3 = pd.read_xml(url + '-'.join(list3) + '/xml/', xpath=".//period",
                 names = names3)


# In[ ]:


#hago el merge entre df1, df2 y df3
df = df1.merge(df2, on='Date', how='outer')
df = df.merge(df3, on='Date', how='outer')


# In[ ]:


#Reemplazo los trimestres por el mes inicio de cada mes
trimestre ={'T1':'01', 'T2':'04', 'T3':'07','T4':'10'}

df['Date'] = df['Date'].replace(trimestre, regex=True)


# In[ ]:


#Reemplazo los n.d. por NaN
df.replace('n.d.', np.nan, inplace=True)


# In[ ]:


#Cambio el formato de la fecha
df['Date'] = pd.to_datetime(df['Date'], format = '%m.%y')


# In[ ]:


#Cambio el índice
df.set_index('Date', inplace=True)
#Agrego el nombre de la entidad
df['country'] = 'Peru'

alphacast.datasets.dataset(537).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)



