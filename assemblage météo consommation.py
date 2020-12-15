conso=pd.read_csv("https://raw.githubusercontent.com/yvan-belakebi/prediction-conso/contrib-yvan-bis/consommation_finale")
consolight=conso[['Périmètre','Date','Heures','Consommation']]
consolight['datebis']=consolight['Date'].copy()
consolight['datebis']=consolight['datebis'].apply(transfo)
consolight['datebis']=consolight['datebis'].str[4:8]+consolight['datebis'].str[2:4]+consolight['datebis'].str[0:2]
consolight['heurebis']=consolight['Heures'].copy()
consolight['heurebis']=consolight['heurebis'].apply(transfo)
consolight['heureter']=consolight['heurebis']+'00'

consolightbis=consolight.copy()
consolightbis['date']=consolightbis['datebis']+consolight['heurebis']

station_pop['date']=station_pop['date'].str[0:12]

A=station_pop.copy()
B=consolightbis.copy()
C=A.groupby('date').apply(lambda x: np.average(x['cdd'], weights = x['weight']))
H=A.groupby('date').apply(lambda x: np.average(x['hdd'], weights = x['weight']))
L=list(A['date'].drop_duplicates())

Tfrance=pd.DataFrame({'date':L, 'cdd_pond':C,'hdd_pond':H})
Tfrance=Tfrance.reset_index(drop=True)

base_totale=pd.merge(Tfrance,B)
base_synthé=base_totale[['date','cdd_pond','hdd_pond','Consommation']]

base_synthé.to_csv("C:/Users/ADMIN/Documents/projet python 2A/base_synthé")

base_synthé.plot(x='date',y='cdd_pond')