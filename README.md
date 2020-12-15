# prediction-conso

## récupération et mise en qualité de données météorologiques



import pandas as pd
import numpy as np
import bs4
import urllib

###importation d'une base contenant les dates, identifiants de station et données météo de la station (source météo-France)###

Gbase=pd.read_csv("https://raw.githubusercontent.com/yvan-belakebi/prediction-conso/contrib-yvan/historique%20m%C3%A9t%C3%A9o%20exploitable")
Gbase=Gbase.reset_index(drop=True)



basemod=Gbase.copy()
basemod=basemod.replace("mq",nan)
basemod=basemod.replace("t", nan)
basemod=basemod.dropna()
basemod["t"]=basemod["t"].astype(float)
basemod["date"]=basemod["date"].astype(str)
basemod["numer_sta"]=basemod["numer_sta"].astype(int)
basemod=basemod.rename(columns={'numer_sta':'ID'})

basemod=pd.merge(basemod,stations,on=['ID'])

#basemod.to_csv("C:/Users/ADMIN/Documents/projet python 2A/météo et stations")

###importation des informations sur les stations (disponibles sur le site météo-France)###

stations=pd.read_csv("https://raw.githubusercontent.com/yvan-belakebi/prediction-conso/contrib-yvan/stations.txt", sep=";")

###webscrapping de la population des différents départements, dans l'optique de pondérer les poids des stations###

from urllib import request

url_popdep="https://fr.wikipedia.org/wiki/Liste_des_d%C3%A9partements_fran%C3%A7ais_class%C3%A9s_par_population_et_superficie"

request_text=request.urlopen(url_popdep).read()
page = bs4.BeautifulSoup(request_text, "lxml")
tableau_dep=page.find('table',{"class":"wikitable sortable alternance"})
table_body=tableau_dep.find('tbody')
rows=table_body.find_all('tr')

dico_dep = dict()
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols[1:]]
    if len(cols) > 0 :
        dico_dep[cols[0]] = cols[0:]

data_dep = pd.DataFrame.from_dict(dico_dep,orient='index')
#data_dep.to_csv("C:/Users/ADMIN/Documents/projet python 2A/data_dep")


for row in rows:
    cols = row.find_all('th')
    if len(cols) > 0 :
        cols = [ele.get_text(separator=' ').strip().title() for ele in cols]
        columns_dep = cols

import re

columns_années = [re.sub('\[ (\d+) \] ?', '', nom_col) for nom_col in columns_dep]
columns_dep=['Code','Département']+columns_années+['superficie','densité']

data_dep.columns = columns_dep[0:]
popdep=data_dep[['Code','Département','2017 ']]


def transfo(s):
    return re.sub("\D","",s)

#après localisation des stations dans leur département via geopandas, on obtient la base station_finale

station_dep=pd.read_csv("https://raw.githubusercontent.com/yvan-belakebi/prediction-conso/contrib-yvan/station_finale")
station_dep=pd.merge(basemod,station_dep)
popdep=popdep.rename(columns={'Code':'code_departement'})
popdep=popdep.astype({'2017 ':'str'}, errors='ignore')
popdep['2017 ']=popdep['2017 '].apply(transfo)
popdep['test']=popdep['2017 '].str.isdigit()
popdep=popdep.query('test')

popdep=popdep.astype({'2017 ':'int'})

popdep['weight']=popdep['2017 ']/popdep['2017 '].sum()

station_pop=pd.merge(station_dep,popdep, on='code_departement')
station_pop['code_departement']=station_pop['code_departement'].replace("2A","2")
station_pop['code_departement']=station_pop['code_departement'].replace("2B","2")
station_pop=station_pop.astype({"code_departement":'int'})


tbasse=289.15  #16°C, température à partir de laquelle on chauffe
thaute=301.15  #28°C, température à partir de laquelle on climatise

station_pop['hdd']=np.maximum(0, tbasse-station_pop['t'])
station_pop['hdd']=np.maximum(0, station_pop['t']-thaute)
