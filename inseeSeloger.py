# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 08:32:55 2014

@author: Paco
"""

import xml.etree.ElementTree as xml
import urllib2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def xstr(s):
    if s is None:
      return ''
    else:
      return s.text  

def crawlSeLoger(localisation='350238',typedebien='1',page='1',prixMin='200',prixMax='2000',tri='a_px'):
    
    apiUrl = "http://ws.seloger.com/search.xml?" 
    url = apiUrl+"ci="+localisation+"&SEARCHpg="+page+"&pxmin="+prixMin+"&pxmax="+prixMax+"&idtt=1&idtypebien="+typedebien+"&tri="+tri
    tree = xml.ElementTree(file=urllib2.urlopen(url))
    root = tree.getroot()
    
    df = pd.DataFrame(columns=('idannonce','idagence','typeBien','creationDate',
    'titre','libelle','description','prix','nbPieces','surface','pays','codePostal',
    'codeInsee','ville','lien','latitude','longitude','neuf','nbSallesDeBain','nbSallesEau','nbParkings'))
    i=0
    
    for annonces in root.findall('annonces'):
        for annonce in annonces.findall('annonce'):
            idannonce = xstr(annonce.find('idAnnonce'))
            idagence = xstr(annonce.find('idAgence'))
            typeBien = xstr(annonce.find('idTypeBien'))
            creationDate = xstr(annonce.find('dtCreation'))
            titre = xstr(annonce.find('titre'))
            libelle = xstr(annonce.find('libelle'))
            description = xstr(annonce.find('descriptif'))
            prix = xstr(annonce.find('prix'))
            nbPieces = xstr(annonce.find('nbPiece'))
            surface = xstr(annonce.find('surface'))
            pays = xstr(annonce.find('pays'))
            codePostal = xstr(annonce.find('cp'))
            codeInsee = xstr(annonce.find('codeInsee'))
            ville = xstr(annonce.find('ville'))
            lien = xstr(annonce.find('permaLien'))
            latitude = xstr(annonce.find('latitude'))
            longitude = xstr(annonce.find('longitude'))
            neuf = xstr(annonce.find('siLotNeuf'))
            nbSallesDeBain = xstr(annonce.find('nbsallesdebain'))
            nbSallesEau = xstr(annonce.find('nbsalleseau'))
            nbParkings = xstr(annonce.find('nbparkings'))
            
            d = np.array([idannonce,idagence,typeBien,creationDate,titre,
            libelle,description,prix,nbPieces,surface,pays,codePostal,
            codeInsee,ville,lien,latitude,longitude,neuf,nbSallesDeBain,
            nbSallesEau,nbParkings])
            
            df.loc[i] = d
            i = i+1
    df = df.fillna(0)        
    df = df.replace(to_replace='', value='0')
    return df        

def infoLocationVille(appart):
    ville = appart[['ville']][:1][[0]]
    df = appart[['prix']]
    df_2 = appart[['nbPieces']]
    df_3 = appart[['surface']]
    converted = df.apply(lambda f : float(f[0]) , axis = 1)  
    converted2 = df_2.apply(lambda f : float(f[0]) , axis = 1)
    converted3 = df_3.apply(lambda f : float(f[0]) , axis = 1)
    truc = converted.mean(axis=1)
    truc2 = converted2.mean(axis=1)
    truc3 = converted3.mean(axis=1)
    dd = np.array([ville,truc,truc2,truc3])
    df_ville = pd.DataFrame(columns=['ville','prix_moy','nb_pieces_moy','surface_moy'])
    df_ville.loc[0] = dd
    return df_ville

## Paris, Lyon, Toulouse, Genoble, Bordeaux, Lille, Nantes, AixenProvence, Rennes, Strasbourg
#appart_paris = crawlSeLoger(localisation='750056')
#appart_lyon = crawlSeLoger(localisation='690123')
#appart_toulouse = crawlSeLoger(localisation='310555')
#appart_grenoble = crawlSeLoger(localisation='380185')
#appart_bordeaux = crawlSeLoger(localisation='330063')
#appart_lille = crawlSeLoger(localisation='590350')
#appart_nantes = crawlSeLoger(localisation='440109')
#appart_aix = crawlSeLoger(localisation='130001')
#appart_rennes = crawlSeLoger(localisation='350238')
#appart_strasbourg = crawlSeLoger(localisation='670482')
#appart_montpellier = crawlSeLoger(localisation='340172')
#appart_villeurbanne = crawlSeLoger(localisation='690266')


## Average 
#apparts = [appart_paris,appart_lyon,appart_toulouse,appart_grenoble,
#appart_bordeaux,appart_lille,appart_nantes,appart_aix,appart_rennes,appart_strasbourg,appart_montpellier,appart_villeurbanne]
#cadre_moy = pd.DataFrame()
#for ap in apparts:
#    cadre_moy = cadre_moy.append(infoLocationVille(ap))

# Graph price vs surface 
x = np.array(cadre_moy.prix_moy)
y = np.array(cadre_moy.surface_moy) 
z = np.array(cadre_moy.nb_pieces_moy)
n = ['Paris','Lyon','Toulouse','Grenoble','Bord','Lille','Nantes','Aix','Ren','Stra','Montp','Villeur']

fig, ax = plt.subplots()
ax.scatter(x, y)

for i,txt in enumerate(n):
    ax.annotate(txt, (x[i],y[i]))
 
# Graph price vs surface    
fig2, ax2 = plt.subplots()
ax2.scatter(x, z)

for i,txt in enumerate(n):
    ax2.annotate(txt, (x[i],z[i]))
   


