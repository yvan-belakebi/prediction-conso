# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 18:39:28 2020

@author: nicol
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import xlrd 
import geopandas as gdp
import shapely
from shapely.geometry import Point
"""
path = 'C:/Users/nicol/OneDrive/Bureau/Cours ENSAE 2A/Python pour le DS/projet python/data_cons_2018/cons_2018.csv'
path2 = 'C:/Users/nicol/OneDrive/Bureau/Cours ENSAE 2A/Python pour le DS/projet python/data_cons_2018/cons_2018.xls'
cons = pd.read_csv(path,keep_default_na=(False))
cons = cons[['Date','Heures','Consommation']]
# On supprime les lignes avec des valeurs manquantes
cons = cons[cons['Consommation']!='']
cons['Consommation'] = cons['Consommation'].astype(float)

# Première idée : on veut faire une graphique de la consommation moyenne heure 
# par heure pour se faire une idée de la variation de la consommation pendant
# une même journée.

cons_heure = cons.groupby('Heures')['Consommation'].mean()
plt.title("Consommation moyenne lors d'une journée")
plt.ylabel('Consommation en MWh')
cons_heure.plot()
plt.close()


# Maintenant on veut avoir la variation de la consommation à travers les mois. 
# Création de la variable mois 
cons['Mois'] = cons['Date'].str[5:7]
cons_mois = cons.groupby('Mois')['Consommation'].mean()
plt.title("Consommation moyenne mensuelle")
plt.ylabel('Consommation en MWh')
cons_mois.plot()

# On importe la base de données contenant l'historique 
url_historique = 'C:/Users/nicol/OneDrive/Bureau/Cours ENSAE 2A/Python pour le DS/projet python/historique météo.txt'
historique = pd.read_csv(url_historique)


# On repart sur la base telle qu'elle était au départ 
cons = pd.read_csv(path)
cons = cons.drop(['Nature','Consommation'],axis=1)
cons.dropna(inplace=True)
# On regarde quelles sont les sources d'énergies qui produisent le plus 
# en moyenne
moyenne = cons.mean().sort_values(ascending = True)
#


# Problème : on y voit pas clair dans ce df ! les colonnes ne sont pas bien nommées
# Mes idées sont les suivantes : recherche les énergies qui produisent le plus 
# Donner leur part dans le mix énergétique français. 

"""

# Partie I. Importation et nettoyage des données 

# On commence par importer les données de la base Eco2mix concernant la 
# consommation et la production d'énergie en France. 
path = 'C:/Users/nicol/OneDrive/Bureau/Cours ENSAE 2A/Python pour le DS/projet python/data_cons_2018/cons_2018.csv'
cons_france_2018 = pd.read_csv(path)
cons_france_2018 = cons_france_2018.drop(['Nature'],axis=1)
cons_france_2018.dropna(inplace=True)
# On restreint la base au colonnes sur la production et la consommation. 
cons_france_2018 = cons_france_2018.iloc[:,0:13]
# 3 graphiques : mix énergétique français / consommation par heure / par mois. 

# Mix énergétique français. 
labels = cons_france_2018.columns[7:13].to_list()
somme = cons_france_2018.iloc[:,7:13].sum()
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','darkolivegreen','darksalmon','cadetblue','orange']

plt.pie(somme, labels=labels, colors=colors, 
        autopct='%1.1f%%', shadow=True, startangle=90)

plt.axis('equal')
plt.title('Part des différences énergies dans le mix énergétique français')
plt.show()

# Problème : le graphique n'est pas bien proportionné. 

# Reste à faire : production moyenne horaire et mensuel
# On crée la variable  variable mois 
cons_france_2018['Mois'] =  cons_france_2018['Date'].str[5:7]
cons_heure = cons_france_2018.groupby('Mois')['Consommation'].mean()
cons_heure.plot()

#I.B Ici on va importer de les données concernant les métropoles. L'idée 
# est de voir comment se réparti la production des énergies selon les métropoles
# quelles sont les métropoles championnes des énergies vertes, les métropoles
# qui polluent le plus etc.

regions = ['hauts-de-france','ile-de-france','bretagne',
           'paca','normandie','nouvelle-aquitaine','grand-est']
