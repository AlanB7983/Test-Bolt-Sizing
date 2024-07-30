# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 14:36:52 2022

@author: GMET_PORTABLE
"""




from M_Gestion_Listes_Tables import Table_Str_to_Table_Float, Liste_Str_to_Liste_Float, position, get_colonne_of_table, suppr_doublons_liste, valeur_in_table


def interpolation_lineaire(x1, x2, xi, y1, y2) :
    """

    Parameters
    ----------
    x1 : TYPE = Float
    x2 : TYPE = Float
    xi : TYPE = Float
    y1 : TYPE = Float
        Valeur de y évaluée en x1
    y2 : TYPE = Float
        Valeur de y évaluée en x2

    Returns
    -------
    yi : TYPE = Float
        Valeur de Y en xi compris entre x1 et x2 par interpolation linéaire

    """
    
    yi = y1 + ((y2 - y1)/(x2 - x1))*(xi - x1)
    return yi


###################################################################
# MANIPULATION DES GRANDEURS DES PROPRIETES PHYSIQUES DU MATERIAU #
###################################################################


def get_donnees_grandeur_fonction_T(L_Fichier, Grandeur) :
    """

    Parameters
    ----------
    L_Fichier : TYPE = Liste de listes de str
        Tableau issue de la conversion du fichier csv en liste de listes
    Grandeur : TYPE = str
        Nom de la grandeur physique dont on souhaite extraire les valeurs

    Returns
    -------
    L_Grandeur : TYPE = Liste de liste de str
        Tableau à 2 colonnes contenant la température dans la première colonne et la valeur de la grandeur à la température correspondante dans la deuxième.
        L'entête avec le nom des variables ['T', 'Grandeur'] est supprimé
        exemple : [['20', '200 000'], ['50', '193 000'], ..., ['500', '178 000']]

    """
    
    L_Grandeur = []
    # On trouve le numéro de la colonne correspondant à la grandeur renseignée par l'utilisateur
    i = 0
    while L_Fichier[0][i] != Grandeur and i < len(L_Fichier[0]) :
        i = i + 1
        num_colonne = i
    
    # On récupère la valeur de la température et de la grandeur correspondante
    i = 1 # On commence à 1 car on ne veut que les valeurs et pas le nom de la grandeur
    while L_Fichier[i][num_colonne] != '' and i < len(L_Fichier)-1 :
        L_Grandeur.append([L_Fichier[i][0], L_Fichier[i][num_colonne]])
        i = i + 1
      
    return L_Grandeur




def get_grandeur_T_donnee(L_Grandeur, L_T, T) :
    """

    Parameters
    ----------
    L_Grandeur : TYPE = Liste de liste de str
        Tableau à 2 colonnes contenant la température dans la première colonne et la valeur de la grandeur à la température correspondante dans la deuxième.
    L_T : TYPE = Liste de str
        Liste contenant les températures
    T : TYPE = int
        Valeur de la température à laquelle on veut connaitre la valeur de la grandeur
        La température doit faire partie des températures pour laquelle les grandeurs physiques sont connues 
        (ie : faire partie de L_T)

    Returns
    -------
    Grandeur_T : TYPE = Float
        Valeur de la grandeur à la température donnée

    """
    
    Liste_Str_to_Liste_Float(L_T)
    Table_Str_to_Table_Float(L_Grandeur)
    Index = position(T, L_T)
    
    Grandeur_T = L_Grandeur[Index][1]
    
    return Grandeur_T




def get_grandeur_T_quelconque(Nom_Grandeur, L_Fichier, T) :
    """

    Parameters
    ----------
    Nom_Grandeur : TYPE = Str
        Nom de la grandeur 
    L_Fichier : TYPE = Liste de liste
        DESCRIPTION.
    T : TYPE = Int ou Float
        Valeur de la température à laquelle on veut connaitre la valeur de la grandeur
        La température peut être une valeur quelconque 
        (ie : ne pas faire partie des températures pour lesquelles les propriétés physiques du matériau sont connues)
        
    Returns
    -------
    G_T : TYPE = Float
        Valeur de la grandeur à la température quelconque donnée, obtenue par interpolation linéaire

    """
    
    L_Grandeur = get_donnees_grandeur_fonction_T(L_Fichier, Nom_Grandeur)
    L_T = get_colonne_of_table(L_Grandeur, Index_Colonne = 0, Entete = True)
    
    if str(T) in L_T :
        G_T = get_grandeur_T_donnee(L_Grandeur, L_T, T)
        
    else :
        if T < float(L_T[0]) :
            G_T = get_grandeur_T_donnee(L_Grandeur, L_T, float(L_T[0]))
            
        elif T > float(L_T[-1]) :
            G_T = get_grandeur_T_donnee(L_Grandeur, L_T, float(L_T[-1]))
            
        else :
            # On cherche entre quelles valeurs de températures connues se trouve la valeur de T donnée
            i = 0
            while T > float(L_T[i]) and i < len(L_T) :
                i = i + 1
            T1 = float(L_T[i-1])
            T2 = float(L_T[i])
            
            x1 = T1
            x2 = T2
            xi = T
            y1 = get_grandeur_T_donnee(L_Grandeur, L_T, T1)
            y2 = get_grandeur_T_donnee(L_Grandeur, L_T, T2)
            G_T = interpolation_lineaire(x1, x2, xi, y1, y2)
        
    return G_T




######################################################################
# CREATION DE LA TABLE DE VALEURS DE LA COURBE DE LA REGLE DE NEUBER #
######################################################################


def create_neuber_rule_table(Delta_Sigma_N, Delta_Epsilon_N, K_F) :
    """

    Parameters
    ----------
    Delta_Sigma_N : TYPE = Float
        Valeur de l'intervalle de contraintes du cycle obtenu par calcul linéaire et noté Delta_Sigma_N
    Delta_Epsilon_N : TYPE = Float
        Valeur de l'intervalle de déformations du cycle obtenu par calcul linéaire et noté Delta_Epsilon_N
    K_F : TYPE = Int
        Valeur du facteur de réduction de la résistance à la fatigue

    Returns
    -------
    T_Neuber_Rule : TYPE = liste de listes de float
        Tableau contenant les valeurs de la courbe obtenue par la règle de Neuber à partir des données d'entrées
        et définie par Delta_Sigma*Delta_Epsilon = K_F²*Delta_Sigma_N*Delta_Epsilon_N

    """
    
    Cst = K_F*K_F*Delta_Sigma_N*Delta_Epsilon_N
    
    L_Delta_Sigma = []
    T_Neuber_Rule = []
    
    # Construction des valeurs
    L_Delta_Epsilon = [0.001 + 0.001*i for i in range(1, 500001)]
    for i in range(0, len(L_Delta_Epsilon)) :
        L_Delta_Sigma.append(Cst/L_Delta_Epsilon[i])
    
    for i in range(0, len(L_Delta_Epsilon)) :
        T_Neuber_Rule.append([L_Delta_Epsilon[i], L_Delta_Sigma[i]])
        
    return T_Neuber_Rule





##################################################
# EXTRACTION DE LA COURBE CONTRAINTE-DEFORMATION #
##################################################

def get_cyclic_curve_T_connu(L_Fichier_Cyclic_Curve, T) :
    """

    Parameters
    ----------
    L_Fichier_Cyclic_Curve : TYPE = Lsite de listes de str
        Tableau contenant les valeurs de la courbe cyclique contrainte-déformation du matériau pour les différentes températures
    T : TYPE = Int
        Valeur de la température à laquelle on veut extraire les valeurs de la courbe contrainte-déformation
        La température doit faire partie des températures pour laquelle les valeurs de la courbe contrainte-déformation sont connues 
        
    Returns
    -------
    T_Cyclic_Curve : TYPE = Liste de liste de float
        Tableau contenant les valeurs de la courbe contrainte-déformation du matériau à la température connue donnée

    """
    
    T_Cyclic_Curve = []
    
    for j in range(0, len(L_Fichier_Cyclic_Curve)) :
        if L_Fichier_Cyclic_Curve[j][0] == str(T) :
            T_Cyclic_Curve.append([L_Fichier_Cyclic_Curve[j][1], L_Fichier_Cyclic_Curve[j][2]])
            
    Table_Str_to_Table_Float(T_Cyclic_Curve)
    
    return T_Cyclic_Curve
    
    
    
    
def get_cyclic_curve_T_donnee(L_Fichier_Cyclic_Curve, T) :
    """

    Parameters
    ----------
    L_Fichier_Cyclic_Curve : TYPE = Lsite de listes de str
        Tableau contenant les valeurs de la courbe cyclique contrainte-déformation du matériau pour les différentes températures
    T : TYPE = Int
        Valeur de la température à laquelle on veut extraire les valeurs de la courbe contrainte-déformation
        La température peut être une valeur quelconque 
        (ie : ne pas faire partie des températures pour lesquelle les valeurs de la courbe contrainte-déformation du matériau sont connues)
        
    Returns
    -------
    T_Cyclic_Curve : TYPE = Liste de liste de float
       Tableau contenant les valeurs de la courbe contrainte-déformation du matériau à la température quelconque donnée,
       obtenues par interpolation linéaire

    """
    
    L_T = get_colonne_of_table(L_Fichier_Cyclic_Curve, Index_Colonne = 0, Entete = False)
    L_T = suppr_doublons_liste(L_T)
    
    if str(T) in L_T :
        T_Cyclic_Curve = get_cyclic_curve_T_connu(L_Fichier_Cyclic_Curve, T)
    
    else :
        if T < float(L_T[0]) :
            T_Cyclic_Curve = get_cyclic_curve_T_connu(L_Fichier_Cyclic_Curve, L_T[0])
            
        elif T > float(L_T[-1]) :
            T_Cyclic_Curve = get_cyclic_curve_T_connu(L_Fichier_Cyclic_Curve, L_T[-1])
            
        else :
        
            # On cherche entre quelles valeurs de températures connues se trouve la valeur de T donnée
            i = 0
            while T > float(L_T[i]) and i < len(L_T) :
                i = i + 1
            T1 = int(L_T[i-1])
            T2 = int(L_T[i])
            T_Cyclic_Curve_1 = get_cyclic_curve_T_connu(L_Fichier_Cyclic_Curve, str(T1))
            T_Cyclic_Curve_2 = get_cyclic_curve_T_connu(L_Fichier_Cyclic_Curve, str(T2))
            
            L_Delta_Epsilon = []
            L_Delta_Sigma = []
            
            i = 0
            
            while i < min(len(T_Cyclic_Curve_1),len(T_Cyclic_Curve_2)) :   
                x1 = T1
                x2 = T2
                xi = T
                y1 = T_Cyclic_Curve_1[i][0]
                y2 = T_Cyclic_Curve_2[i][0]
                Epsilon = interpolation_lineaire(x1, x2, xi, y1, y2)
                L_Delta_Epsilon.append(Epsilon)
                
                y1 = T_Cyclic_Curve_1[i][1]
                y2 = T_Cyclic_Curve_2[i][1]
                Sigma = interpolation_lineaire(x1, x2, xi, y1, y2)
                L_Delta_Sigma.append(Sigma)
                
                i = i + 1
            
            T_Cyclic_Curve = []
            for i in range(len(L_Delta_Sigma)) :
                T_Cyclic_Curve.append([L_Delta_Epsilon[i], L_Delta_Sigma[i]])
            Table_Str_to_Table_Float(T_Cyclic_Curve)
    return T_Cyclic_Curve




######################################
# EXTRACTION DE LA COURBE DE FATIGUE #
######################################

def get_fatigue_curve_T_connu(L_Fichier, T) :
    """

    Parameters
    ----------
    L_Fichier : TYPE = Liste de Liste de str
        Tableau contenant les valeurs dans le fichier correspondant.
    T : TYPE = int
        Valeur de la température à laquelle on veut extraire les valeurs de la courbe contrainte-déformation
        La température doit faire partie des températures pour laquelle les valeurs de la courbe cyclique sont connues 
        
    Returns
    -------
    T_Fatigue_Curve : TYPE = Liste de listes de float
        Tableau contenant les valeurs de la courbe de fatigue à la température connue donnée

    """
    
    T_Fatigue_Curve = []
    
    for j in range(0, len(L_Fichier)) :
        if L_Fichier[j][0] == str(T) :
            T_Fatigue_Curve.append([L_Fichier[j][1], L_Fichier[j][2]])
            
    Table_Str_to_Table_Float(T_Fatigue_Curve)
    return T_Fatigue_Curve



def get_fatigue_curve_T_donnee(L_Fichier_Fatigue_Curve, T) :
    """

    Parameters
    ----------
    L_Fichier_Fatigue_Curve : TYPE = Liste de listes de str
        Tableau contenant les valeurs de la courbe de fatigue du matériau pour les différentes températures
    T : TYPE = Int ou Float
        Valeur de la température à laquelle on veut extraire les valeurs de la courbe contrainte-déformation
        La température peut être une valeur quelconque 
        (ie : ne pas faire partie des températures pour lesquelle les valeurs de la courbe contrainte-déformation du matériau sont connues)

    Returns
    -------
    T_Fatigue_Curve : TYPE = Liste de listes de float
        Tableau contenant les valeurs de la courbe de fatigue à la température quelconque donnée, obtenues par interpolation linéaire

    """
    
    Grandeur_Presente = valeur_in_table('T', L_Fichier_Fatigue_Curve)
    
    L_Fichier_Fatigue_Curve = L_Fichier_Fatigue_Curve[1:] #On supprime l'entête
    
    if Grandeur_Presente == True : # La courbe de fatigue dépend de la température
        L_T = get_colonne_of_table(L_Fichier_Fatigue_Curve, Index_Colonne = 0, Entete = False)
        L_T = suppr_doublons_liste(L_T)
        
        # La température fait partie des températures pour lesquelles la courbe de fatigue est connue
        if str(T) in L_T :
            T_Fatigue_Curve = get_fatigue_curve_T_connu(L_Fichier_Fatigue_Curve, T)
            
        # La température ne fait PAS partie des températures pour lesquelles la courbe de fatigue est connue
        else :
            if T < float(L_T[0]) :
                T_Fatigue_Curve = get_fatigue_curve_T_connu(L_Fichier_Fatigue_Curve, L_T[0])
                
            elif T > float(L_T[-1]) :
                T_Fatigue_Curve = get_fatigue_curve_T_connu(L_Fichier_Fatigue_Curve, L_T[-1])
                
            else :
            
                # On cherche entre quelles valeurs de températures connues se trouve la valeur de T donnée
                i = 0
                while T > float(L_T[i]) and i < len(L_T) :
                    i = i + 1
                T1 = int(L_T[i-1])
                T2 = int(L_T[i])
                T_Fatigue_Curve_1 = get_fatigue_curve_T_connu(L_Fichier_Fatigue_Curve, str(T1))
                T_Fatigue_Curve_2 = get_fatigue_curve_T_connu(L_Fichier_Fatigue_Curve, str(T2))
                
                
                L_Grandeur = []
                L_N = []
                
                i = 0
                
                while i < min(len(T_Fatigue_Curve_1),len(T_Fatigue_Curve_2)) :   
                    x1 = T1
                    x2 = T2
                    xi = T
                    y1 = T_Fatigue_Curve_1[i][0]
                    y2 = T_Fatigue_Curve_2[i][0]
                    Grandeur = interpolation_lineaire(x1, x2, xi, y1, y2)
                    L_Grandeur.append(Grandeur)
                    
                    y1 = T_Fatigue_Curve_1[i][1]
                    y2 = T_Fatigue_Curve_2[i][1]
                    N = interpolation_lineaire(x1, x2, xi, y1, y2)
                    L_N.append(N)
                    
                    i = i + 1
                    
                T_Fatigue_Curve = []
                for i in range(len(L_N)) :
                    T_Fatigue_Curve.append([L_Grandeur[i], L_N[i]])
                Table_Str_to_Table_Float(T_Fatigue_Curve)
                
                
                
    else : #La courbe ne dépend pas de T
        T_Fatigue_Curve = L_Fichier_Fatigue_Curve
            
    return T_Fatigue_Curve





################################
# CALCUL DU NOMBRE DE CYCLES N #
################################

def calculate_N_pour_Delta_Epsilon_donnee(T_Fatigue_Curve, Delta_Epsilon) :
    """

    Parameters
    ----------
    T_Fatigue_Curve : TYPE = Liste de listes de float
        Tableau contenant les valeurs de la courbe de fatigue à la température quelconque donnée, obtenues par interpolation linéaire
    Delta_Epsilon : TYPE = Float
        Valeur de l'intervalle de déformations du cycle obtenu prenant en compte la concentration de contrainte,
        estimée avec la règle de Neuber et noté Delta_Epsilon

    Returns
    -------
    N : TYPE = Float
        Valeur du nombre de cycles obtenue via la courbe de fatigue définie à partir de Delta_Epsilon_Barre (N = f(Delta_Epsilon_Barre))
    
    """
    
    L_Delta_Epsilon = get_colonne_of_table(T_Fatigue_Curve, 0, True)
    L_N = get_colonne_of_table(T_Fatigue_Curve, 1, True)

    
    if Delta_Epsilon > L_Delta_Epsilon[0] :
        N = L_N[0]
    
    elif Delta_Epsilon < L_Delta_Epsilon[-1] :
        N = L_N[-1]
    
    else :
        index = 0
        while L_Delta_Epsilon[index] > Delta_Epsilon and index < len(L_Delta_Epsilon) :
            index = index + 1
    
        x1 = L_Delta_Epsilon[index-1]
        x2 = L_Delta_Epsilon[index]
        xi = Delta_Epsilon
        y1 = L_N[index-1]
        y2 = L_N[index]
        N = interpolation_lineaire(x1, x2, xi, y1, y2)
        
    return N



def calculate_N_pour_Sa_donnee(T_Fatigue_Curve, Delta_Sigma_Barre) :
    """

    Parameters
    ----------
    T_Fatigue_Curve : TYPE = Liste de listes de float
        Tableau contenant les valeurs de la courbe de fatigue à la température quelconque donnée, obtenues par interpolation linéaire
    Delta_Sigma_Barre : TYPE = Float
        Valeur de l'intervalle de contraintes du cycle obtenu prenant en compte la concentration de contrainte,
        estimée avec la règle de Neuber et noté Delta_Sigma

    Returns
    -------
    N : TYPE = Float
        Valeur du nombre de cycles obtenue via la courbe de fatigue définie à partir de l'amplitude
        de contrainte notée Sa (N = f(Sa))
    
    """
    
    Sa = Delta_Sigma_Barre/2
    L_Sa = get_colonne_of_table(T_Fatigue_Curve, 0, True)
    L_N = get_colonne_of_table(T_Fatigue_Curve, 1, True)
    
    Liste_Str_to_Liste_Float(L_Sa)
    Liste_Str_to_Liste_Float(L_N)

    if Sa > L_Sa[0] :
        N = L_N[0]
    
    elif Sa < L_Sa[-1] :
        N = L_N[-1]
    
    else :
        index = 0
        while L_Sa[index] > Sa and index < len(L_Sa) :
            index = index + 1
    
        x1 = L_Sa[index-1]
        x2 = L_Sa[index]
        xi = Sa
        y1 = L_N[index-1]
        y2 = L_N[index]
        N = interpolation_lineaire(x1, x2, xi, y1, y2)
        
    return N


def calculate_N (T_Fatigue_Curve, Delta_Sigma_Barre, Delta_Epsilon_Barre) :
    """

    Parameters
    ----------
    T_Fatigue_Curve : TYPE = Liste de listes de float
        Tableau contenant les valeurs de la courbe de fatigue à la température quelconque donnée, obtenues par interpolation linéaire
    Delta_Sigma_Barre : TYPE = Float
        Valeur de l'intervalle de contraintes réel du cycle, noté Delta_Sigma_Barre
    Delta_Epsilon_Barre : TYPE = Float
        Valeur de l'intervalle de déformations réel du cycle, noté Delta_Espilon_Barre

    Returns
    -------
    N : TYPE = Float
        Valeur du nombre de cycles obtenue via la courbe de fatigue quelque soit la façon dont elle est définie
        (N = f(Delta_Epsilon_Barre) ou N = f(Sa))

    """
    
    #On regarde si la courbe de fatigue est donnée en fonction de la déformation ou de la contrainte
    if int(T_Fatigue_Curve[0][0]) > 100 : #La courbe est donnée en contrainte
        N = calculate_N_pour_Sa_donnee(T_Fatigue_Curve, Delta_Sigma_Barre)
        
    else : #La courbe est donnée en déformation
        N = calculate_N_pour_Delta_Epsilon_donnee(T_Fatigue_Curve, Delta_Epsilon_Barre)
        
    return N

