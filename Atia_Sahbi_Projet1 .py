#!/usr/bin/env python
# coding: utf-8

# In[135]:


#importer les librairies
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 


# In[136]:


cd "C:\Users\narje\Desktop\données_P4\DAN-P4-FAO"


# # 1) La proportion de personnes en état de sous-nutrition pour l'année 2017 :

# In[137]:


sous_nutrition = pd.read_csv("sous_nutrition.csv") #importer le fichier sous_nutrition
population = pd.read_csv("population.csv",sep=';',index_col = ['Année']) #téléchargement du fichier population depuis les données de FAO
sous_nutrition['Valeur'] = sous_nutrition['Valeur'].replace(['<0.1'],0) #remplacement des valeurs considéderées négligeable par 0
sous_nutrition['Année'] = sous_nutrition['Année'].replace(['2016-2018'],2017) #le nombre de personnes correspond à la moyenne sur ces 3 années
sous_nutrition.set_index(sous_nutrition['Année'],inplace = True) #indexation de la dataframe sous-nutrition par Année
sous_nutrition.Valeur = pd.to_numeric(sous_nutrition.Valeur) #convertir les Valeurs de sous-nutrition de objet à numérique 
sum1 = sous_nutrition.loc[2017]['Valeur'].sum() #somme de personne en état de sous-nutrition en 2017
sum2 = population.loc[2017,'Valeur'].sum() #somme de population mondiale en 2017
print("Le nombre de personnes en état de sous-nutrition pour l'année 2017 est de",sum1,'millions')
print('-'*80)
print("La proportion de personnes en état de sous-nutrition pour l'année 2017 est de",((sum1 * 1000 / sum2) * 100).round(2),'%')


# # 2) Le nombre théorique de personnes qui pourraient être nourries:

# In[138]:


dispo_alimentaire = pd.read_csv("dispo_alimentaire.csv",sep=',') #importer le fichier dispo_alimentaire 
S = dispo_alimentaire.loc[:,['Zone','Disponibilité alimentaire (Kcal/personne/jour)']] #dataframe S contient les colonnes Zone et Disponibilité alimentaire (Kcal/personne/jour)
S.rename(columns = {'Disponibilité alimentaire (Kcal/personne/jour)':'disponibilité'},inplace = True) #changement du nom de colonne 
A = S.groupby(['Zone']).sum() #somme de disponibilité alimentaire par zone
population_2017 = pd.read_csv("population_2017.csv",encoding = 'ANSI',sep=';') #importer le fichier population depuis le site de FAO
H = pd.merge(A,population_2017,on = 'Zone') #jointure entre le dataframe population et celle de la disponibilité
J = ( H['disponibilité'] * H['Valeur'] ).sum() #disponilité alimentaire en (Kcal/jour) de chaque zone
print("Le nombre théorique de personnes qui pourraient être nourries est de",(J / 2500).round(1),"milles") #2500Kcal/personne/jour:le MDER
print('-'*70)
print('La proportion de personnes qui pourraient être nourries est de',(J * 100 / 2500 / sum2).round(2),'%')


# # 3) La disponibilité alimentaire des produits végétaux :

# In[139]:


dispo_alimentaire = pd.read_csv("dispo_alimentaire.csv",sep = ',') #téléchargement du fichier dispo_alimentaire depuis les données de FAO
G = population_2017.loc[:,['Zone','Valeur']] #dataframe ne contient que les zones et la population de chaque pays
P = dispo_alimentaire[dispo_alimentaire['Origine'] == 'vegetale'] #filtre pour la disponibilité alimentaire d'origine végetale
G.rename(columns={'Valeur':'Population'},inplace = True) #chnagement de nom de colonne de valeur à Population
N = pd.merge(P,G,left_on='Zone',right_on='Zone') #jointure entre la dataframe P et G
B = (N['Population'] * N['Disponibilité alimentaire (Kcal/personne/jour)']).sum() #disponilité alimentaire des produits végétaux en (Kcal/jour/personne) de chaque zone
print('La proportion de disponibilité alimentaire des produits végétaux est de ',(B * 100 / 2500 / sum2).round(2),'%')


# # 4-a) Utilisation de la disponibilité intérieure,la part qui est attribuée à l’alimentation animale :

# In[140]:


A = dispo_alimentaire.groupby(['Zone'])['Aliments pour animaux'].sum()#somme des Aliments pour animaux pour chaque zone
B = dispo_alimentaire.groupby(['Zone'])['Disponibilité intérieure'].sum()#somme de Disponibilité intérieure pour chaque zone
C = pd.merge(A,B,left_on='Zone',right_on='Zone')#jointure de deux dataframe A et B par zone
D = ((C['Aliments pour animaux'].sum() / C['Disponibilité intérieure'].sum()) * 100).round(2)#proportion des Aliments pour animaux par rapport à la Disponibilité intérieure
print('La part qui est attribuée à l’alimentation animale est de ',D,'% de la disponibilité intérieur')


# # 4-b) Utilisation de la disponibilité intérieure,la part qui est perdu :

# In[141]:


A = dispo_alimentaire.groupby(['Zone'])['Pertes'].sum()#somme des pertes alimentaire pour chaque zone
B = dispo_alimentaire.groupby(['Zone'])['Disponibilité intérieure'].sum()#somme de Disponibilité intérieure pour chaque zone
C = pd.merge(A,B,left_on='Zone',right_on='Zone')#jointure entre la dataframe A et B par zone
D = ((C['Pertes'].sum() / C['Disponibilité intérieure'].sum()) * 100).round(2)#proportion des pertes des aliments par rapport à la Disponibilité intérieure
print('La part perdu est de ',D,'% de la disponibilité intérieur')


# # 4-c) Utilisation de la disponibilité intérieure, la part qui est concrètement utilisée pour l'alimentation humaine :

# In[142]:


Prodction = dispo_alimentaire['Production'].sum()#somme de production alimentaire mondiale
Importation = dispo_alimentaire['Importations - Quantité'].sum()#somme des importations alimentaire mondiale
Exportations = dispo_alimentaire['Exportations - Quantité'].sum()#somme des expotations alimentaire mondiale
Variation_stock = dispo_alimentaire['Variation de stock'].sum()#somme de Variation de stock mondiale
Aliments_animaux = dispo_alimentaire['Aliments pour animaux'].sum()#somme des Aliments pour animaux mondiale
Semences = dispo_alimentaire['Semences'].sum()#somme des semences mondiale
Traitement= dispo_alimentaire['Traitement'].sum()#somme des traitements des aliments mondiale
Autres_Utilisations = dispo_alimentaire['Autres Utilisations'].sum()#somme des autres utilistations
Pertes = dispo_alimentaire['Pertes'].sum()#somme des pertes alimentaires mondiales
Disponibilité_alimentation_humaine = Prodction + Importation - Exportations + Variation_stock - Aliments_animaux - Semences - Traitement - Autres_Utilisations - Pertes
print("La part qui est concrètement utilisée pour l'alimentation humaine est de",Disponibilité_alimentation_humaine,"milles tonnes")
Total_dispo_alimentaire = C['Disponibilité intérieure'].sum()
P = ((Disponibilité_alimentation_humaine / Total_dispo_alimentaire) * 100).round(2)#proportion de disponibilité alimentaire pour humain par rapport à la disonibilité totale
print('-'*70)
print("La proportion de l'alimentation humaine est de ",P,"% de la diponibilité intérieure")


# # 5) Les pays pour lesquels la proportion de personnes sous-alimentées est la plus forte en 2017:

# In[143]:


sous_nutrition_2017 = (sous_nutrition.loc[2017,['Zone','Valeur']]) #la sous-nutrition mondiale en 2017
population_2017 = population.loc[2017,['Zone','Valeur']] #la population mondiale en 2017
population_2017.rename(columns = {'Valeur':'Population'} , inplace = True) #changement de nom de colonne
C = pd.merge(sous_nutrition_2017,population_2017,left_on = 'Zone',right_on = 'Zone') #jointure entre les deux dataframe en zone
C.set_index('Zone',inplace=True) #reindexation la dataframe C par zone
D = ((C['Valeur'] / (C['Population'] / 1000)) * 100).round(2) #proportion de sous-nutrition
E = D.sort_values(ascending = False) #tri par proportion de sous-nutrition des zones
E = pd.DataFrame(data = E) #convertir E en dataframe
E.reset_index(inplace = True) #revenir à l'indexation par défaut
E.rename(columns = {0:'Proportion en %'} , inplace = True) #donner le nom 'Proportion en %' au premier colonne
E.index = np.arange(1,len(E) + 1) #commencer l'indexation par 1 au lieu de 0
print('Les 20 premiers dont la proportion de personnes sous-alimentées est la plus forte en 2017 sont:\n')
E.head(20)


