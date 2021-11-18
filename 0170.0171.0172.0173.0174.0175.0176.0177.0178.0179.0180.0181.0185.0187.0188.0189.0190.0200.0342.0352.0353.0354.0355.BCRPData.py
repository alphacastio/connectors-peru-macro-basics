#!/usr/bin/env python
# coding: utf-8

# In[3]:


#!/usr/bin/env python
# coding: utf-8

# In[35]:


import pandas as pd
import numpy as np

import requests
import io
import html
from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)



# In[158]:


def fix_date(df):
    if "b'Trimestre/Año" in df.columns:
        df["b'Trimestre/Año"] = df["b'Trimestre/Año"].str.replace(r'T(\d).(\d+)', r'\2-Q\1')
        df["Q"] = df["b'Trimestre/Año"].str.split("-", expand=True)[1]
        df["Y"] = df["b'Trimestre/Año"].str.split("-", expand=True)[0]
        df["Y2"] = df["b'Trimestre/Año"].str.split("-", expand=True)[0]
        df.loc[df["Y2"] > "29", "Y"] = "19" +  df["Y2"]
        df.loc[df["Y2"] <= "29", "Y"] = "20" +  df["Y2"]
        df["b'Trimestre/Año"] = df["Y"]+"-"+df["Q"]
        df['Date'] = pd.PeriodIndex(df["b'Trimestre/Año"], freq='Q').to_timestamp()
        del df["b'Trimestre/Año"]
        del df["Y"]
        del df["Y2"]
        del df["Q"]

    if "b'Día/Mes/Año" in df.columns:
        df["Day"] = df["b'Día/Mes/Año"].str.split(pat=".", expand=True)[0]
        df["Month"] = df["b'Día/Mes/Año"].str.split(pat=".", expand=True)[1]
        df["Year"] = df["b'Día/Mes/Año"].str.split(pat=".", expand=True)[2]
        df["Y2"] = df["b'Día/Mes/Año"].str.split(pat=".", expand=True)[2]
        df.loc[df["Y2"] > "29", "Year"] = "19" +  df["Y2"]
        df.loc[df["Y2"] <= "29", "Year"] = "20" +  df["Y2"]
        df["Month"] = df["Month"].replace(
            {'Abr': 4, 'Ago': 8, 
             'Dic':12, 'Ene': 1, 
             'Feb': 2,'Jul': 7, 
             'Jun': 6, 'Mar': 3, 
             'May': 5 , 'Nov': 11, 
             'Oct': 10, 'Sep':9 }
            )
        df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]], errors="coerce")
        del df["Year"]
        del df["Month"]
        del df["Day"]
        del df["b'Día/Mes/Año"]
        
        

    if "b'Mes/Año" in df.columns:
        df["Month"] = df["b'Mes/Año"].str.split(pat=".", expand=True)[0]
        df["Year"] = df["b'Mes/Año"].str.split(pat=".", expand=True)[1]
        df["Month"] = df["Month"].replace(
            {'Abr': 4, 'Ago': 8, 
             'Dic':12, 'Ene': 1, 
             'Feb': 2,'Jul': 7, 
             'Jun': 6, 'Mar': 3, 
             'May': 5 , 'Nov': 11, 
             'Oct': 10, 'Sep':9 }
            )
        df["Day"] = 1
        df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]], errors="coerce")
        del df["Year"]
        del df["Month"]
        del df["Day"]
        del df["b'Mes/Año"]
    return df


# In[190]:


variables = { 
            170 : {
            "variables" : ["PN03371FQ", "PN03372FQ", "PN03373FQ", "PN03374FQ", "PN03375FQ", "PN03376FQ", "PN03377FQ", "PN03378FQ", "PN03379FQ", "PN03380FQ", "PN37923FQ", "PN37924FQ", "PN03381FQ", "PN03382FQ", "PN03383FQ", "PN03384FQ", "PN03385FQ", "PN03386FQ", "PN37925FQ", "PN03388FQ", "PN03389FQ", "PN03390FQ", "PN03391FQ", "PN03392FQ", "PN37931FQ", "PN03393FQ", "PN03394FQ", "PN03395FQ", "PN03396FQ", "PN03397FQ", "PN03398FQ", "PN03399FQ", "PN03400FQ", "PN03401FQ", "PN03402FQ", "PN03403FQ", "PN03404FQ", "PN03405FQ", "PN03406FQ", "PN03407FQ", "PN03408FQ", "PN03409FQ", "PN03410FQ", "PN03411FQ", "PN03412FQ", "PN37933FQ", "PN03413FQ", "PN37926FQ", "PN03414FQ", "PN37934FQ", "PN37935FQ", "PN03415FQ", "PN03416FQ", "PN03417FQ", "PN03418FQ", "PN03431FQ", "PN03419FQ", "PN03420FQ", "PN03421FQ", "PN03422FQ", "PN03423FQ", "PN03424FQ", "PN03425FQ", "PN03426FQ", "PN03427FQ", "PN03428FQ", "PN03429FQ"],
            "dataset_name": ["Saldo de la deuda del sector público no financiero (millones S/)"]
                }, 
            171 : {
            "variables" : ["PN03432FQ", "PN03433FQ", "PN03434FQ", "PN03435FQ", "PN03436FQ", "PN03437FQ", "PN03438FQ", "PN03439FQ", "PN03440FQ", "PN03441FQ", "PN37927FQ", "PN37928FQ", "PN03442FQ", "PN03443FQ", "PN03444FQ", "PN03445FQ", "PN03446FQ", "PN03447FQ", "PN37929FQ", "PN03449FQ", "PN03450FQ", "PN03451FQ", "PN03452FQ", "PN03453FQ", "PN37932FQ", "PN03454FQ", "PN03455FQ", "PN03456FQ", "PN03457FQ", "PN03458FQ", "PN03459FQ", "PN03460FQ", "PN03461FQ", "PN03462FQ", "PN03463FQ", "PN03464FQ", "PN03465FQ", "PN03466FQ", "PN03467FQ", "PN03468FQ", "PN03469FQ", "PN03470FQ", "PN03471FQ", "PN03472FQ", "PN03473FQ", "PN37936FQ", "PN03474FQ", "PN37930FQ", "PN03475FQ", "PN37937FQ", "PN37938FQ", "PN03476FQ", "PN03477FQ", "PN03478FQ", "PN03479FQ", "PN03480FQ", "PN03491FQ", "PN03481FQ", "PN03482FQ", "PN03483FQ", "PN03484FQ", "PN03485FQ", "PN03486FQ", "PN03487FQ", "PN03488FQ", "PN03489FQ", "PN03490FQ" ],
            "dataset_name": ["Saldo de la deuda del sector público no financiero (porcentaje del PBI)"]
                }, 
            172 : {
            "variables" : ["PD12301MD", "PD04677MD", "PD04678MD", "PD04679MD", "PD04680MD", "PD04681MD", "PD04682MD", "PD04683MD", "PD04684MD", "PD04685MD", "PD04686MD", "PD04687MD", "PD04688MD", "PD04689MD", "PD04690MD", "PD04691MD", "PD04692MD", "PD04693MD", "PD31893DD", "PD31894DD", ],
            "dataset_name": ["Tasas de interés"]
                }, 

            173 : {
            "variables" : ["PN01270PM", "PN01288PM", "PN01289PM", "PN09813PM", "PN01290PM", "PN09814PM", "PN01291PM", "PN01292PM", "PN01293PM", "PN01336PM", "PN01337PM", "PN01338PM", "PN09815PM", "PN01294PM", ],
            "dataset_name": ["Índice de precios Lima Metropolitana (índice 2009 = 100)"]
                },     
            
            174 : {
            "variables" : ["PN01296PM", "PN01297PM", "PN01298PM", "PN01299PM", "PN01300PM", "PN01301PM", "PN01302PM", "PN01303PM", "PN01304PM", "PN01305PM", "PN01306PM", "PN01308PM", "PN01309PM", "PN01310PM", "PN01311PM", ],
            "dataset_name": ["Índice de precios al consumidor Lima Metropolitana: clasificación sectorial (variación porcentual)"]
                },     

            175 : {
            "variables" : ["PN01366PM", "PN01367PM", "PN01368PM", "PN01369PM", "PN01370PM", "PN01372PM", "PN01373PM", "PN01374PM", "PN01375PM", "PN01376PM", "PN01377PM", "PN01378PM", "PN01379PM", "PN01380PM", "PN01381PM", "PN01382PM",],
            "dataset_name": ["Índice de precios al consumidor Lima Metropolitana: clasificación transables - no transables (variación porcentual)"]
                },
                 
            176 : {
            "variables" : ["PN02124PM", "PN37695PM", "PN37696PM", "PN37697PM", "PN02125PM", "PN31879GM", "PN31880GM", "PN31881GM", "PN31882GM", "PN31883GM", "PN31884GM", "PN31885GM", "PN31886GM", "PN38063GM", "PN38064GM", "PN38065GM", "PN38066GM", "PN38067GM", "PN38068GM", "PN38050GM", "PN38051GM", "PN38052GM", "PN38053GM", "PN38054GM", "PN38055GM", "PN38056GM", "PN38057GM", "PN38058GM", "PN38059GM", "PN38060GM", "PN38061GM", "PN38062GM", "PN38069GM", "PN38070GM", "PN38071GM"],
            "dataset_name": ["REMUNERACIONES Y EMPLEO"]
                },  
    
            177 : {
            "variables" : ["PN01251PM", "PN01259PM", "PN01262PM", "PN01263PM", "PN01264PM", "PN01265PM", "PN01266PM", "PN01267PM", "PN01268PM"],
            "dataset_name": [
                "Índice del tipo de cambio real (base 2009=100)", 
                "Tipo de cambio real bilateral del Perú respecto a países latinoamericanos (promedio del período)"
                           ]
                },      
            178 : {
            "variables" : ["PN01448BM", "PN01449BM", "PN01450BM", "PN01451BM", "PN01452BM", "PN01453BM", "PN01454BM", "PN01455BM", "PN01456BM", "PN01457BM"],
            "dataset_name": [
                "Balanza comercial - valores FOB (millones US$)",                 
                           ]
                }, 
            179 : {
            "variables" : ["PN01472BM", "PN01473BM", "PN01474BM", "PN01475BM", "PN01476BM", "PN01477BM", "PN01478BM", "PN01479BM", "PN01480BM", "PN01481BM", "PN01482BM", "PN01483BM", "PN01484BM", "PN01485BM", "PN01486BM", "PN01487BM", "PN01488BM" ],
            "dataset_name": [
                    "Exportaciones por grupo de productos - valores FOB (millones US$)",                 
                           ]
                }, 

            180 : {
            "variables" : ["PN01497BM", "PN01498BM", "PN01499BM", "PN01500BM", "PN01501BM", "PN01502BM", "PN01503BM", "PN01504BM", "PN01505BM", "PN01506BM", "PN01507BM", "PN01508BM", "PN01509BM", "PN01510BM", "PN01511BM", "PN01512BM", "PN01513BM", "PN01514BM", "PN01515BM", "PN01516BM", "PN01517BM", "PN01518BM", "PN01519BM", "PN01520BM", "PN01521BM", "PN01522BM", "PN01523BM", "PN01524BM", "PN01525BM", "PN01526BM", "PN01527BM", "PN01528BM", "PN01529BM", "PN01530BM", "PN01531BM", "PN01532BM", "PN01533BM", "PN01534BM", "PN01535BM", "PN01536BM", "PN01537BM", "PN01538BM", "PN01539BM", "PN01540BM", "PN01541BM", "PN01542BM", "PN01543BM", "PN01544BM", "PN01545BM", "PN01546BM", "PN01547BM", "PN01548BM", "PN01564BM", "PN01565BM", "PN01566BM", "PN01567BM", "PN01568BM", "PN01569BM", "PN01570BM", "PN01571BM", "PN01572BM", "PN01573BM", "PN01574BM", "PN01575BM", "PN01576BM", "PN01577BM", "PN01578BM", "PN01579BM", "PN01580BM", "PN01581BM", "PN01582BM", "PN01583BM", "PN01584BM", "PN01585BM", "PN01586BM", "PN01587BM", "PN01588BM", "PN01589BM", "PN01590BM", "PN01591BM", "PN01592BM", "PN01593BM", "PN01594BM", "PN01595BM", "PN01596BM", "PN01597BM", "PN01598BM", "PN01599BM", "PN01600BM", "PN01601BM", "PN01602BM", "PN01603BM", "PN01604BM", "PN01605BM", "PN01606BM", "PN01607BM", "PN01608BM", "PN01609BM", "PN01610BM", "PN01611BM", "PN01612BM", "PN01613BM", "PN01614BM", "PN01615BM", "PN01616BM", "PN01617BM", "PN01618BM", "PN01619BM", "PN01620BM", "PN01621BM", "PN01622BM", "PN01623BM", "PN01624BM", ],
                "dataset_name": [
                    "xxxxx",                 
                       ]
                }, 

            181 : {
            "variables" : ["PN01625BM", "PN01626BM", "PN01627BM", "PN01628BM", "PN01629BM", "PN01630BM", "PN01631BM", "PN01632BM", "PN01633BM", "PN01634BM", "PN01635BM", "PN01636BM", "PN01637BM", "PN01638BM", "PN01639BM", "PN01640BM", "PN01641BM", "PN01642BM", "PN01643BM", "PN01644BM", "PN01645BM", "PN01646BM", "PN01647BM", "PN01648BM", "", ],
                "dataset_name": [
                    "Importaciones según uso o destino económico - valores FOB (millones US$)",                 
                       ]
                }, 

            185 : {
            "variables" : ["PD12912AM", 'PD38048AM', "PD38049AM" ],
                "dataset_name": [
                    "Expectativas Macroeconómicas"               
                       ]
                }, 
    
            187 : {
            "variables" : ['PN00001MM','PN00002MM','PN00003MM','PN00004MM','PN00005MM','PN00006MM','PN00007MM','PN00008MM','PN00009MM','PN00010MM','PN00011MM','PN00012MM','PN00013MM','PN00014MM','PN00015MM','PN00016MM','PN00178MM','PN00181MM','PN00184MM','PN00187MM','PN00190MM','PN00193MM','PN00196MM','PN00021MM','PN00023MM','PN00025MM','PN00480MM','PN00483MM','PN00486MM','PN00489MM','PN00492MM','PN00494MM','PN00495MM'],
                "dataset_name": [
                    "Cuentas monetarias de las sociedades creadoras de depósito", 
                    "Liquidez de las sociedades creadoras de depósito (fin de periodo)", 
                    "Emisión primaria y multiplicador (millones S/)"                 
                       ]
                }, 
            188 : {
            "variables" : ['PN00496MM','PN00499MM','PN00502MM','PN00505MM','PN00508MM','PN00511MM','PN00532MM','PN00533MM','PN00534MM','PN00535MM','PN00536MM','PN00537MM','PN00538MM','PN00539MM','PN00540MM','PN00541MM','PN00542MM','PN00543MM','PN00544MM','PN00545MM','PN00546MM','PN00547MM','PN00548MM','PN00549MM','PN00550MM','PN00551MM'],
                "dataset_name": [
                    "Crédito de las sociedades creadoras de depósito al sector privado (fin de periodo)", 
                    "Crédito al sector privado de las sociedades creadoras de depósito, por tipo de crédito", 
                    "Crédito al sector privado de las sociedades creadoras de depósito, por tipo de crédito y por monedas"                 
                       ]
                }, 
    
            189 : {
            "variables" : ['PN00264MM','PN00265MM','PN00266MM','PN00267MM','PN00268MM','PN00269MM','PN00270MM','PN00271MM','PN00272MM','PN00273MM','PN00274MM','PN00275MM','PN00276MM','PN00277MM','PN00278MM','PN00279MM','PN00280MM','PN00281MM','PN00282MM','PN00283MM','PN00284MM','PN00285MM','PN00286MM','PN00287MM','PN00288MM','PN00289MM','PN00290MM','PN00291MM','PN00292MM','PN00293MM','PN00294MM','PN00295MM','PN00296MM','PN00297MM','PN00298MM','PN00299MM','PN00300MM','PN00301MM','PN00302MM','PN00303MM','PN00304MM','PN00305MM','PN00306MM','PN00307MM','PN00308MM','PN00309MM','PN00310MM','PN00311MM','PN00312MM','PN00313MM','PN00314MM','PN00315MM','PN00316MM','PN00317MM','PN00318MM','PN00319MM','PN00320MM','PN00321MM','PN00322MM','PN00323MM','PN00324MM','PN00325MM','PN00326MM','PN00327MM','PN00328MM','PN00329MM','PN00330MM','PN00331MM','PN00332MM','PN00333MM','PN00334MM','PN00335MM','PN00336MM','PN00337MM','PN00338MM','PN00339MM','PN00340MM','PN00341MM','PN00342MM','PN00343MM','PN00344MM','PN00345MM','PN00346MM','PN00347MM','PN00348MM','PN00349MM','PN00350MM','PN00351MM','PN00352MM','PN00353MM','PN00354MM','PN00355MM','PN00356MM','PN00357MM','PN00358MM','PN00359MM','PN00360MM','PN00361MM','PN00362MM','PN00363MM','PN00364MM','PN00365MM','PN00366MM','PN00367MM','PN00368MM','PN00369MM','PN00370MM','PN00371MM'],
                "dataset_name": [
                    "Saldo de obligaciones domésticas de las sociedades creadoras de depósito en MN por institución", 
                    "Saldo de obligaciones domésticas de las sociedades creadoras de depósito en MN por institución", 
                    " (millones S/)"
                        ]
                }, 
    
            190 : {
            "variables" : ['PN00863MM','PN00864MM','PN00865MM','PN00866MM','PN00867MM','PN00868MM','PN00869MM','PN00870MM','PN00871MM','PN00872MM','PN00873MM','PN00874MM','PN00875MM','PN00876MM','PN00877MM','PN00878MM','PN00879MM','PN00880MM','PN00881MM','PN00882MM','PN00883MM','PN00884MM','PN00885MM','PN00886MM','PN00887MM','PN00888MM','PN00889MM','PN00890MM','PN00891MM','PN00892MM','PN00893MM','PN00894MM','PN00895MM','PN00896MM','PN00897MM','PN00898MM','PN00899MM','PN00900MM','PN00901MM','PN00902MM','PN00903MM','PN00904MM','PN00905MM','PN00906MM','PN00907MM','PN00908MM','PN00909MM','PN00910MM','PN00911MM','PN00912MM','PN00913MM','PN00914MM','PN00915MM','PN00916MM','PN00917MM','PN00918MM','PN00919MM','PN00920MM','PN00921MM','PN00922MM','PN00923MM','PN00924MM','PN00925MM','PN00926MM','PN00927MM','PN00928MM','PN00929MM','PN00930MM','PN00931MM','PN00932MM','PN00933MM','PN00934MM','PN00935MM','PN00936MM','PN00937MM','PN00938MM','PN00939MM','PN00940MM','PN00941MM','PN00942MM','PN00943MM','PN00944MM','PN00945MM','PN00946MM','PN00947MM','PN00948MM','PN00949MM','PN00950MM','PN00951MM','PN00952MM','PN00953MM','PN00954MM','PN00955MM','PN00956MM','PN00957MM','PN00958MM','PN00959MM','PN00960MM','PN00961MM','PN00962MM','PN00963MM','PN00964MM','PN00965MM','PN00966MM','PN00967MM','PN00968MM','PN00969MM','PN00970MM','PN00971MM','PN00972MM','PN00973MM','PN00974MM','PN00975MM','PN00976MM','PN00977MM','PN00978MM','PN00979MM','PN00980MM','PN00981MM','PN00982MM','PN00983MM','PN00984MM','PN00985MM','PN00986MM','PN00987MM','PN00988MM','PN00989MM'],
                "dataset_name": [
                    "Obligaciones de las sociedades creadoras de depósito con el sector público", 
                    "Crédito neto al sector público de las sociedades creadoras de depósito"
                       ]
                }, 
            200 : {
            "variables" : ['PN07801NM','PN07802NM','PN07803NM','PN07804NM','PN07805NM','PN07806NM','PN07807NM','PN07808NM','PN07809NM','PN07810NM','PN07811NM','PN07812NM','PN07813NM','PN07814NM','PN07815NM','PN07816NM','PN07817NM','PN07818NM','PN07819NM', 'PN07821NM','PN07822NM','PN07823NM','PN07824NM','PN07825NM','PN07826NM','PN07827NM','PN07828NM','PN07829NM','PN07830NM','PN07831NM','PN07832NM','PN07833NM','PN07834NM','PN07835NM','PN07836NM','PN07837NM','PN07838NM','PN07839NM'],
                "dataset_name": [
                    "Tasas de interés activas y pasivas promedio de las empresas bancarias en", 
                    "(términos efectivos anuales)"
                       ]
                },

            342 : {
            "variables" : ["PD38041AM", "PD38042AM", "PD38043AM", "PD38044AM", "PD38045AM", "PD38046AM", "PD38047AM", ],
                "dataset_name": [
                    "Expectativas Empresariales", 
                       ]
                },    

            352 : {
            "variables" : ["PN02312FM", "PN02313FM", "PN02314FM", "PN02315FM", "PN02316FM", "PN02317FM", "PN02318FM", "PN02319FM", "PN02320FM", "PN02321FM", "PN02322FM", "PN02323FM", "PN02324FM", "PN02325FM", "PN02326FM", "PN02327FM", ],
                "dataset_name": [
                    "Ingresos corrientes del gobierno central (millones S/)", 
                       ]
                },    
            353 : {
            "variables" : ["PN02221FM", "PN02222FM", "PN02223FM", "PN02224FM", "PN02225FM", "PN02226FM", "PN02227FM", "PN02228FM", "PN02229FM", "PN02230FM", "PN02231FM", "PN02232FM", "PN02233FM", ],
                "dataset_name": [
                    "Gastos del gobierno central (millones S/)", 
                       ]
                },        

            354 : {
            "variables" : ["PN02390FM", "PN02391FM", "PN02392FM", "PN02393FM", "PN02394FM", "PN02395FM", "PN09808FM", "PN02396FM", "PN02397FM", "PN02398FM", "PN02399FM", "PN02400FM", "PN02401FM", "PN02402FM", "PN02403FM", "PN02404FM", "PN02405FM", "PN02406FM", "PN02407FM", "PN02408FM", "PN02409FM", "PN02410FM", "PN02411FM", "PN02412FM", "PN38072FM", ],
                "dataset_name": [
                    "Gastos no financieros del gobierno general (millones S/)", 
                       ]
                },        
            355 : {
            "variables" : ["PN02294FM", "PN02295FM", "PN02296FM", "PN02297FM", "PN02298FM", "PN02299FM", "PN02300FM", "PN02301FM", "PN02302FM", "PN02303FM", "PN02304FM", "PN02305FM", "PN02306FM", "PN02307FM", "PN02308FM", "PN02309FM", "PN02310FM", "PN02311FM", "PN37894FM", "PN37895FM", "PN37896FM", "PN37897FM", "PN37898FM", "PN37899FM", "PN37900FM", ],
                "dataset_name": [
                    "Ingresos corrientes del gobierno general (millones S/)", 
                       ]
                },        
            }


for dataset in variables:
#for dataset in [352, 353, 354, 355]:
    url = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{}/csv/".format("-".join(variables[dataset]["variables"]))
    print(url)
    print(variables[dataset]["dataset_name"])
    r = requests.get(url, allow_redirects=False)
    s_buf = io.StringIO(str(r.content).replace("<br>", "|"))

    df = pd.read_csv(s_buf, lineterminator="|", encoding = "latin-1")
    for column in df.columns:
        df[column] = df[column].replace("n.d.", np.nan)
        for dataset_name in variables[dataset]["dataset_name"]:                        
            df = df.rename(columns={
                            column: html.unescape(column)
                                   })            
            column = html.unescape(column)
            df = df.rename(columns={
                        column: column.replace(dataset_name + " - ", "")
                         })
            
    
    df = fix_date(df)
    df = df[df["Date"].notnull()]
    df["country"] = "Peru"
    df = df.set_index("Date")

    alphacast.datasets.dataset(dataset).upload_data_from_df(df, 
        deleteMissingFromDB = False, onConflictUpdateDB = True, uploadIndex=True)



# In[ ]:




