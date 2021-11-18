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


#Defino las series a descargar
#Las primeras comienzan en 1985, las últimas 4 en 1994

### list1
# PN01504BM	Agrícolas
# PN01505BM	Agrícolas - Algodón
# PN01508BM	Agrícolas - Azúcar
# PN01511BM	Agrícolas - Café
# PN01515BM	Mineros
# PN01516BM	Mineros - Cobre
# PN01519BM	Mineros - Estaño
# PN01522BM	Mineros - Hierro
# PN01525BM	Mineros - Oro

#### list2
# PN01528BM	Mineros - Plata Refinada
# PN01531BM	Mineros - Plomo
# PN01534BM	Mineros - Zinc
# PN01497BM	Pesqueros
# PN01501BM	Pesqueros - Aceite de Pescado
# PN01498BM	Pesqueros - Harina de Pescado
# PN01541BM	Petróleo y Gas Natural
# PN01542BM	Petróleo y Gas Natural - Petróleo Crudo y Derivados
# PN01548BM	Productos Tradicionales

### list3
# PN01514BM	Agrícolas - Resto de Agrícolas
# PN01537BM	Mineros - Molibdeno
# PN01540BM	Mineros - Resto de Mineros
# PN01545BM	Petróleo y Gas Natural - Gas Natural



#### Exportaciones de productos tradicionales (volumen) desde 1985
# PN01499BM	Pesqueros - Harina de Pescado - Volumen (miles de toneladas)
# PN01502BM	Pesqueros - Aceite de Pescado - Volumen (miles de toneladas)
# PN01506BM	Agrícolas - Algodón - Volumen (miles de toneladas)
# PN01509BM	Agrícolas - Azúcar - Volumen (miles de toneladas)
# PN01512BM	Agrícolas - Café - Volumen (miles de toneladas)
# PN01517BM	Mineros - Cobre - Volumen (miles de toneladas)
# PN01520BM	Mineros - Estaño - Volumen (miles de toneladas)
# PN01523BM	Mineros - Hierro - Volumen (millones de toneladas)
# PN01526BM	Mineros - Oro - Volumen (miles de onzas troy)
# PN01529BM	Mineros - Plata Refinada - Volumen (millones de onzas troy)
# PN01532BM	Mineros - Plomo - Volumen (miles de toneladas)
# PN01535BM	Mineros - Zinc - Volumen (miles de toneladas)
# PN01538BM	Mineros - Molibdeno - Volumen (miles de toneladas)
# PN01543BM	Petróleo y Gas Natural - Petróleo Crudo y Derivados - Volumen (millones de barrile
# PN01546BM	Petróleo y Gas Natural - Gas Natural - Volumen (miles de m3)

### Exportaciones de productos tradicionales (precios) desde 1985
# PN01500BM	Pesqueros - Harina de Pescado - Precio (US$ por toneladas)
# PN01503BM	Pesqueros - Aceite de Pescado - Precio (US$ por toneladas)
# PN01507BM	Agrícolas - Algodón - Precio (US$ por toneladas)
# PN01510BM	Agrícolas - Azúcar - Precio (US$ por toneladas)
# PN01513BM	Agrícolas - Café - Precio (US$ por toneladas)
# PN01518BM	Mineros - Cobre - Precio (¢US$ por libras)
# PN01521BM	Mineros - Estaño - Precio (¢US$ por libras)
# PN01524BM	Mineros - Hierro - Precio (US$ por toneladas)
# PN01527BM	Mineros - Oro - Precio (US$ por onzas troy)
# PN01530BM	Mineros - Plata Refinada - Precio (US$ por onzas troy)
# PN01533BM	Mineros - Plomo - Precio (¢US$ por libras)
# PN01536BM	Mineros - Zinc - Precio (¢US$ por libras)
# PN01539BM	Mineros - Molibdeno - Precio (¢US$ por libras) desde 1994
# PN01544BM	Petróleo y Gas Natural - Petróleo Crudo y Derivados - Precio (US$ por barriles)
# PN01547BM	Petróleo y Gas Natural - Gas Natural - Precio (US$ por m3) desde 1994



#Las 2 primeras listas comienzan en enero 1985
list1 = ['PN01504BM','PN01505BM','PN01508BM','PN01511BM','PN01515BM','PN01516BM','PN01519BM','PN01522BM','PN01525BM']
list2 = ['PN01528BM','PN01531BM','PN01534BM','PN01497BM','PN01501BM','PN01498BM','PN01541BM','PN01542BM','PN01548BM']
list3 = ['PN01514BM','PN01537BM','PN01540BM','PN01545BM']