# In[113]:


E.head(20).plot(kind = 'barh', x = 'Zone',figsize = (10,6)) #figure de la proportion de personnes sous-alimentées par zone pour les 2  prémiers pays
plt.title('Proportion de personnes sous-alimentées par zone') #titre de la figure
plt.ylabel('Zone') #axe des ordonnées
plt.xlabel('Proportion de sous-nutrition en %') #axe des abscisses
plt.savefig('Proportion de personnes sous-alimentées par zone(20 pays).png' , dpi = 200,bbox_inches = 'tight') #enregistrement de figure dans le répertoire de travail et augmentation de la résolution


# In[144]:


E.hist(bins = 20,figsize = (10,6)) #histogramme de proportion de sous-nutrition par zone
plt.title('Proportion de personnes sous-alimentées par zone')#titre de la figure
plt.xlabel('Proportion en %')
plt.ylabel('Nombre de pays')
plt.savefig('proportion de personnes sous-alimentées par zone.png' , dpi = 200,bbox_inches = 'tight') #enregistrement de figure dans le répertoire de travail et augmentation de la résolution


# In[333]:


E.describe() #statistiques de sous-nutrition mondiale par zone


# # 6) La liste de pays qui ont le plus bénéficié d’aide depuis 2013:

# In[145]:


aide_alimentaire = pd.read_csv("aide_alimentaire.csv") #télechargement de fichier aide alimentaire
A = aide_alimentaire.groupby(['Pays bénéficiaire'])['Valeur'].sum() #somme des valeurs d'aide par zone
B = A.sort_values(ascending = False) #tri par valeur de l'aide
B = pd.DataFrame(data = B) #convertir B en dataframe
B.reset_index(inplace=True) #reindexation de B 
B.index = np.arange(1,len(B) + 1) #commencer l'indexation par 1
B.rename(columns={'Valeur':"Valeur de l'aide (en tonne)"} , inplace = True) #changement du nom de colonne
print("Les 20 premiers pays qui ont le plus bénéficié d’aide depuis 2013:")
B.head(20)


# In[116]:


B.head(20).plot(kind = 'barh', x = 'Pays bénéficiaire',figsize=(10,6))
plt.title('Liste de 20 premiers pays qui ont le plus bénéficié d’aide depuis 2013') #titre de la graphique
plt.xlabel("Valeur de l'aide (en million de tonne)") #axe des abscisses
plt.ylabel('Pays bénéficiaire') #axe des ordonnées
plt.savefig('Liste de 20 premiers pays qui ont le plus bénéficié d’aide depuis 2013.png' , dpi = 200,bbox_inches = 'tight') #enregistrement de figure dans le répertoire de travail et augmentation de la résolution


# In[117]:


B.hist(bins = 20,figsize=(10,6)) #histogramme de proportion de sous-nutrition par zone
plt.title('répartition de la valeur d’aide par zone depuis 2013') #titre de la figure
plt.xlabel("Valeur de l'aide (en million de tonne)") #axe des abscisses
plt.ylabel('Pays bénéficiaire') #axe des ordonnées
plt.savefig('répartition de la valeur d’aide par zone depuis 2013.png' , dpi = 200,bbox_inches = 'tight') #enregistrement de figure dans le répertoire de travail et augmentation de la résolution


# # 7-a) Liste des pays qui ont plus de disponibilité/habitant (Kcal/personne/jour):

# In[118]:


A = dispo_alimentaire.groupby(['Zone'])['Disponibilité alimentaire (Kcal/personne/jour)'].sum()#somme de disponibilité alimentaire mondiale par zone
A = A.sort_values(ascending = False)#tri des zones par disponibilité alimentaire
A = pd.DataFrame(data = A)#convertir A en dataframe
A.reset_index(inplace=True)#reindexation de A
A.index = np.arange(1,len(A) + 1)#commencer l'indexation de 1 au lieu de 0
print("Liste de 20 premiers pays qui ont plus de disponibilité par habitant")
A.head(20)


# In[146]:


