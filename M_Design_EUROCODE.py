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

def page_EUROCODE() :

    # =========================================================================
    # Variables 
    # =========================================================================

    liste_classe = ["4.6", "4.8", "5.6", "5.8", "6.8", "8.8", "10.9"] 

    # =============================================================================
    # TITRE DE L'APPLICATION ET INTRODUCTION 
    # =============================================================================
    
    st.title("Dimensionnement de la boulonnerie selon l'EUROCODE")
    st.write("En cours de développement...")


    
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
        d = st.text_input("$d [mm]$ :", placeholder = "0.0")
        p = st.text_input("$p [mm]$ :", placeholder = "0.0")
        d0 = st.text_input("$d_0 [mm]$ :", placeholder = "0.0")

    with bolt_goem_data_col2 :
        st.write("Type de trou")
        type_trou = st.radio("", ("Normal", "Surdimensionné", "Oblong"), label_visibility="collapsed")

    if type_trou == "Oblong" :
        st.write("Est-ce qu'il s'agit d'un trou oblong court ou long ?")
        type_trou_oblong = st.radio("", ("Court", "Long"), horizontal=True, label_visibility="collapsed")
        st.write("Est-ce que l'axe longitudinal est parallèle ou perpendiculaire aux efforts de cisaillement ? (Voir Figure ci-dessous)")
        axe_longi = st.radio("", ("Parallèle", "Perpendiculaire"), horizontal=True, label_visibility="collapsed")
        st.image("Pictures/def_axe_trou_oblong.PNG", use_column_width=True)
    
    # On met une valeur par défaut aux variables pour ne pas générer de message d'erreur
    d = float(d) if d else 1.0
    p = float(p) if p else 1.0
    d0 = float(d0) if d0 else 1.0

    # On détermine les données intermédiaires
    d1 = d - 1.0825*p             # Diamètre au sommet de l'écrou [mm]
    d2 = d - 0.6495*p             # Diamètre moyen de la vis [mm]
    d3 = d - 1.2268*p             # Diamètre à fond de filet (ou diamètre du noyau), noté aussi dn [mm]
    S = np.pi*d*d/4               # Section du fût
    As = (((d1+d2)/2)**2)*np.pi/4 # Section résistante
    GammaM2 = 1.25                # Coefficient partiel pour la résistance des boulons
    
    if type_trou == "Surdimensionné" :
        C = 0.8                   # Coefficient de trou
    elif type_trou == "Oblong" :
        C = 0.6                   # Coefficient de trou
    else :
        C = 1.0                   # Coefficient de trou
        
    classe_part1 = classe[0] # On récupère le premier digit de la classe de la boulonnerie pour calculer fub
    if classe_part1 == "1" :
        fub = float(classe_part1)*1000 # résistance ultime à la traction
    else :
        fub = float(classe_part1)*100  # résistance ultime à la traction
    

    # On créé un tableau pandas qui servira aussi pour le rapport
    L_Designation = ["Diamètre nominal", "Pas", "Diamètre du trou", "Diamètre en sommet d'écrou", "Diamètre moyen", "Diamètre à fond de filet", "Section résistante à la traction", 
                     "Section brute ou du fût lisse", "Résistance ultime à la traction (à 20°C)", "Coefficient de trou", "Coefficient partiel pour la résistance des boulons"]
    L_Symbole = ["d", "p", "d0", "d1", "d2", "d3", "As", "S", "fub", "C", "GammaM2"]
    L_Valeur = [d, p, d0, d1, d2, d3, round(As, 2), round(S, 2), fub, C, GammaM2]
    L_Unite = ["[mm]", "[mm]", "[mm]", "[mm]", "[mm]", "[mm]", "[mm²]", "[mm²]", "[MPa]", "[-]", "[-]"]

    # Création d'un dictionnaire
    D_bolt_geom_data = {
        'Désignation' : L_Designation,
        'Symbole' : L_Symbole,
        'Valeur' : L_Valeur,
        'Unité' : L_Unite
        }
    
    # Création du DataFrame pandas à partir du dictionnaire
    df_bolt_geom_data = pd.DataFrame(D_bolt_geom_data)



    # DONNEES LIEES A L'ASSEMBLAGE #
    ################################

    st.subheader("Données liées à l'assemblage") #Sous-Partie

    st.write("- ##### *Type d'élément de serrage*") #Sous-Partie