#Comienzan en 1985, solo algunas de la ultima lista comienzan en 1994
list4 = ['PN01499BM','PN01502BM','PN01506BM','PN01509BM','PN01512BM','PN01517BM','PN01520BM','PN01523BM','PN01526BM',
         'PN01529BM','PN01532BM','PN01535BM','PN01538BM','PN01543BM','PN01546BM']
list5 = ['PN01500BM','PN01503BM','PN01507BM','PN01510BM','PN01513BM','PN01518BM','PN01521BM','PN01524BM','PN01527BM',
         'PN01530BM','PN01533BM','PN01536BM','PN01539BM','PN01544BM','PN01547BM']



names1=["Date", "Exportaciones de productos tradicionales - valores FOB (millones US$) - Agrícolas" ,
        "Exportaciones de productos tradicionales - valores FOB (millones US$) - Agrícolas - Algodón",
        "Exportaciones de productos tradicionales - valores FOB (millones US$) - Agrícolas - Azúcar" ,
        "Exportaciones de productos tradicionales - valores FOB (millones US$) - Agrícolas - Café" ,
        "Exportaciones de productos tradicionales - valores FOB (millones US$) - Mineros",
        "Exportaciones de productos tradicionales - valores FOB (millones US$) - Mineros - Cobre",
        "Exportaciones de productos tradicionales - valores FOB (millones US$) - Mineros - Estaño",
        "Exportaciones de productos tradicionales - valores FOB (millones US$) - Mineros - Hierro",
        "Exportaciones de productos tradicionales - valores FOB (millones US$) - Mineros - Oro"]

names2 = ["Date", "Exportaciones de productos tradicionales - valores FOB (millones US$) - Pesqueros",
          "Exportaciones de productos tradicionales - valores FOB (millones US$) - Pesqueros - Harina de Pescado",
          "Exportaciones de productos tradicionales - valores FOB (millones US$) - Pesqueros - Aceite de Pescado",
          "Exportaciones de productos tradicionales - valores FOB (millones US$) - Mineros - Plata Refinada",
          "Exportaciones de productos tradicionales - valores FOB (millones US$) - Mineros - Plomo",
          "Exportaciones de productos tradicionales - valores FOB (millones US$) - Mineros - Zinc",
          "Exportaciones de productos tradicionales - valores FOB (millones US$) - Petróleo y Gas Natural",
          "Exportaciones de productos tradicionales - valores FOB (millones US$) - Petróleo y Gas Natural - Petróleo Crudo y Derivados",
          "Exportaciones de productos tradicionales - valores FOB (millones US$) - Productos Tradicionales"]

names3= ["Date","Exportaciones de productos tradicionales - valores FOB (millones US$) - Agrícolas - Resto de Agrícolas", 
        "Exportaciones de productos tradicionales - valores FOB (millones US$) - Mineros - Molibdeno",
        "Exportaciones de productos tradicionales - valores FOB (millones US$) - Mineros - Resto de Mineros",
        "Exportaciones de productos tradicionales - valores FOB (millones US$) - Petróleo y Gas Natural - Gas Natural"]

names4 = ['Date', 'Exportaciones de productos tradicionales (volumen) - Pesqueros - Harina de Pescado - Volumen (miles de toneladas)',
          'Exportaciones de productos tradicionales (volumen) - Pesqueros - Aceite de Pescado - Volumen (miles de toneladas)',
          'Exportaciones de productos tradicionales (volumen) - Agrícolas - Algodón - Volumen (miles de toneladas)',
          'Exportaciones de productos tradicionales (volumen) - Agrícolas - Azúcar - Volumen (miles de toneladas)',
          'Exportaciones de productos tradicionales (volumen) - Agrícolas - Café - Volumen (miles de toneladas)',
          'Exportaciones de productos tradicionales (volumen) - Mineros - Cobre - Volumen (miles de toneladas)',
          'Exportaciones de productos tradicionales (volumen) - Mineros - Estaño - Volumen (miles de toneladas)',
          'Exportaciones de productos tradicionales (volumen) - Mineros - Hierro - Volumen (millones de toneladas)',
          'Exportaciones de productos tradicionales (volumen) - Mineros - Oro - Volumen (miles de onzas troy)',
          'Exportaciones de productos tradicionales (volumen) - Mineros - Plata Refinada - Volumen (millones de onzas troy)',
          'Exportaciones de productos tradicionales (volumen) - Mineros - Plomo - Volumen (miles de toneladas)',
          'Exportaciones de productos tradicionales (volumen) - Mineros - Zinc - Volumen (miles de toneladas)',
          'Exportaciones de productos tradicionales (volumen) - Mineros - Molibdeno - Volumen (miles de toneladas)',
          'Exportaciones de productos tradicionales (volumen) - Petróleo y Gas Natural - Petróleo Crudo y Derivados - Volumen (millones de barriles)',
          'Exportaciones de productos tradicionales (volumen) - Petróleo y Gas Natural - Gas Natural - Volumen (miles de m3)']

