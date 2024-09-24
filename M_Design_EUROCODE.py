# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 10:15:40 2024

@author: alanb
"""

import streamlit as st
# Ajouter un graphique simple
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import os


from M_Manipulation_Donnees_Materiaux_2 import get_grandeur_T_quelconque, get_donnees_grandeur_fonction_T
from M_Createur_Rapport_PDF_EUROCODE import create_pdf_eurocode



def calculer_marge(valeur, critere) :
    """

    Parameters
    ----------
    valeur : TYPE = float
        Valeur calculée au préalable
    critere : TYPE = float
        Valeur dont on veut calculer l'écart sous forme de marge en %

    Returns
    -------
    marge : TYPE = float
        Valeur de l'écart relatif entre la valeur calculée et la valeur du critère sous forme de pourcentage

    """
    
    marge = 100*(float(critere) - float(valeur))/float(critere)
    
    return marge


def trouver_marge_min(table_result) :
    """
    Donnée d'entrée :
        Liste de liste sous la forme : [["N° Boulon", "Nom du critère", "Effort de calcul [N]", "Effort de résistance [N]", "Marge [%]"]]
    Donnée de sortie :
        Float : valeur de la marge minimale contenue dans le tableau donné en entrée
    """
    
    marge_min = 100.0 # Valeur de départ la plus élevée possible
    
    for i in range(1, len(table_result)) : # On commence à un pour ne pas considérer l'entête
        if float(table_result[i][4]) < marge_min :
            marge_min = float(table_result[i][4])
    return marge_min


        

def determination_type_trou(d, forme_trou, d0, Largeur, Longueur) :
    if forme_trou == "Rond" :
        if d == 3 :
            if d0 > 3.4 :
                return("Trou rond surdimensionné")
            else :
                return("Trou rond normal")
        elif 4 <= d <= 5 :
            if d0 > d + 0.5 :
                return("Trou rond surdimensionné")
            else :
                return("Trou rond normal")
        elif d == 6 :
            if d0 > 6.6:
                return("Trou rond surdimensionné")
            else :
                return("Trou rond normal")
        elif 8 <= d <= 10 :
            if d0 > d + 1 :
                return("Trou rond surdimensionné")
            else :
                return("Trou rond normal")
        elif 12 <= d <= 16 :
            if d0 > d + 1.5 :
                return("Trou rond surdimensionné")
            else :
                return("Trou rond normal")
        elif 18 <= d <= 24 :
            if d0 > d + 2 :
                return("Trou rond surdimensionné")
            else :
                return("Trou rond normal")
        elif 27 <= d <= 45 :
            if d0 > d + 3 :
                return("Trou rond surdimensionné")
            else :
                return("Trou rond normal")
        elif 48 <= d <= 52 :
            if d0 > d + 4 :
                return("Trou rond surdimensionné")
            else :
                return("Trou rond normal")
        elif 56 <= d <= 72 :
            if d0 > d + 6 :
                return("Trou rond surdimensionné")
            else :
                return("Trou rond normal")
    else : # forme_trou == "Oblong"
        if d <= 12 :
            if Largeur <= d + 1.5 and Longueur <= d + 4 :
                return("Trou oblong court")
            elif Largeur <= d + 1.5 and Longueur <= (d + 3) * 2 :
                return("Trou oblong long")
            else :
                return ("Trou oblong très long")
        elif 12 < d <= 14 :
            if Largeur <= d + 1.5 and Longueur <= d + 4 :
                return("Trou oblong court")
            elif Largeur <= d + 1.5 and Longueur <= (d + 3) * 2 + 1 :
                return("Trou oblong long")
            else :
                return ("Trou oblong très long")
        elif 14 < d <= 16 :
            if Largeur <= d + 1.5 and Longueur <= d + 6 :
                return("Trou oblong court")
            elif Largeur <= d + 1.5 and Longueur <= (d + 4) * 2 :
                return("Trou oblong long")
            else :
                return ("Trou oblong très long")
        elif 16 < d <= 18 :
            if Largeur <= d + 2 and Longueur <= d + 6 :
                return("Trou oblong court")
            elif Largeur <= d + 2 and Longueur <= (d + 4) * 2 + 1 :
                return("Trou oblong long")
            else :
                return ("Trou oblong très long")
        elif 18 < d <= 20 :
            if Largeur <= d + 2 and Longueur <= d + 6 :
                return("Trou oblong court")
            elif Largeur <= d + 2 and Longueur <= (d + 5) * 2 :
                return("Trou oblong long")
            else :
                return ("Trou oblong très long")
        elif 20 < d <= 22 :
            if Largeur <= d + 2 and Longueur <= d + 6 :
                return("Trou oblong court")
            elif Largeur <= d + 2 and Longueur <= (d + 5) * 2 + 1 :
                return("Trou oblong long")
            else :
                return ("Trou oblong très long")
        elif 22 < d <= 24 :
            if Largeur <= d + 2 and Longueur <= d + 8 :
                return("Trou oblong court")
            elif Largeur <= d + 2 and Longueur <= (d + 6) * 2 :
                return("Trou oblong long")
            else :
                return ("Trou oblong très long")
        elif 24 < d <= 27 :
            if Largeur <= d + 3 and Longueur <= d + 10 :
                return("Trou oblong court")
            elif Largeur <= d + 3 and Longueur <= (d + 6) * 2 + 1 :
                return("Trou oblong long")
            else :
                return ("Trou oblong très long")
        elif 27 < d <= 30 :
            if Largeur <= d + 3 and Longueur <= d + 10 :
                return("Trou oblong court")
            elif Largeur <= d + 3 and Longueur <= (d + 7) * 2 + 1 :
                return("Trou oblong long")
            else :
                return ("Trou oblong très long")
        elif 30 < d <= 33 :
            if Largeur <= d + 3 and Longueur <= d + 10 :
                return("Trou oblong court")
            elif Largeur <= d + 3 and Longueur <= (d + 8) * 2 :
                return("Trou oblong long")
            else :
                return ("Trou oblong très long")
        elif 33 < d <= 36 :
            if Largeur <= d + 3 and Longueur <= d + 10 :
                return("Trou oblong court")
            elif Largeur <= d + 3 and Longueur <= (d + 9) * 2 :
                return("Trou oblong long")
            else :
                return ("Trou oblong très long")



def diametre_trou_normal_max(d) :
    if int(d) in range(0, 16) :
        return int(d + 1)
    elif int(d) in range(16, 27) :
        return int(d + 2)
    elif int(d) in range(27, 1000) :
        return int(d + 3)
    else :
        return int(d)

def determine_dm(d, L_dm) :
    for i in range(0, len(L_dm)) :
        if float(L_dm[i][0]) == float(d)  :
            dm = float(L_dm[i][1])


    return dm
        

def page_EUROCODE() :

    # =========================================================================
    # Variables 
    # =========================================================================

    liste_classe = ["4.6", "4.8", "5.6", "5.8", "6.8", "8.8", "10.9"] 
    liste_position = ["Intérieure", "Rive"]
    L_dm = [[3,5.75], [4,7.35], [5,8.4], [6,10.5], [8,13.7], [10,16.9], [12,19], [14,22.2], [16,25.4], [18,28.55], [20,31.75], [22,35.85], [24,38], [27,43.1], [30,47.9], [33,52.7], [36,57.9], [39,63.2], [42,68.15], [45,73.5], [48,78.8], [52,84.1], [56,89.3], [60,94.6], [64,99.95]]

    
    # =============================================================================
    # TITRE DE L'APPLICATION ET INTRODUCTION 
    # =============================================================================
    
    st.title("Dimensionnement de la boulonnerie selon l'EUROCODE")

    # saut de ligne
    st.write("\n")

    with st.expander("INTRODUCTION ET RAPPEL DES HYPOTHÈSES.") :
        st.subheader("Objectifs et conditions d'application")
        st.write("Cette partie est dédiée au dimensionnement des liaisons boulonnées selon les règles de conception et de calcul de la norme **NF EN 1993-1-8 (Eurocode 3 : Calcul des structures en acier – Calcul des assemblages)**. Elle concerne les assemblages soumis à un chargement statique prédominant. Les aciers qui peuvent les composer, éléments de serrage comme pièces assemblées, doivent être de nuances S235, S275, S355, S420, S450 et S460. Les règles spécifiques aux attaches par boulons, rivets ou axes d’articulation sont données dans la **section 3** du code. Elles ne sont applicables qu’aux classes de boulons de qualité suivantes, données avec leurs limite d’élasticité $f_{yb}$ et résistance ultime à la traction $f_{ub}$ associées :")
        st.image("Pictures/tableau_fu_fy_introduction.PNG", use_column_width=True)
        st.write("Les attaches boulonnées sont divisées en 5 catégories qui dépendent de l’effort subi et de leur condition d’utilisation :")
        st.write("-	**Catégorie A**, pour les boulons travaillant à la pression diamétrale qui ne nécessitent pas de préserrage")
        st.write("- **Catégorie B**, pour les boulons précontraints à haute résistance devant résister au glissement à l’état limite de service (ELS)")
        st.write("- **Catégorie C**, pour les boulons précontraints à haute résistance devant résister au glissement à l’état ultime de service (ELU)")
        st.write("- **Catégorie D**, pour les boulons sollicités en traction qui ne nécessite pas de préserrage")
        st.write("- **Catégorie E**, pour les boulons précontraints à haute résistance sollicités en traction")
        st.write("Il est alors possible, pour une attache soumise à des efforts combinés, d’appartenir à plusieurs catégories (A et D, B et E ou C et E). A noter que seuls les boulons de classes 8.8 et 10.9 peuvent entrer dans les catégories B, C et E. Chaque catégorie nécessite la vérification de différents critères, donnés dans le **Tableau 3.2** et calculés selon les règles des sections **3.6**, **3.7**, **3.8** et **3.9**.")

        st.subheader("Présentation")
        st.write("Cette application simple d’utilisation se compose en plusieurs parties. Après avoir choisi le type d’élément de serrage, l’utilisateur doit renseigner :")
        st.write("1. les données liées à l'élément de serrage")
        st.write("2. les données liées à l'assemblage, en temres de géométrie et de matériaux")
        st.write("3. les efforts sollicitant la liaison")
        st.write("4. les conditions de calcul : catégorie(s), données liée à la précontrainte, etc.")
        st.write("Les résultats sont ensuite générés sous la forme de tableau, un par catégorie étudiée, et sous la forme :")
        st.write("N° Boulon | Nom du critère | Effort de calcul [N] | Effort de résistance [N] | Marge associée [%]")
        st.write("")
        st.write("Un rapport automatique est généré et peut être téléchargé. Il rassemble les informations renseignées, les critères évalués, les résultats et le détail des formules utilisées.")
        st.write("Bon dimensionnement !")


    
    # =============================================================================
    # DONNEES D'ENTREE    
    # =============================================================================

    st.header("SAISIE DES DONNÉES D'ENTRÉE") # Partie


    
    # DONNEES LIEES A L'ELEMENT DE SERRAGE #
    ########################################
    
    st.subheader("Données liées à l'élément de serrage") #Sous-Partie

    st.write("- ##### *Type d'élément de serrage*") #Sous-Partie
    
    type_boulonnerie = st.radio("", ("Boulon", "Rivet"), horizontal=True, label_visibility="collapsed")

    type_bolt_col1, type_bolt_col2, type_bolt_col3 = st.columns([1, 1, 1])

    # Classe (menu déroulant)
    with type_bolt_col1 :
        classe = st.selectbox("Classe de l'élément de serrage : ", liste_classe)
    
    # Tête fraisée (case à cocher)
    with type_bolt_col2 :
        tete_fraisee_check = st.checkbox("Tête fraisée")
    
    # Résine injectée (case à cocher)
    with type_bolt_col3 :
        resine_check = st.checkbox("Résine injectée")
    
    st.write("") # Saut de ligne

    
    st.write("- ##### *Données géométriques*")
    bolt_goem_data_col1, bolt_goem_data_col2 = st.columns([1, 1])

    with bolt_goem_data_col1 :
        st.write("Type de trou")
        forme_trou = st.radio("", ("Rond", "Oblong"), label_visibility="collapsed")
        d = st.text_input("Diamètre nominal, $d [mm]$ :", placeholder = "0.0")
        p = st.text_input("Pas, $p [mm]$ :", placeholder = "0.0")
        

    with bolt_goem_data_col2 :
        if forme_trou == "Rond" :
            d0 = st.text_input("Diamètre du perçage, $d_0 [mm]$ :", placeholder = "0.0")
            Largeur = 0.0
            longueur = 0.0
        else :
            Largeur = st.text_input("Largeur du trou oblong, $L_0 [mm]$ :", placeholder = "0.0")
            longueur = st.text_input("Longueur du trou oblong, $l_0 [mm]$ :", placeholder = "0.0")
            d0 = Largeur

    # On met une valeur par défaut aux variables pour ne pas générer de message d'erreur
    d = float(d) if d else 1.0
    p = float(p) if p else 1.0
    d0 = float(d0) if d0 else 1.0
    Largeur = float(Largeur) if Largeur else 0.0
    longueur = float(longueur) if longueur else 0.0
    if d > 2.0 :
        dm = determine_dm(d, L_dm)
    else :
        dm = 1.0

    # On détermine le type de trou et on affiche le résultat
    st.write("") # Saut de ligne
    if d > 2.0 :
        type_trou = determination_type_trou(d, forme_trou, d0, Largeur, longueur)
        st.write("D'après les données saisies, il s'agit d'un " + type_trou.lower())
    else :
        type_trou = "trou rond normal"
    
    
    st.write("") # Saut de ligne
    if forme_trou == "Oblong" :
        st.write("Est-ce que l'axe longitudinal est parallèle ou perpendiculaire aux efforts de cisaillement ? (Voir Figure ci-dessous)")
        axe_longi = st.radio("", ("Parallèle", "Perpendiculaire"), horizontal=True, label_visibility="collapsed")
        st.image("Pictures/def_axe_trou_oblong.PNG", use_column_width=True)
        type_trou = type_trou + " " + axe_longi
        st.write("") # Saut de ligne
    st.write("") # Saut de ligne
    


    # On détermine les données intermédiaires
    d1 = d - 1.0825*p             # Diamètre au sommet de l'écrou [mm]
    d2 = d - 0.6495*p             # Diamètre moyen de la vis [mm]
    d3 = d - 1.2268*p             # Diamètre à fond de filet (ou diamètre du noyau), noté aussi dn [mm]
    S = np.pi*d*d/4               # Section du fût
    As = (((d3+d2)/2)**2)*np.pi/4 # Section résistante
    GammaM2 = 1.25                # Coefficient partiel pour la résistance des boulons
    GammaM4 = 1.0                 # Coefficient partiel pour la résistance en pression diamétrale des boulons injectés
    GammaM3ser = 1.1              # Coefficient partiel
    
    
    if "surdimensionné" in type_trou :
        kb = 0.8                   # Coefficient de trou
    elif forme_trou == "Oblong" :
        kb = 0.6                   # Coefficient de trou
    else :
        kb = 1.0                   # Coefficient de trou

    if type_trou == "Trou rond surdimensionné" or type_trou == "Trou oblong court Perpendiculaire" :
        ksp = 0.85
    elif type_trou == "Trou oblong long Perpendiculaire" :
        ksp = 0.7
    elif type_trou == "Trou oblong court Parallèle" :
        ksp = 0.76
    elif type_trou == "Trou oblong long Parallèle" :
        ksp = 0.63
    else :
        ksp = 1.0

    if resine_check :
        if type_trou == "Normal" :
            ksresine = 1
        elif type_trou == "Surdimensionné" :
            d0normalmax = diametre_trou_normal_max(d) # Diamètre maximal d'un trou normal pour un diamètre de bolt d
            m = float(d0normalmax) - d0
            ksresine = 1 - 0.1*m
        elif "Oblong" in type_trou :
            m = (longueur - Largeur)/2
            ksresine = 1 - 0.1*m
        else : 
            ksresine = 1
        
    classe_part1 = classe[0] # On récupère le premier digit de la classe de la boulonnerie pour calculer fub
    if classe_part1 == "1" :
        fub = float(classe_part1)*1000 # résistance ultime à la traction
    else :
        fub = float(classe_part1)*100  # résistance ultime à la traction

    

    # On créé un tableau pandas qui servira aussi pour le rapport
    L_Designation = ["Diamètre nominal", "Pas", "Diamètre du trou", "Diamètre en sommet d'écrou", "Diamètre moyen", "Diamètre à fond de filet", "Section résistante à la traction", 
                     "Section brute ou du fût lisse", "Résistance ultime à la traction (à 20°C)", "Coefficient de trou", "Coefficient de trou en précontrainte",
                     "Coefficient partiel pour la résistance des boulons"]
    L_Symbole = ["d", "p", "d0", "d1", "d2", "d3", "As", "S", "fub", "kb", "ks", "GammaM2"]
    L_Valeur = [d, p, d0, d1, d2, d3, round(As, 2), round(S, 2), fub, kb, ksp, GammaM2]
    L_Unite = ["[mm]", "[mm]", "[mm]", "[mm]", "[mm]", "[mm]", "[mm²]", "[mm²]", "[MPa]", "[-]", "[-]", "[-]"]




    # DONNEES LIEES A L'ASSEMBLAGE #
    ################################

    st.subheader("Données liées à l'assemblage") #Sous-Partie

    st.write("- ##### *Données géométriques*") #Sous-Partie
    st.write("Est-ce que les notions d'entraxe longitudinal et d'entraxe transversal, respectivement notés $p_1$ et $p_2$, visibles sur la figure ci-dessous sont définies ?")
    st.image("Pictures/definition_entraxe_longi_transv.PNG", use_column_width=True)
    p1_cal1, p2_col2, empty_col3 = st.columns([1, 1, 1])
    with p1_cal1 :
        p1_check = st.checkbox("Entraxe longitudinal, $p_1$")
    with p2_col2 :
        p2_check = st.checkbox("Entraxe transversal, $p_2$")

    if p1_check and p2_check :
        quinconce_check = st.checkbox("Est-ce qu'il s'agit d'un assemblage en quinconce comme décrit sur la figure ci-dessous ?")
        st.image("Pictures/definition_assemblage_quinconce.PNG", use_column_width=True)

    st.write("") # Saut de ligne
    bolt_goem_data_col1, bolt_goem_data_col2 = st.columns([1, 1])

    with bolt_goem_data_col1 :
        tp = st.text_input("Épaisseur de la plaque sous tête ou sous écrou, $t_p [mm]$ :", placeholder = "0.0")
        t = st.text_input("Épaisseur minimale des pièces assemblées extérieures, $t [mm]$ :", placeholder = "0.0")
        e1 = st.text_input("Pince longitudinale, $e_1 [mm]$ :", placeholder = "0.0")
        e2 = st.text_input("Pince transversale, $e_2 [mm]$ :", placeholder = "0.0")
        Lj = st.text_input("Entraxe extrême dans la direction des efforts, $L_j [mm]$ :", placeholder = "0.0")
        

                                     

    with bolt_goem_data_col2 :
        if p1_check :
            p1 = st.text_input("Entraxe longitudinal, $p_1 [mm]$ :", placeholder = "0.0")
            p1 = float(p1) if p1 else 1.0
            # On ajoute dans le tableau des données d'entrée
            L_Designation.append("Entraxe longitudinal")
            L_Symbole.append("p1")
            L_Valeur.append(p1)
            L_Unite.append("[mm]")
        else : # Si p1 et p2 ne sont pas définis, on met une valeur infinie pour pas qu'elle soit utilisée dans le calcul des critères
            p1 = 100000.0
            
        if p2_check :
            p2 = st.text_input("Entraxe transversal, $p_2 [mm]$ :", placeholder = "0.0")
            p2 = float(p2) if p2 else 1.0
            # On ajoute dans le tableau des données d'entrée
            L_Designation.append("Entraxe transversal")
            L_Symbole.append("p2")
            L_Valeur.append(p2)
            L_Unite.append("[mm]")
        else :# Si p1 et p2 ne sont pas définis, on met une valeur infinie pour pas qu'elle soit utilisée dans le calcul des critères
            p2 = 100000.0

        if p1_check and p2_check :
            if quinconce_check :
                L = st.text_input("Distance minimale entre 2 perçages, $L [mm]$ :", placeholder = "0.0")
                L = float(L) if L else 0.0
                # On ajoute dans le tableau des données d'entrée
                L_Designation.append("Distance minimale entre 2 perçages")
                L_Symbole.append("L")
                L_Valeur.append(L)
                L_Unite.append("[mm]")
            
        if tete_fraisee_check :
            pf = st.text_input("Profondeur du fraisage, $p_f [mm]$ :", placeholder = "0.0")
            pf = float(pf) if pf else 1.0
            # On ajoute dans le tableau des données d'entrée
            L_Designation.append("Profondeur du fraisage")
            L_Symbole.append("pf")
            L_Valeur.append(pf)
            L_Unite.append("[mm]")
        if resine_check :
            tb_resine = st.text_input("Épaisseur efficace de résine en pression diamétrale, $t_{b,résine} [mm]$ :", placeholder = "0.0")
            tb_resine = float(tb_resine) if tb_resine else 1.0
            # On ajoute dans le tableau des données d'entrée
            L_Designation.append("Épaisseur efficace de résine en pression diamétrale")
            L_Symbole.append("tb,résine")
            L_Valeur.append(tb_resine)
            L_Unite.append("[mm]")

    e1 = float(e1) if e1 else 1.0
    e2 = float(e2) if e2 else 1.0
    t = float(t) if t else 1.0
    tp = float(tp) if tp else 1.0
    Lj = float(Lj) if Lj else 1.0

    # On teste la valeur de Lj pour savoir s'il s'agit d'un assemblage long
    if Lj > 15*d :
        check_assemblage_long = True
    else :
        check_assemblage_long = False

    # On ajoute dans le tableau des données d'entrée
    L_Designation.append("Épaisseur de la plaque sous tête ou sous écrou")
    L_Designation.append("Épaisseur minimale des pièces assemblées extérieures")
    L_Designation.append("Pince longitudinale")
    L_Designation.append("Pince transversale")
    L_Designation.append("Entraxe extrême dans la direction des efforts")
    L_Symbole.append("tp")
    L_Symbole.append("t")
    L_Symbole.append("e1")
    L_Symbole.append("e2")
    L_Symbole.append("Lj")
    L_Valeur.append(tp)
    L_Valeur.append(t)
    L_Valeur.append(e1)
    L_Valeur.append(e2)
    L_Valeur.append(Lj)
    L_Unite.append("[mm]")
    L_Unite.append("[mm]")
    L_Unite.append("[mm]")
    L_Unite.append("[mm]")
    L_Unite.append("[mm]")

    st.image("Pictures/definition_donnee_assemblage_full.PNG", use_column_width=True, caption="Définition des données d'assemblage")
    
    st.write("") # Saut de ligne
    
    st.write("- ##### *Données matériaux*") #Sous-Partie
    mat_piece_col1, mat_piece_col2 = st.columns([1, 1])
    with mat_piece_col1 :
        fu = st.text_input("Résistance ultime à la traction minimale des pièces assemblée, $f_u [MPa]$ :", placeholder = "0.0")
        fu = float(fu) if fu else 1.0
        # On ajoute dans le tableau des données d'entrée
        L_Designation.append("Résistance ultime à la traction minimale des pièces assemblée")
        L_Symbole.append("fu")
        L_Valeur.append(fu)
        L_Unite.append("[MPa]")
    with mat_piece_col2 :
        if resine_check :
            fbresine = st.text_input("Résistance en pression diamétrale de la résine, $f_{b,résine} [MPa]$ :", placeholder = "0.0")
            fbresine = float(fbresine) if fbresine else 1.0
            # On ajoute dans le tableau des données d'entrée
            L_Designation.append("Résistance en pression diamétrale de la résine")
            L_Symbole.append("fb,resine")
            L_Valeur.append(fbresine)
            L_Unite.append("[MPa]")
    

    # Création d'un dictionnaire
    D_bolt_geom_data = {
        'Désignation' : L_Designation,
        'Symbole' : L_Symbole,
        'Valeur' : L_Valeur,
        'Unité' : L_Unite
        }
    
    # Création du DataFrame pandas à partir du dictionnaire
    df_bolt_geom_data = pd.DataFrame(D_bolt_geom_data)
    st.write("") # Saut de ligne


    
    # ===================================
    # Saisie du torseur mécanique
    # ===================================
    st.subheader("Efforts sollicitant la liaison")

    # On crée in tableau de saisie vide
    if 'efforts_ext' not in st.session_state:
        st.session_state.efforts_ext = pd.DataFrame(columns=['N° Boulon', 'Position', 'Effort de traction, Ft,Ed [N]', 'Effort de cisaillement selon x, Fvx,Ed [N]', 'Effort de cisaillement selon y, Fvy,Ed [N]'])
        
    # Saisies utilisateur pour ajouter des données
    saisie_effort_col1, saisie_effort_col2 = st.columns([1, 1])
    with saisie_effort_col1 :
        FtEd = st.text_input('Effort de traction, $F_{t,Ed}$ [N]', placeholder = 0.0)
    with saisie_effort_col2 :
        FvxEd = st.text_input('Effort de cisaillement selon x, $F_{vx,Ed}$ [N]', placeholder = 0.0)
        
    st.write("") # Saut de ligne    
    saisie_effort_col3, saisie_position_col4 = st.columns([1, 1])
    with saisie_effort_col3 :
        FvyEd = st.text_input('Effort de cisaillement selon y, $F_{vy,Ed}$ [N]', placeholder = 0.0)
    with saisie_position_col4 :
        position = st.selectbox('Position', liste_position)
    
    but_col1, but_col2, but_col3 = st.columns([1,1,4])
    indice_boulon = 1
    with but_col1 :
        # Bouton pour ajouter les données au DataFrame
        if st.button('Ajouter', use_container_width = True) :
            indice_boulon = st.session_state.efforts_ext.shape[0] + 1
            new_data = pd.DataFrame({'N° Boulon': [indice_boulon], 'Position': [position], 'Effort de traction, Ft,Ed [N]' : [float(FtEd)], 'Effort de cisaillement selon x, Fvx,Ed [N]': [float(FvxEd)], 'Effort de cisaillement selon y, Fvy,Ed [N]' : [float(FvyEd)]})
            st.session_state.efforts_ext = pd.concat([st.session_state.efforts_ext, new_data], ignore_index=True)
    with but_col2:
        if st.button('Effacer', use_container_width = True):
            st.session_state.efforts_ext = pd.DataFrame(columns=['N° Boulon', 'Position', 'Effort de traction, Ft,Ed [N]', 'Effort de cisaillement selon x, Fvx,Ed [N]', 'Effort de cisaillement selon y, Fvy,Ed [N]'])

    # Afficher les données sous forme de tableau
    st.dataframe(st.session_state.efforts_ext)

    # On crée une liste de listes à partir de ce tableau dataframe
    torseur_effort = [st.session_state.efforts_ext.columns.tolist()] + st.session_state.efforts_ext.values.tolist()  
    
    # saut de ligne
    st.write("\n")
    
    # saut de ligne
    st.write("\n")



    
    # =======================================
    # Condition de calcul
    # =======================================
    
    st.subheader("Conditions de calcul")

    if classe == "8.8" or classe == "10.9" :
    
        st.write("- ##### *Fonction de l'élément de serrage*")
        fct_bolt_col_1, fct_bolt_col_2 = st.columns([1, 1])
        with fct_bolt_col_1 :
            check_preload = st.checkbox("Boulonnerie précontrainte")
        # saut de ligne
        st.write("\n")
        
        # saut de ligne
        st.write("\n")
    
        if check_preload :
            st.write("Valeur de l'effort de précontrainte $F_{p,Cd}$.")
            F0 = st.text_input("$F_{p,Cd}$ [N] :", placeholder = "0.0")
            F0 = float(F0) if F0 else 0.0
            
            st.write("$F_{p,Cd}$ pris en compte dans les efforts saisis ?")
            F0_selection = st.radio("", ("oui", "non"), horizontal=True, label_visibility="collapsed", key="test")

            torseur_effort_full = []
            
            if F0_selection == "non" :
                # On demande la valeur de Lambda
                st.write("Valeur du coefficient de rigidité $\Lambda$.")
                Lambda = st.text_input("$\Lambda$ [-] :", placeholder = "0.0")
                Lambda = float(Lambda) if Lambda else 0.0
                st.info("Prendre $\Lambda$ = 0 revient à prendre l'hypothèse d'une liaison infiniment rigide.")
    
                # On ajoute une colonne pour noter F0 dans le tableau et pour écrire Ft,Ed,p
                for index, ligne in enumerate(torseur_effort) :
                    if index == 0 :
                        # Si c'est la première ligne (entête), ajouter le nom des nouvelles colonnes
                        nouvelle_ligne = ligne + ["Effort de précontrainte, Fp,Cd [N]", "Effort de traction d'origine externe et interne, Ft,Ed,p [N]"]  # Ajout des en-têtes pour les nouvelles colonnes
                    else :
                        # Convertir les valeurs numériques de Col1
                        col2_val = float(ligne[2])
    
                        # Calcul pour la nouvelle colonne Ft,Ed,p 
                        FtEdp = F0 + float(Lambda)*col2_val

                        # Ajouter la nouvelle colonne 6 (F0) et colonne 7 (Ft,Ed,p)
                        nouvelle_ligne = ligne + [float(F0), FtEdp]
                    
                    # Ajouter la nouvelle ligne modifiée à la liste finale
                    torseur_effort_full.append(nouvelle_ligne)

            # Si F0 a été pris en compte dans les résultats saisis
            else :
                # On ajoute une colonne pour noter F0 dans le tableau et pour écrire Ft,Ed,p
                for index, ligne in enumerate(torseur_effort) :
                    if index == 0 :
                        # Si c'est la première ligne (entête), ajouter le nom des nouvelles colonnes
                        nouvelle_ligne = ligne + ["Effort de précontrainte, Fp,Cd [N]", "Effort de traction d'origine externe et interne, Ft,Ed,p [N]"]  # Ajout des en-têtes pour les nouvelles colonnes
                    else :
                        # On copie colle la valeur de Ft,Ed,p dans la dernière colonne
                        FtEdp = float(ligne[2])

                        # Ajouter la nouvelle colonne 6 (F0) et colonne 7 (Ft,Ed,p)
                        nouvelle_ligne = ligne + [float(F0), float(FtEdp)]
                    
                    # Ajouter la nouvelle ligne modifiée à la liste finale
                    torseur_effort_full.append(nouvelle_ligne)


        # Si on est de classe 8.8 ou 10.9 mais qu'on n'est pas précontraint
        else :
            check_preload = False
            torseur_effort_full = torseur_effort

        # saut de ligne
        st.write("\n")

        if check_preload :
            # On demande le nombre de pièces assemblées 
            st.write("Nombre de pièces assemblées (hors rondelles)")
            nb_piece = st.number_input("Nombre de pièces assemblées (hors rondelles)", min_value = 2, step = 1, label_visibility="collapsed")
            n = nb_piece - 1
    
            # On demande de choisir le coefficient de frottement mu
            st.write("Sélectionner le coefficient de frottement $\mu$ en fonction du traitement de surface détaillé dans le tableau ci-dessous")
            mu = st.radio("", ("0.50", "0.40", "0.30", "0.20"), horizontal=True, label_visibility="collapsed", key="mu")
            mu = float(mu) if mu else 0.2
            T_mu_Data = [["µ [-]", "Classe", "Traitement de surface"], ["0.50", "A", "Surfaces grenaillées ou sablées, débarrassées de toute rouille non adhérente, exemple de piqûres."], 
                 ["0.40", "B", "Surfaces grenaillées ou sablées : \n - puis métallisées par projection d'un produit à base d'aluminium ou de zinc \n - avec une peinture au zinc silicate (alcalin) inorganique d'une épaisseur de 50 µm à 80 µm"],
                 ["0.30", "C", "Surfaces nettoyées à la brosse métallique ou au chalumeau, débarrassées de toute rouille non adhérente."],
                 ["0.20", "D", "Surfaces brutes de laminage."]]
            df_T_mu_Data = pd.DataFrame(T_mu_Data[1:], columns=T_mu_Data[0])
            st.write(df_T_mu_Data)

            # saut de ligne
            st.write("\n")

    
    # Si la boulonnerie n'est pas de classe 8.8 ou 10.9                 
    else :
        check_preload = False
        torseur_effort_full = torseur_effort

    
    # saut de ligne
    st.write("\n")

    # Torseur finalement utilisé pour le dimensionnement
    if check_preload : # On ne l'affiche que si on est précontraint parce que sinon il n'y a rien qui change
        st.write("Le torseur d'effort finalement utilisé pour le dimensionnement de la boulonnerie en fonction des conditions de calcul saisies est donné dans le tableau ci-dessous.")
        
        # Convertir la liste de listes en DataFrame
        df_torseur_full = pd.DataFrame(torseur_effort_full[1:], columns=torseur_effort_full[0])
        
        # Afficher le DataFrame dans Streamlit
        st.dataframe(df_torseur_full)
    else :
        # On ne l'affiche pas mais on le convertie en dataframe pour l'afficher dans le rapport
        df_torseur_full = pd.DataFrame(torseur_effort_full[1:], columns=torseur_effort_full[0])
        


    # saut de ligne
    st.write("\n")

    st.write("- ##### *Catégorie*") #Sous-Partie
    if check_preload :
        critere_col1, critere_col2, critere_col3 = st.columns([1, 1, 1])
        with critere_col1 :
            check_cat_B = st.checkbox("Catégorie B : Résistant au glissement à l'ELS")
        with critere_col2 :
            check_cat_C = st.checkbox("Catégorie C : Résistant au glissement à l'ELU")
        with critere_col3 :
            check_cat_E = st.checkbox("Catégorie E : Attaches tendues par boulons précontraints à haute résistance")
        if (check_cat_B and check_cat_E) or (check_cat_C and check_cat_E) or (check_cat_C and check_cat_B and check_cat_E) :
            check_combine = True
        else :
            check_combine = False
        # On met une valeur False apr défaut pour les autres type de catégories
        check_cat_A = False
        check_cat_D = False
        
    else :
        critere_col4, critere_col5, critere_col6 = st.columns([1, 1, 1])
        with critere_col4 :
            check_cat_A = st.checkbox("Catégorie A : Travail en pression diamétrale")
        with critere_col5 :
            check_cat_D = st.checkbox("Catégorie D : Attaches tendues par boulons non précontraints")
            
        if check_cat_A and check_cat_D :
            check_combine = True
        else :
            check_combine = False
        # On met une valeur False apr défaut pour les autres type de catégories
        check_cat_B = False
        check_cat_C = False
        check_cat_E = False
    
    if check_cat_A or check_cat_B or check_cat_C :
        # saut de ligne
        st.write("\n")
        st.write("Préciser la localisation du ou des plans de cisaillements.")
        plan_cisaillement_col1, plan_cisaillement_col2 = st.columns([1, 1])
        with plan_cisaillement_col1 :
            plan_cisaill_fut_lisse_check = st.checkbox("Plan de cisaillement dans le fût lisse")
        with plan_cisaillement_col2 :
            plan_cisaill_filet_check = st.checkbox("Plan de cisaillement dans les filets", value = True)
        
        # st.image("Pictures/definition_plan_cisaillement.PNG", use_column_width=True, caption="Définition du ou des plans de cisaillement")
            
        if plan_cisaill_fut_lisse_check and plan_cisaill_filet_check == False :
            plan_cisaillement = "fut lisse"
        elif plan_cisaill_fut_lisse_check and plan_cisaill_filet_check :
            plan_cisaillement = "filet"
        else :
            plan_cisaillement = "filet"
        
            

    # saut de ligne
    st.write("\n")
    
    # saut de ligne
    st.write("\n")




    # =======================================
    # Calculs
    # =======================================

    Result_Cat_A = [["N° Boulon", "Nom du critère", "Effort de calcul [N]", "Effort de résistance [N]", "Marge [%]"]]
    Result_Cat_B = [["N° Boulon", "Nom du critère", "Effort de calcul [N]", "Effort de résistance [N]", "Marge [%]"]]
    Result_Cat_C = [["N° Boulon", "Nom du critère", "Effort de calcul [N]", "Effort de résistance [N]", "Marge [%]"]]
    Result_Cat_D = [["N° Boulon", "Nom du critère", "Effort de calcul [N]", "Effort de résistance [N]", "Marge [%]"]]
    Result_Cat_E = [["N° Boulon", "Nom du critère", "Effort de calcul [N]", "Effort de résistance [N]", "Marge [%]"]]
    Result_Cat_Combine = [["N° Boulon", "Nom du critère", "Effort de calcul [N]", "Effort de résistance [N]", "Marge [%]"]]

    # On parcourt l'ensemble des valeurs des efforts
    for i in range(1, len(torseur_effort_full)) :

        position = torseur_effort_full[i][1]
        FtEd = float(torseur_effort_full[i][2])
        FvxEd = float(torseur_effort_full[i][3])
        FvyEd = float(torseur_effort_full[i][4])
        
        if check_preload :
            FtEdp = float(torseur_effort_full[i][6])
            # st.write("FtEdp = " + str(FtEdp))
                     
        FvEd = (FvxEd**2 + FvyEd**2)**(0.5)

        # st.write("FtEd = " + str(FtEd))
        # st.write("FvxEd = " + str(FvxEd))
        # st.write("FvyEd = " + str(FvyEd))
        # st.write("FvEd = " + str(FvEd))
        
        
        ###############
        # Catégorie A #
        ###############
    
        if check_cat_A :
            
            # Résistance au cisaillement 
            
            if type_boulonnerie == "Rivet" :
                A = As
                alpha_v = 0.6
                
            else :
                if plan_cisaillement == "filet" :
                    A = As
                    if classe == "4.6" or classe == "5.6" or classe == "8.8" :
                        alpha_v = 0.6
                    else :
                        alpha_v = 0.5
                else :
                    A = S
                    alpha_v = 0.6

            # st.write("alpha_v = " + str(alpha_v))
            # st.write("A = " + str(A))
                
            FvRd = alpha_v*fub*A/GammaM2

            if tp > d/3 :
                Betap = 9*d/(8*d+3*tp)
                # st.write("Betap = " + str(Betap))
                
                FvRd = Betap*FvRd
                
            # Si c'est un assemblage long, on applique un coefficient supplémentaire
            if check_assemblage_long :
                BetaLf = 1 - (Lj - 15*d)/(200*d)
                if BetaLf <= 0.75 :
                    BetaLf = 0.75
                FvRd = BetaLf*FvRd

            marge = round(calculer_marge(FvEd, FvRd), 2)

            Result_Cat_A.append(["Boulon n°" + str(i), "Résistance au cisaillement", round(FvEd,2), round(FvRd, 2), marge])



            

            # Résistance à la pression diamétrale
            
            # Si ce n'est pas un boulon injecté (avec résine)
            if not resine_check :
                # S'il s'agit d'un boulon à tête fraisée, on modifie la valeur de t
                if tete_fraisee_check :
                    t = tp - pf/2
                
                # Pour les boulons intérieurs
                if position == "Intérieure" :
                    alpha_d = (p1/(3*d0)) - 1/4
                    alpha_b = min(alpha_d, float(fub)/float(fu), 1)
                    k1 = min((1.4*p2/d0 - 1.7), 2.5)
    
                # Pour les boulons de rive
                else :
                    alpha_d = e1/(3*d0)
                    alpha_b = min(alpha_d, float(fub)/float(fu), 1)
                    k1 = min((2.8*e2/d0 - 1.7), (1.4*p2/d0 - 1.7), 2.5)

                # st.write("alpha_d = " + str(alpha_d))
                # st.write("alpha_b = " + str(alpha_b))
                # st.write("k1 = " + str(k1))
                FbRd = kb*k1*alpha_b*fu*d*t/GammaM2

            # Si c'est un boulon injecté (avec résine)
            else :
                Beta = 1.0 # Valeur par défaut
                FbRd = kb*1.2*ksresine*d*tb_resine*Beta*fbresine/GammaM4

            marge = round(calculer_marge(FvEd, FbRd), 2)
            Result_Cat_A.append(["Boulon n°" + str(i), "Résistance à la pression diamétrale", round(FvEd,2), round(FbRd, 2), marge])

        
        ###############
        # Catégorie B #
        ###############
    
        if check_cat_B :
            st.write("Catégorie B")
            # Résistance au cisaillement 

            if type_boulonnerie == "Rivet" :
                A = As
                alpha_v = 0.6
                
            else :
                if plan_cisaillement == "filet" :
                    A = As
                    if classe == "4.6" or classe == "5.6" or classe == "8.8" :
                        alpha_v = 0.6
                    else :
                        alpha_v = 0.5
                else :
                    A = S
                    alpha_v = 0.6
                
            FvRd = alpha_v*fub*A/GammaM2

            if tp > d/3 :
                Betap = 9*d/(8*d+3*tp)
                FvRd = Betap*FvRd
                
            # Si c'est un assemblage long, on applique un coefficient supplémentaire
            if check_assemblage_long :
                BetaLf = 1 - (Lj - 15*d)/(200*d)
                if BetaLf <= 0.75 :
                    BetaLf = 0.75
                FvRd = BetaLf*FvRd

            marge = round(calculer_marge(FvEd, FvRd), 2)

            Result_Cat_B.append(["Boulon n°" + str(i), "Résistance au cisaillement", round(FvEd,2), round(FvRd, 2), marge])


            # Résistance à la pression diamétrale
            
            # Si ce n'est pas un boulon injecté (avec résine)
            if not resine_check :
                # S'il s'agit d'un boulon à tête fraisée, on modifie la valeur de t
                if tete_fraisee_check :
                    t = tp - pf/2
                
                # Pour les boulons intérieurs
                if position == "Intérieure" :
                    alpha_d = (p1/(3*d0)) - 1/4
                    alpha_b = min(alpha_d, float(fub)/float(fu), 1)
                    k1 = min((1.4*p2/d0 - 1.7), 2.5)
    
                # Pour les boulons de rive
                else :
                    alpha_d = e1/(3*d0)
                    alpha_b = min(alpha_d, float(fub)/float(fu), 1)
                    k1 = min((2.8*e2/d0 - 1.7), (1.4*p2/d0 - 1.7), 2.5)
    
                FbRd = kb*k1*alpha_b*fu*d*t/GammaM2

            # Si c'est un boulon injecté (avec résine)
            else :
                Beta = 1 # Valeur par défaut
                FbRd = kb*1.2*ksresine*d*tb_resine*Beta*fbresine/GammaM4

            marge = round(calculer_marge(FvEd, FbRd), 2)
            Result_Cat_B.append(["Boulon n°" + str(i), "Résistance à la pression diamétrale", round(FvEd,2), round(FbRd, 2), marge])



            # Résistance au glissement à l'ELS
            
            FpC = 0.7*fub*As
            st.write(FpC)
            # Si il y a des efforts combinés
            if check_combine :
                FsRdser = ksp*n*mu*(FpC - 0.8*FtEd)/GammaM3ser
            else : 
                FsRdser = ksp*n*mu*FpC/GammaM3ser
            
            # Si c'est un boulon injecté
            if resine_check :
                Beta = 1.0 # Valeur par défaut
                FbRdresine = ksresine*d*tbresine*Beta*fbresine/GammaM4
                FsRd = FbRdresine + FsRdser
            else :
                FsRd = FsRdser

            marge = round(calculer_marge(FvEd, FsRd), 2)
            Result_Cat_B.append(["Boulon n°" + str(i), "Résistance au glissement à l'ELS", round(FvEd,2), round(FsRd, 2), marge])



        
        
        ###############
        # Catégorie C #
        ###############
    
        if check_cat_C :
            st.write("Catégorie C")

            # Résistance à la pression diamétrale
            
            # Si ce n'est pas un boulon injecté (avec résine)
            if not resine_check :
                # S'il s'agit d'un boulon à tête fraisée, on modifie la valeur de t
                if tete_fraisee_check :
                    t = tp - pf/2
                
                # Pour les boulons intérieurs
                if position == "Intérieure" :
                    alpha_d = (p1/(3*d0)) - 1/4
                    alpha_b = min(alpha_d, float(fub)/float(fu), 1)
                    k1 = min((1.4*p2/d0 - 1.7), 2.5)
    
                # Pour les boulons de rive
                else :
                    alpha_d = e1/(3*d0)
                    alpha_b = min(alpha_d, float(fub)/float(fu), 1)
                    k1 = min((2.8*e2/d0 - 1.7), (1.4*p2/d0 - 1.7), 2.5)
    
                FbRd = kb*k1*alpha_b*fu*d*t/GammaM2

            # Si c'est un boulon injecté (avec résine)
            else :
                Beta = 1 # Valeur par défaut
                FbRd = kb*1.2*ksresine*d*tb_resine*Beta*fbresine/GammaM4

            marge = round(calculer_marge(FvEd, FbRd), 2)
            Result_Cat_C.append(["Boulon n°" + str(i), "Résistance à la pression diamétrale", round(FvEd,2), round(FbRd, 2), marge])



            # Résistance au glissement à l'ELU
            
            FpC = 0.7*fub*As
            # Si il y a des efforts combinés
            if check_combine :
                FsRdser = ksp*n*mu*(FpC - 0.8*FtEd)/GammaM3ser
            else : 
                FsRdser = ksp*n*mu*FpC/GammaM3ser

            # Si c'est un boulon injecté
            if resine_check :
                Beta = 1.0 # Valeur par défaut
                FbRdresine = 1.2*ksresine*d*tbresine*Beta*fbresine/GammaM4
                FsRd = FbRdresine + FsRdser
            else :
                FsRd = FsRdser

            marge = round(calculer_marge(FvEd, FsRd), 2)
            Result_Cat_C.append(["Boulon n°" + str(i), "Résistance au glissement à l'ELU", round(FvEd,2), round(FsRd, 2), marge])
            
            





        

        ###############
        # Catégorie D #
        ###############
    
        if check_cat_D :
            st.write("Catégorie D")
            # Résistance à la traction 

            if tete_fraisee_check :
                k2 = 0.63
            else :
                k2 = 0.9

            FtRd = k2*fub*As/GammaM2
            marge = round(calculer_marge(FtEd, FtRd), 2)
            Result_Cat_D.append(["Boulon n°" + str(i), "Résistance à la traction", round(FtEd,2), round(FtRd, 2), marge])



            # Résistance au poinçonnement

            # Si ce n'est pas un boulon, on ne vérifie pas le critère de résistance au poinçonnement
            if type_boulonnerie == "Boulon" :
                BpRd = 0.6*np.pi*dm*tp*fu/GammaM2
                marge = round(calculer_marge(FtEd, BpRd), 2)
                Result_Cat_D.append(["Boulon n°" + str(i), "Résistance au poinçonnement", round(FtEd,2), round(BpRd, 2), marge])




        
    
        ###############
        # Catégorie E #
        ###############
    
        if check_cat_E :
            st.write("Catégorie E")
            # Résistance à la traction 

            if tete_fraisee_check :
                k2 = 0.63
            else :
                k2 = 0.9

            FtRd = k2*fub*As/GammaM2
            marge = round(calculer_marge(FtEdp, FtRd), 2)
            Result_Cat_E.append(["Boulon n°" + str(i), "Résistance à la traction", round(FtEdp,2), round(FtRd, 2), marge])



            # Résistance au poinçonnement

            # Si ce n'est pas un boulon, on ne vérifie pas le critère de résistance au poinçonnement
            if type_boulonnerie == "Boulon" :
                BpRd = 0.6*np.pi*dm*tp*fu/GammaM2
                marge = round(calculer_marge(FtEdp, BpRd), 2)
                Result_Cat_E.append(["Boulon n°" + str(i), "Résistance au poinçonnement", round(FtEdp,2), round(BpRd, 2), marge])




        
            
        ######################
        # Catégorie Combinés #
        ######################
        
        if check_combine :
            st.write("Catégorie Combinés")
            if check_preload :
                effort = FvEd/FvRd + FtEdp/(1.4*FtRd)
                marge = round(calculer_marge(effort, 1.0), 2)
            else :
                effort = FvEd/FvRd + FtEd/(1.4*FtRd)
                marge = round(calculer_marge(effort, 1.0), 2)
                
            Result_Cat_Combine.append(["Boulon n°" + str(i), "Résistance combinée", round(effort,2), 1.0, marge])
    

    
    
    
    # =======================================
    # Résultats
    # =======================================
    
    st.subheader("Résultats")

    rappel_geom_data_check_box = st.checkbox("Afficher les données géométriques utilisées pour le calcul")
    if rappel_geom_data_check_box :
        st.write(df_bolt_geom_data)

        # saut de ligne
        st.write("\n")
        
        # saut de ligne
        st.write("\n")

    
    if check_cat_A :
        # Convertir la liste de listes en DataFrame
        df_cat_A = pd.DataFrame(Result_Cat_A[1:], columns=Result_Cat_A[0])
        
        # Afficher le DataFrame dans Streamlit
        st.dataframe(df_cat_A)

        # On affiche la légende
        st.caption("Résultats du dimensionnement pour les critères de catégorie A")
        
        # On récupère la marge min
        marge_min_A = trouver_marge_min(Result_Cat_A)

        # saut de ligne
        st.write("\n")
        
        # saut de ligne
        st.write("\n")


    if check_cat_B :
        # Convertir la liste de listes en DataFrame
        df_cat_B = pd.DataFrame(Result_Cat_B[1:], columns=Result_Cat_B[0])
        
        # Afficher le DataFrame dans Streamlit
        st.dataframe(df_cat_B)

        # On affiche la légende
        st.caption("Résultats du dimensionnement pour les critères de catégorie B")
        
        # On récupère la marge min
        marge_min_B = trouver_marge_min(Result_Cat_B)

        # saut de ligne
        st.write("\n")
        
        # saut de ligne
        st.write("\n")
        

    if check_cat_C :
        # Convertir la liste de listes en DataFrame
        df_cat_C = pd.DataFrame(Result_Cat_C[1:], columns=Result_Cat_C[0])
        
        # Afficher le DataFrame dans Streamlit
        st.dataframe(df_cat_C)

        # On affiche la légende
        st.caption("Résultats du dimensionnement pour les critères de catégorie C")
        
        # On récupère la marge min
        marge_min_C = trouver_marge_min(Result_Cat_C)

        # saut de ligne
        st.write("\n")
        
        # saut de ligne
        st.write("\n")
        

    if check_cat_D :
        # Convertir la liste de listes en DataFrame
        df_cat_D = pd.DataFrame(Result_Cat_D[1:], columns=Result_Cat_D[0])
        
        # Afficher le DataFrame dans Streamlit
        st.dataframe(df_cat_D)
        
        # On affiche la légende
        st.caption("Résultats du dimensionnement pour les critères de catégorie D")

        # On récupère la marge min
        marge_min_D = trouver_marge_min(Result_Cat_D)

        # saut de ligne
        st.write("\n")
        
        # saut de ligne
        st.write("\n")
        

    if check_cat_E :
        # Convertir la liste de listes en DataFrame
        df_cat_E = pd.DataFrame(Result_Cat_E[1:], columns=Result_Cat_E[0])
        
        # Afficher le DataFrame dans Streamlit
        st.dataframe(df_cat_E)

        # On affiche la légende
        st.caption("Résultats du dimensionnement pour les critères de catégorie E")
        
        # On récupère la marge min
        marge_min_E = trouver_marge_min(Result_Cat_E)

        # saut de ligne
        st.write("\n")
        
        # saut de ligne
        st.write("\n")
        

    if check_combine :
        # Convertir la liste de listes en DataFrame
        df_cat_Combine = pd.DataFrame(Result_Cat_Combine[1:], columns=Result_Cat_Combine[0])
        
        # Afficher le DataFrame dans Streamlit
        st.dataframe(df_cat_Combine)

        # On affiche la légende
        st.caption("Résultats du dimensionnement pour les critères de cisaillement et traction combinés")

        # On récupère la marge min
        marge_min_combine = trouver_marge_min(Result_Cat_Combine)

        
    # saut de ligne
        st.write("\n")
        
    # saut de ligne
    st.write("\n")

    # On affiche les marges min des différentes catégories
        
    

    # RAPPORT PDF
    # On récupère les données nécessaires
    L_cat = [check_cat_A, check_cat_B, check_cat_C, check_cat_D, check_cat_E, check_combine]
    recouvrement_une_rangee = "oui"
    
    # On crée le rapport pdf
    pdf_buffer = create_pdf_eurocode(type_boulonnerie, d, classe, tete_fraisee_check, resine_check, df_bolt_geom_data, df_bolt_geom_data, recouvrement_une_rangee, plan_cisaillement, df_torseur_full, L_cat, tp , Lj)
    
    
    # Proposer le téléchargement
    file_name = st.text_input("Nom du fichier PDF", placeholder="Rapport.pdf")
    
    if ".pdf" not in file_name :
        file_name = file_name + ".pdf"
        
    st.download_button(
      label="Télécharger le rapport PDF",
      data=pdf_buffer,
      file_name = file_name,
      mime="application/pdf" # utilisé pour spécifier le type de fichier que l'utilisateur peut télécharger. Ici, application/pdf signifie qu'il s'agit d'un document pdf
    )


    





