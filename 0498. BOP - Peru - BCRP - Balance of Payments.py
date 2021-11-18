#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
from datetime import datetime

from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)



# In[ ]:


#Esto es para que siempre traiga el último disponible
fecha_actual = str(datetime.now().year) + '-' + str(datetime.now().month)


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
# PN02603BQ	Financiamiento Excepcional
# PN02604BQ	Errores y Omisiones Netos
# PN02605BQ	Resultado de Balanza de Pagos
# PN02606BQ	Resultado de Balanza de Pagos - Variación del Saldo de RIN
# PN02607BQ	Resultado de Balanza de Pagos - Efecto Valuación


#Las 2 primeras listas comienzan en enero 1985
list1 = ['PN02581BQ','PN02582BQ','PN02583BQ','PN02584BQ','PN02585BQ','PN02586BQ','PN02587BQ','PN02588BQ','PN02589BQ',
         'PN02590BQ','PN02591BQ','PN02592BQ']
list2 = ['PN02593BQ','PN02594BQ','PN02595BQ','PN02596BQ','PN02597BQ','PN02603BQ','PN02604BQ','PN02605BQ','PN02606BQ',
         'PN02607BQ']


names1=["Date", 'Balanza de pagos (millones US$) - Balanza en Cuenta Corriente',
        'Balanza de pagos (millones US$) - Balanza en Cuenta Corriente - Balanza Comercial',
        'Balanza de pagos (millones US$) - Balanza en Cuenta Corriente - Balanza Comercial - Exportaciones FOB',
        'Balanza de pagos (millones US$) - Balanza en Cuenta Corriente - Balanza Comercial - Importaciones FOB',
        'Balanza de pagos (millones US$) - Balanza en Cuenta Corriente - Servicios',
        'Balanza de pagos (millones US$) - Balanza en Cuenta Corriente - Servicios - Exportaciones',
        'Balanza de pagos (millones US$) - Balanza en Cuenta Corriente - Servicios - Importaciones',
        'Balanza de pagos (millones US$) - Balanza en Cuenta Corriente - Renta de Factores',
        'Balanza de pagos (millones US$) - Balanza en Cuenta Corriente - Renta de Factores - Privado',
        'Balanza de pagos (millones US$) - Balanza en Cuenta Corriente - Renta de Factores - Público',
        'Balanza de pagos (millones US$) - Balanza en Cuenta Corriente - Transferencias Corrientes',
        'Balanza de pagos (millones US$) - Balanza en Cuenta Corriente - Remesas del Exterior']

names2 = ["Date", 'Balanza de pagos (millones US$) - Cuenta Financiera',
          'Balanza de pagos (millones US$) - Cuenta Financiera - Sector Privado',
          'Balanza de pagos (millones US$) - Cuenta Financiera - Sector Privado - Activos',
          'Balanza de pagos (millones US$) - Cuenta Financiera - Sector Privado - Pasivos',
          'Balanza de pagos (millones US$) - Cuenta Financiera - Sector Público',
          'Balanza de pagos (millones US$) - Financiamiento Excepcional',
          'Balanza de pagos (millones US$) - Errores y Omisiones Netos',
          'Balanza de pagos (millones US$) - Resultado de Balanza de Pagos',
          'Balanza de pagos (millones US$) - Resultado de Balanza de Pagos - Variación del Saldo de RIN',
          'Balanza de pagos (millones US$) - Resultado de Balanza de Pagos - Efecto Valuación']


# In[ ]:


url = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/'


# In[ ]:


#Comienza en 1985
df1 = pd.read_xml(url + '-'.join(list1) + '/xml/', xpath=".//period",
                 names = names1)

#Comienza en 1985
df2 = pd.read_xml(url + '-'.join(list2) + '/xml/', xpath=".//period",
                 names = names2)


# In[ ]:


#hago el merge entre df1 y df2
df = df1.merge(df2, on='Date', how='outer')


# In[ ]:


#Reemplazo los trimestres por el mes inicio de cada mes
trimestre ={'T1':'01', 'T2':'04', 'T3':'07','T4':'10'}

df['Date'] = df['Date'].replace(trimestre, regex=True)

#Reemplazo los n.d. por NaN
df.replace('n.d.', np.nan, inplace=True)


# In[ ]:


#Cambio el formato de la fecha
df['Date'] = pd.to_datetime(df['Date'], format = '%m.%y')

#Cambio el índice
df.set_index('Date', inplace=True)
#Agrego el nombre de la entidad
df['country'] = 'Peru'

alphacast.datasets.dataset(498).upload_data_from_df(df, 
    deleteMissingFromDB = False, onConflictUpdateDB = True, uploadIndex=True)