A.head(20).plot(kind = 'barh', x = 'Zone',figsize = (13,6)) #représentation graphique à barres
plt.title('Liste de 20 premiers pays qui ont plus de disponibilité par habitant') #titre de la figure
plt.xlabel("Disponibilité alimentaire (Kcal/personne/jour)") #axe des abscisses
plt.ylabel('Zone') #axe des ordonnées
plt.savefig('Liste de 20 premiers pays qui ont plus de disponibilité par habitant.png' , dpi = 200,bbox_inches = 'tight') #enregistrement de figure dans le répertoire de travail et augmentation de la résolution


# In[120]:


A.hist(bins = 20,figsize=(10,6)) #histogramme de Liste des pays qui ont plus de disponibilité/habitant 
plt.title('répartition de disponibilité alimentaire(Kcal/jour/habitant)') #titre de la figure
plt.xlabel("Disponibilité alimentaire (Kcal/personne/jour)") #axe des abscisses
plt.ylabel('Zone') #axe des ordonnées
plt.savefig('Liste de 20 premiers pays qui ont plus de disponibilité par habitant.png' , dpi = 200,bbox_inches = 'tight') #enregistrement de figure dans le répertoire de travail et augmentation de la résolution


# In[2051]:


A.describe() #statistique de A


# # 7-b) Liste des pays qui ont moins de disponibilité/habitant en (Kcal/personne/jour):

# In[1]:


A = dispo_alimentaire.groupby(['Zone'])['Disponibilité alimentaire (Kcal/personne/jour)'].sum() #somme de disponibilité alimentaire mondiale par zone
A = A.sort_values(ascending = True) #tri des zones par disponibilité alimentaire descendante 
A = pd.DataFrame(data = A) #convertir A en dataframe
A.reset_index(inplace=True) #reindexation de A
A.index = np.arange(1,len(A) + 1) #commencer l'indexation de 1 au lieu de 0
print("Liste de 20 premiers pays qui ont plus de disponibilité par habitant")
A.head(20)


# In[122]:


A.head(20).plot(kind = 'barh', x = 'Zone',figsize=(13,6))
plt.title('Liste de 20 premiers pays qui ont moins de disponibilité par habitant') #titre de la figure
plt.xlabel("Disponibilité alimentaire (Kcal/personne/jour)") #axe des abscisses
plt.ylabel('Zone') #axe des ordonnées
plt.savefig('Liste de 20 premiers pays qui ont moins de disponibilité par habitant.png' , dpi = 200,bbox_inches = 'tight') #enregistrement de figure dans le répertoire de travail et augmentation de la résolution


# # 8) L'utilisation des céréales pour l'alimentation animale en 2017:

# In[147]:


liste_cereales = ["Blé et produits", "Riz et produits", "Orge et produits", "Maïs et produits", "Seigle et produits",
                  "Avoine", "Millet et produits", "Sorgho et produits", "Céréales, Autres"]

cereales = dispo_alimentaire.loc[dispo_alimentaire['Produit'].isin(liste_cereales),:] #Création d'une table n contenant que les informations des céréales
A = cereales['Aliments pour animaux'].sum()
B = cereales['Disponibilité intérieure'].sum()
print("La proportion d'alimentation animale est de ",(A * 100 / B).round(2), "%")
C = cereales['Nourriture'].sum()
print("La proportion d'alimentation humaine est de",(C * 100/ B).round(2), "%")


# # 9)L’utilisation du manioc par la Thaïlande aux égards de la proportion de personnes en sous-nutrition en 2017:

# In[148]:


thai_manioc = dispo_alimentaire.loc[(dispo_alimentaire['Produit'] == "Manioc") & (dispo_alimentaire['Zone'] == "Thaïlande"),:] #filtration sur le produit manioc pour la Thaïlande
A = thai_manioc["Exportations - Quantité"] 
B = thai_manioc["Production"]
C = A/B
C = pd.DataFrame(data = C) #convertir C en dataframe
D = C.loc[13809,0].round(2)
print("la Thaïlande exporte",D * 100,"%","de ce qu'elle produise de manioc")
population_Thaïlande = population_2017[population_2017['Zone'] == 'Thaïlande']
B = sous_nutrition.loc[2017,['Année','Zone','Valeur']] #dataframe se sous-nutrition pour l'année 2017\n",
D = B [ B ['Zone'] == 'Thaïlande'] #filtration sur la sous-nutrition en Thaïlande\n",
V = D['Valeur'].sum()
print('-'*70)
print("Le nombre de personnes en sous-nutrition en Thaïlande en 2017 est de",V,"millions")

