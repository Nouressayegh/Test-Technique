# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 17:16:35 2021

@author: noure
"""
"""Etape 1 : Travail sur une liste d'horaire correspondant au même jour 
et à la même personne (sans chevauchement) :"""


"""Pour pouvoir travailler avec la forme imposée par l'enoncé j'ai défini une première fonction __convert__ pour avoir un tuple d'entier correspondant à (heure, minute)"""
def convert(horaire):
    heure =''
    minute=''
    for i in range(len(horaire)) :
        if horaire[i] ==":":
            break
        heure += horaire[i]
    #on garde que les minutes
    minute= horaire.replace(heure+':','')
    return (int(heure),int(minute))


#calcule la durée entre deux horaires

def duree(horaire1, horaire2):
    
    horaire1=convert(horaire1)
    horaire2=convert(horaire2)
    
    #convertir en minutes
    h1=horaire1[0]*60 +horaire1[1]
    h2=horaire2[0]*60 +horaire2[1]
    duree = h2-h1+1
    return duree


#un premier teste simple 

L=['1','1 08:30-09:45']
debut="8:00"
fin="17:59"
#tester avant et après le premier créneau
if duree(debut,L[1][2:7])>60 :
    print( "Il y a un horaire entre 8:00 et 8:59 ")
elif duree(L[1][8:],fin)>60 :
    print("Il y a un horaire entre 17:00 et 17:59")
    
    
#relation d'ordre

def ordre_inferieur(horaire1,horaire2):
    horaire1=convert(horaire1)
    horaire2=convert(horaire2)
    #comparer les heures
    if horaire1[0]< horaire2[0]:
        return True
    #comparer les minutes si les heures sont égales
    elif horaire1[1]<= horaire2[1] and horaire1[0]== horaire2[0]:
        return True 
    else :
        return False

#trier la liste des creneaux suivant le premier horaire de chaque créneau

def ordonner(L_Total):
    #mettre tout dans une même liste
    L=[0]
    for l in L_Total :
        L+=l[1:]
    L[0]=str(len(L[1:])) 
    #trier la liste avec un tri bulle
    for i in range (int(L[0])):
        for j in range (1,int(L[0])-i):
            if ordre_inferieur(L[j+1][2:7],L[j][2:7]):
                L[j+1],L[j]=L[j],L[j+1]
    #retourner la liste triée
    return L



L1=['3','1 08:30-09:45','1 10:55-11:30','1 11:10-12:12']
L2=['4','1 08:31-09:50','1 10:45-11:30','1 13:15-14:12','1 17:30-17:40']
L3=['2','1 09:45-10:35','1 14:11-15:35']

L=[L1,L2,L3]

L_ordonnee=ordonner(L)
L_ordonnee

#fusionner les créneaux qui se chevauchent

#fusion de deux créneux
def fusion(H1,H2):
    L=[]
    #si H2 est inclu dans H1
    if ordre_inferieur(H2[2:7],H1[8:])and ordre_inferieur(H2[8:],H1[8:]):
        L.append(H1)
        return L
    #si H2 debute dans H1 
    elif ordre_inferieur(H1[8:],H2[8:]) and ordre_inferieur(H2[2:7],H1[8:])and ordre_inferieur(H1[2:7],H2[2:7]):
        L.append(H1[0:8]+H2[8:])
        return L
    #si ils sont disjoints
    else:
        L.append(H1)
        L.append(H2)
        return L

#fusionner les créneaux qui se chevauchent dans la liste de créneaux
def fusionner(L):
    #le nombre de creneaux
    n=int(L[0])
    #notre liste où on va retrouver les horaires non superposés
    L_final=[0]
    #On fixe le premier horaire qui nous permet de faire la comparaison au debut puis les changement suivant si il y a eu fusion ou non
    horaireFinRef=L[1]
    for i in range(2,n+1):
        horairefin=L[i]
        
        #si on a pas de fusion 
        if len(fusion(horaireFinRef,horairefin))==2:
            #on rajoute l'horaire s'il n'est pas déja dans la liste
            if horaireFinRef!=L_final[-1]:
                L_final.append(horaireFinRef)
            L_final.append(horairefin)
            #initiation de l'horaire de réference
            horaireFinRef=horairefin
            
       #si on peut fusionner
        else:
            #on insère le nouvel horaire fusionné dans notre liste
            horaireFinRef=fusion(horaireFinRef,horairefin)[0]
            L_final.append(horaireFinRef)
            
            #Si dans notre liste final le nouvel horaire peut se fusionner avec un horaire déjà dans la liste par une fusion anterieure 
            if len(L_final)>2 and len(fusion(L_final[-2],L_final[-1]))==1 :
                #on supprime l'intrevalle le moins englobant.
                del L_final[-2]
            
    L_final[0]=str(len(L_final[1:]))
    return L_final
       