names5 = ['Date','Exportaciones de productos tradicionales (precios) - Pesqueros - Harina de Pescado - Precio (US$ por toneladas)',
          'Exportaciones de productos tradicionales (precios) - Pesqueros - Aceite de Pescado - Precio (US$ por toneladas)',
          'Exportaciones de productos tradicionales (precios) - Agrícolas - Algodón - Precio (US$ por toneladas)',
          'Exportaciones de productos tradicionales (precios) - Agrícolas - Azúcar - Precio (US$ por toneladas)',
          'Exportaciones de productos tradicionales (precios) - Agrícolas - Café - Precio (US$ por toneladas)',
          'Exportaciones de productos tradicionales (precios) - Mineros - Cobre - Precio (¢US$ por libras)',
          'Exportaciones de productos tradicionales (precios) - Mineros - Estaño - Precio (¢US$ por libras)',
          'Exportaciones de productos tradicionales (precios) - Mineros - Hierro - Precio (US$ por toneladas)',
          'Exportaciones de productos tradicionales (precios) - Mineros - Oro - Precio (US$ por onzas troy)',
          'Exportaciones de productos tradicionales (precios) - Mineros - Plata Refinada - Precio (US$ por onzas troy)',
          'Exportaciones de productos tradicionales (precios) - Mineros - Plomo - Precio (¢US$ por libras)',
          'Exportaciones de productos tradicionales (precios) - Mineros - Zinc - Precio (¢US$ por libras)',
          'Exportaciones de productos tradicionales (precios) - Mineros - Molibdeno - Precio (¢US$ por libras)',
          'Exportaciones de productos tradicionales (precios) - Petróleo y Gas Natural - Petróleo Crudo y Derivados - Precio (US$ por barriles)',
          'Exportaciones de productos tradicionales (precios) - Petróleo y Gas Natural - Gas Natural - Precio (US$ por m3)']


# In[4]:


url = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/'


# In[5]:


#La api no descarga de manera ordenada de acuerdo a la lista, al menos en el segundo caso

#Comienza en 1985
df1 = pd.read_xml(url + '-'.join(list1) + '/xml/1985-1/' + fecha_actual, xpath=".//period",
                 names = names1)

#Comienza en 1985
df2 = pd.read_xml(url + '-'.join(list2) + '/xml/1985-1/' + fecha_actual, xpath=".//period",
                 names = names2)

#Comienza en 1994
df3 = pd.read_xml(url + '-'.join(list3) + '/xml/1994-1/' + fecha_actual, xpath=".//period",
                 names = names3)

df4 = pd.read_xml(url + '-'.join(list4) + '/xml/1985-1/' + fecha_actual, xpath=".//period",
                 names = names4)

df5 = pd.read_xml(url + '-'.join(list5) + '/xml/1985-1/' + fecha_actual, xpath=".//period",
                 names = names5)


# In[6]:


#hago el merge entre df1 y df2
df = df1.merge(df2, on='Date', how='outer')
#hago el merge entre df y df3
df = df.merge(df3, on='Date', how='outer')

#hago el merge entre df y df4
df = df.merge(df4, on='Date', how='outer')

#hago el merge entre df y df5
df = df.merge(df5, on='Date', how='outer')


# In[7]:


#Hago el reemplazo de los nombres de los meses por números
meses ={'Ene':'01', 'Feb':'02', 'Mar':'03','Abr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Ago':'08',
       'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dic':'12'}
df['Date'] = df['Date'].replace(meses, regex=True)

#Reemplazo los n.d. por NaN
df.replace('n.d.', np.nan, inplace=True)


# In[8]:


#Cambio el formato de la fecha
df['Date'] = pd.to_datetime(df['Date'], format = '%m.%y').dt.strftime('%Y-%m-%d')

#Cambio el índice
df.set_index('Date', inplace=True)
#Agrego el nombre de la entidad
df['country'] = 'Peru'


alphacast.datasets.dataset(517).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)




