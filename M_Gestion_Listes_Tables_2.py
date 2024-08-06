# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 09:59:37 2022

@author: GMET_PORTABLE
"""



def suppr_doublons_liste(Liste) :
    """

    Parameters
    ----------
    Liste : TYPE = Liste
        Liste dont on veut supprimer les éléments en double

    Returns
    -------
    L_New : TYPE = Liste
        Liste dont on a supprimé les éléments en double

    """
    
    L_New = []
    
    for i in Liste :
        if i not in L_New :
            L_New.append(i)

    return L_New



def Liste_Str_to_Liste_Float(Liste) :
    """

    Parameters
    ----------
    Liste : TYPE = Liste
        Liste dont on veut transfomer les éléments en float

    Returns
    -------
    None.

    """
    
    for i in range(0, len(Liste)) :
        Liste[i] = float(Liste[i])
        
        

def Table_Str_to_Table_Float(Table) :
    """

    Parameters
    ----------
    Table : TYPE = Liste de listes
        Liste de listes dont on veut transformer les éléments en float

    Returns
    -------
    None.

    """
    
    for i in range(0, len(Table)) :
        for j in range(0, len(Table[0])) :
            Table[i][j] = float(Table[i][j])
            
            
def get_colonne_of_table(Table, Index_Colonne, Entete) :
    """

    Parameters
    ----------
    Table : TYPE = Liste de liste de str
        Tableau dont on veut extraire une colonne
    Index_Colonne : TYPE = Int
        Numéro de la colonne que l'on veut extraire
    Entete : TYPE = Boolean
        True => On garde la première ligne qui est souvente une ligne d'entête
        False => On supprime la première ligne

    Returns
    -------
    L_Colonne : TYPE = Lste de str
        Liste  correspondant à la colonne extraite du tableau

    """
    
    if Entete == True :
        start = 0
        
    else :
        start = 1
    L_Colonne = []
    
    for i in range(start, len(Table)) :
        L_Colonne.append(Table[i][Index_Colonne])
        
    return L_Colonne




def position(Valeur, Liste) :
    """

    Parameters
    ----------
    Valeur : TYPE = Element quelconque (Float, str, liste, etc)
        Valeur dont on cherche la position dans la liste
    Liste : TYPE = Liste
        Liste contenant l'élément dont on cherche la position

    Returns
    -------
    i : TYPE = Int
        Position de la valeur dans la liste en comptant à partir de 1 pour le premier élément

    """
    
    i = 0
    while Valeur != Liste[i] :
        i = i + 1
        
    return i



def valeur_in_table(Valeur, Table) :
    """

    Parameters
    ----------
    Valeur : TYPE = Element quelconque (Float, str, liste, etc)
        Valeur dont on cherche si elle est présente dans la liste
    Table : TYPE = Liste de listes
        Liste de liste contenant l'élément dont on cherche s'il y est présent

    Returns
    -------
    Valeur_Presente : TYPE = Boolean
        True => l'élément se trouve dans la liste
        False => l'élément ne se trouve pas dans la liste

    """

    Valeur_Presente = False
    
    for i in range(0, len(Table)) :
        if Valeur in Table[i] :
            Valeur_Presente = True
            
    return Valeur_Presente



def get_liste_valeur_by_name(L_Fichier, L_Noms_Valeurs_Necessaires, Num_Col_Name, Num_Col_Val) : 
    """

    Parameters
    ----------
    L_Fichier : TYPE = Liste de listes de str
        Tableau issue de la conversion du fichier csv en liste de listes
    L_Noms_Valeurs_Necessaires : TYPE = Liste de str
        Liste contenant le nom des colonnes que l'on souhaite extraire du tableau
    Num_Col_Name : TYPE = Int
        Numéro de la colonne du tableau qui contient le nom des grandeurs
    Num_Col_Val : TYPE = Int
        Numéro de la colonne du tableau qui contient la valeur des grandeurs

    Returns
    -------
    L_Valeurs_Necessaires : TYPE = Liste de liste de str
        Tableau à deux colonnes dont la première contient le nom des grandeurs renseignées et la deuxième les valeurs associées

    """
    
    L_Noms_Valeurs = get_colonne_of_table(L_Fichier, Num_Col_Name, True)
    L_Valeurs = get_colonne_of_table(L_Fichier, Num_Col_Val, True)
    Liste_Str_to_Liste_Float(L_Valeurs)
    
    L_Valeurs_Necessaires = []
    
    for i in L_Noms_Valeurs_Necessaires :
        Index = position(i, L_Noms_Valeurs)
        Valeur = L_Valeurs[Index]
        L_Valeurs_Necessaires.append([i, Valeur])
    
    return L_Valeurs_Necessaires