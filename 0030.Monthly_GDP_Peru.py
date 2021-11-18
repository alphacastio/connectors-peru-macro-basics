#!/usr/bin/env python
# coding: utf-8

# In[13]:


import tabula
import pandas as pd
import requests
from urllib.request import urlopen
from lxml import etree
from tabula.io import read_pdf
from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)



# In[14]:





# In[15]:


url = "http://m.inei.gob.pe/biblioteca-virtual/boletines/produccion-nacional-cifras-desestacionalizadas-9646/1/#lista"
headers = {'Content-Type': 'text/html',}
response = requests.get(url, headers=headers)
html = response.content
htmlparser = etree.HTMLParser()
tree = etree.fromstring(html, htmlparser)
pdf_address = tree.xpath(".//*[@id='row_1']/@rel")[0]
print("http://m.inei.gob.pe" + pdf_address)


# In[16]:


link = "http://m.inei.gob.pe" + pdf_address
df = tabula.io.read_pdf(link, multiple_tables=True, pages='11', output_format='dataframe')
df


# In[17]:


link = "http://m.inei.gob.pe" + pdf_address
df = tabula.io.read_pdf(link, multiple_tables=True, pages='11', output_format='dataframe')
df = pd.DataFrame(df[0])
df.dropna(how='all', inplace=True, axis=0)
df.dropna(how='all', inplace=True, axis=1)
df.columns = ['Año y mes', 'Total', 'Agricultura', 'Pesca', 'Mineria',
        'Manufactura', 'Electricidad, gas y agua', 'Construccion', 'Comercio',
        'Otros Servicios', 'Importacion y Otros Impuestos']
df["year"] = pd.to_numeric(df["Año y mes"], errors="coerce").ffill()
df = df[df["Total"].notnull()]
df = df[df["year"].notnull()]


# In[18]:


df = df[df["year"].notnull()]
df["month"] = df["Año y mes"]
df["month"] = df["month"].str.replace('Ene', "01")
df["month"] = df["month"].str.replace('Feb', "02")
df["month"] = df["month"].str.replace('Mar', "03")
df["month"] = df["month"].str.replace("Abr", "04")
df["month"] = df["month"].str.replace("May", "05")
df["month"] = df["month"].str.replace("Jun", "06")
df["month"] = df["month"].str.replace("Jul", "07")    
df["month"] = df["month"].str.replace("Ago", "08")    
df["month"] = df["month"].str.replace("Set", "09")
df["month"] = df["month"].str.replace("Oct", "10")
df["month"] = df["month"].str.replace("Nov","11")
df["month"] = df["month"].str.replace("Dic", "12")
df["day"] = 1
df["Date"] = pd.to_datetime(df[["year", "month", "day"]])
df = df.set_index("Date")
del df["Año y mes"]
del df["year"]
del df["month"]
del df["day"]
for column in df.columns:
    df[column] = pd.to_numeric(df[column].str.replace(",", "."))
df["country"] = "Peru"


alphacast.datasets.dataset(30).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)





