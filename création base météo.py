import pandas as pd
import numpy as np
import geopandas as gp
from math import *
toutesbases={'bases': [pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201801.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201802.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201803.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201804.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201805.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201806.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201807.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201808.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201809.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201810.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201811.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201812.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201901.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201902.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201903.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201904.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201905.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201906.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201907.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201908.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201909.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201910.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201911.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201912.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.202001.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.202002.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.202003.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.202004.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.202005.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.202006.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.202007.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.202008.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.202009.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.202010.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.202011.txt", sep=";"),pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.202012.txt", sep=";")]}

base1=pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.2020121221.txt", sep=";")
base2=pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/synop.201801.txt", sep=";")


for i in range(35):
    toutesbases['bases'][i]=toutesbases['bases'][i][['numer_sta','date','t']]

def baseglob():
    basetot=toutesbases['bases'][0]
    for i in range(1,35):
        basetot=pd.concat([basetot,toutesbases['bases'][i]])
    return basetot


Gbase=baseglob()
Gbase=Gbase.reset_index(drop=True)



# pour pouvoir relier à la base contenant la consommation, il faut faire une "température française". Pour cela on moyenne la température par département et on webscrappe la population de ce département. On fait ensuite une moyenne pondérée des températures par la population

basemod=Gbase.copy()
basemod=basemod.replace("mq",nan)
basemod=basemod.replace("t", nan)
basemod=basemod.dropna()
basemod["t"]=basemod["t"].astype(float)
basemod["date"]=basemod["date"].astype(str)
basemod["numer_sta"]=basemod["numer_sta"].astype(int)



basemod.to_csv("C:/Users/ADMIN/Documents/projet python 2A/historique météo exploitable")

#def transformernom(chaine):
#    if len(chaine)<5:
#        chaine=str(0)+chaine
#    return chaine

stations=pd.read_csv("C:/Users/ADMIN/Documents/projet python 2A/stations.txt", sep=";")


A=basemod.groupby('date').mean('t')











