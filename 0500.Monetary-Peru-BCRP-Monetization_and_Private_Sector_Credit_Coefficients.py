#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import numpy as np
import datetime
import urllib
import time
from urllib.request import urlopen
import requests  

from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)



# In[9]:


url = "https://estadisticas.bcrp.gob.pe/estadisticas/series/exceltrimestrales/index/codigos/%27PN03492MQ%27%2C%27PN03493MQ%27%2C%27PN03494MQ%27%2C%27PN03495MQ%27%2C%27PN03496MQ%27%2C%27PN03497MQ%27%2C%27PN03498MQ%27%2C%27PN03499MQ%27%2C%27PN03500MQ%27/grupos/0/anio1/2019/anio2/2021/trim1/1/trim2/1/dia1/0/dia2/0"
r = requests.get(url ,allow_redirects=False, verify=False)
df = pd.read_excel(r.content, skiprows= 1)


# In[10]:


df = df.replace(['n.d.'],[np.nan]) 
df = df.iloc[: , 1:]
df["Date"] = pd.date_range(start='1/1/2019', end='4/1/2021', freq='Q')
df["country"] = "Peru"
df = df.set_index(['Date'])

alphacast.datasets.dataset(500).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)