L_fusionnee=fusionner(L_ordonnee)
L_fusionnee

#fonction donnant l'heure +1
def plus_1h(H):
    #convertir en int
    H=convert(H)
    Hbis=[]
    #ajouter une heure en traitant le cas particulier sur les minutes
    if H[1]!=0 :
        Hbis.append(H[0]+1)
        Hbis.append(H[1]-1)
    else:
        Hbis.append(H[0])
        Hbis.append(59)
    #convertir en str
    H=str(Hbis[0])+':'+str(Hbis[1])
    return H

#disponibilité dans une journée

def disponible (L):
    #les horaires limites
    debut="8:00"
    fin="17:59"
    #liste où l'on va mettre l'horaire qui est valable
    horaires=[]
    n=int(L[0])
    i=1
    #on teste le premier horaire
    if duree(debut,L[1][2:7])>60 :
        horaires.append(L[1][0]+' 08:00-08:59')
        
    #on teste entre les horaires de la journée
    while i<n:
        if duree( L[i][8:],L[i+1][2:7])>60 and horaires==[]:
            horaires.append(L[1][0]+' '+L[i][8:]+'-'+plus_1h(L[i][8:]))
        i+=1
    #on teste le dernier 
    if duree(L[-1][8:],fin)>60 and horaires==[]:
            horaires.append(L[1][0]+' 17:00-17:59')
    return horaires


""" Généralisation """

#fonction qui sépare par jour de la semaine
def separer(L):
    L_sep=[[0],[0],[0],[0],[0]]
    #conditions sur les 5 jours de la semaine
    for l in L[1:] :
        if l[0]=='1':
            L_sep[0].append(l)
        elif l[0]=='2':
            L_sep[1].append(l)
        elif l[0]=='3':
            L_sep[2].append(l)
        elif l[0]=='4':
            L_sep[3].append(l)
        else:
            L_sep[4].append(l)
    #initialisation du nombre d'horaires indisponibles dans chaque jour de la semaine     
    for i in range (len(L_sep)):
        L_sep[i][0]=str(len(L_sep[i][1:]))
    return L_sep

#Fonction qui calcule une disponibilité pour toute la semaine
def disponible_semaine(L):
    H=[]
    for i in range (len(L)):
        if L[i]!=['0']:
            H.append(disponible(L[i]))
            
        else:
            H.append([str(i)+' 08:00-08:59'])

    i=0
    while i<len(H):
        if H[i]!=[] :
            Horaire=H[i]
            i+=1
            break
    return Horaire

#%%

L1=['8','2 08:11-09:23','2 10:45-11:30','1 10:15-12:12','5 14:15-15:18','1 17:30-17:40','4 15:03-16:09','3 14:00-15:17','5 16:19-17:00']
L2=['5','1 10:31-11:50','2 12:35-17:34','1 16:15-17:12','5 11:15-15:18','4 15:30-17:40']
L3=['7','1 08:20-08:50','2 11:45-11:30','1 11:15-12:12','5 14:15-15:18','1 16:30-17:40','3 14:50-17:50','2 16:30-16:55']

#On ordonne par horaire
L_ordre=ordonner([L1,L2,L3])
print("liste ordonée :")
L_ordre

#On separe par jour de la semaine
L_sep=separer(L_ordre)
print("liste séparée par jours de la semaine :")
L_sep

#on fusionne les horaires dans chaque semaine
L_sep_fusion=[]
for l in L_sep :
    L_sep_fusion.append(fusionner(l))
    
print("la liste des indisponibilités de la semaine séparé par les jours de la semaine :")
L_sep_fusion

disponible_semaine(L_sep_fusion)