path_reg = 'C:/Users/nicol/OneDrive/Bureau/Cours ENSAE 2A/Python pour le DS/projet python/data/'
cons_reg = pd.read_csv(path_reg  + 'auvergne-rhône-alpes_2018.csv',encoding='ISO-8859-1',error_bad_lines=False,sep = ';')
for i in regions:
    data = pd.read_csv(path_reg + i + '_2018.csv',encoding='ISO-8859-1',error_bad_lines=False,sep = ';')
    cons_reg = pd.concat([cons_reg,data],join='inner')

# On veut maintenant avoir le classement des régions selon les types d'énergies
# produites. Il faut faire des diagrammes en barre à la manière du TP matplotlib

somme = cons_reg.groupby('Périmètre').sum()
somme.drop(somme.tail(1).index,inplace=True)

rang = somme.rank(axis = 0,ascending=False)
somme.plot.bar()

# Digramme en barre des régions qui consomment le plus
somme['Consommation'].sort_values(ascending = False).plot.barh()
# Régions qui produisent le plus d'éolien ou du solaire
somme['Eolien'].sort_values().plot.barh(color='red')
somme['Solaire'].sort_values().plot.barh(color='red')

# On regarde la part de chaque région dans la consommation totale
explode = [0,0,0,0,0.1,0,0,0]
label_region = somme.index.to_list()
plt.title('Part des différentes régions dans la consommation en France')

plt.pie(somme['Consommation'], labels=label_region, colors=colors[0:8], 
        autopct='%1.1f%%', shadow=True, startangle=90,explode = explode)



# Continuons vers la suite. 

# II. Le modèle de régression linéaire :

# Maintenant, on importe les données de l'historique météo 
path_historique = 'C:/Users/nicol/OneDrive/Bureau/Cours ENSAE 2A/Python pour le DS/projet python/data/historique_meteo_exploitable'
historique = pd.read_csv(path_historique)
# On crée la variable proposez par Yvan, d'abord dans un cas arbitraire.
# On considère qu'on allume le chauffage s'il fait moins de 10 degré et que l'on
# met la clim lorsqu'il fait plus de 30 degrés. 


# On convertis les degrés en Kelvin
historique['t_deg'] = historique['t'] - 273.15
historique['jour']

#


# Par ailleurs, on considérera qu'on ne prend qu'une seule température par jour 
# On crée les variables mois et jour qui servirons d'index

station = pd.read_csv('C:/Users/nicol/OneDrive/Bureau/Cours ENSAE 2A/Python pour le DS/projet python/data/meteo_et_station.txt')

station = gdp.GeoDataFrame(station,geometry = gdp.points_from_xy(station['Longitude'], station['Latitude']))


    
departements  = gdp.read_file("C:/Users/nicol/OneDrive/Bureau/Cours ENSAE 2A/Python pour le DS/projet python/data/contours_dep.geojson")

station_dep = gdp.sjoin(station,departements,how='inner',op = 'intersects')
station_dep=station_dep.drop(['geometry'],axis=1)
station_dep.to_csv('C:/Users/nicol/OneDrive/Bureau/Cours ENSAE 2A/Python pour le DS/projet python/data/station_departement_vf')
# Annexe : associer les données géographiques des stations à leur département
station_dep_simple = station_dep[['ID','code_departement']]
station_dep.to_csv('C:/Users/nicol/OneDrive/Bureau/Cours ENSAE 2A/Python pour le DS/projet python/data/station_dep_simple')

new = station_dep_simple.groupby['ID']

station_final = station_dep_simple.drop_duplicates()
station_final.to_csv('C:/Users/nicol/OneDrive/Bureau/Cours ENSAE 2A/Python pour le DS/projet python/data/station_finale')

# On reprend le modèle de régression avec station_dep
station_dep['année'] = station_dep['date'].astype(str).str[0:4]
station_dep['mois'] = station_dep['date'].astype(str).str[4:6]
station_dep['jour'] = station_dep['date'].astype(str).str[6:8]
station_dep['heure'] = station_dep['date'].astype(str).str[8:10]
a = station_dep.head(300)





