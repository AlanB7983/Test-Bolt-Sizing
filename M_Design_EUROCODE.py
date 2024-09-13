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



def page_EUROCODE() :

    # =========================================================================
    # Variables 
    # =========================================================================

    liste_classe = ["4.6", "4.8", "5.6", "5.8", "6.8", "8.8", "10.9"] 
    liste_position = ["Intérieure", "Rive"]

    # =============================================================================
    # TITRE DE L'APPLICATION ET INTRODUCTION 
    # =============================================================================
    
    st.title("Dimensionnement de la boulonnerie selon l'EUROCODE")


    
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
        d = st.text_input("Diamètre nominal, $d [mm]$ :", placeholder = "0.0")
        p = st.text_input("Pas, $p [mm]$ :", placeholder = "0.0")
        d0 = st.text_input("Diamètre du perçage, $d_0 [mm]$ :", placeholder = "0.0")

    with bolt_goem_data_col2 :
        st.write("Type de trou")
        type_trou = st.radio("", ("Normal", "Surdimensionné", "Oblong"), label_visibility="collapsed")
    st.write("") # Saut de ligne
    if type_trou == "Oblong" :
        st.write("Est-ce qu'il s'agit d'un trou oblong court ou long ?")
        type_trou_oblong = st.radio("", ("Court", "Long"), horizontal=True, label_visibility="collapsed")
        st.write("Est-ce que l'axe longitudinal est parallèle ou perpendiculaire aux efforts de cisaillement ? (Voir Figure ci-dessous)")
        axe_longi = st.radio("", ("Parallèle", "Perpendiculaire"), horizontal=True, label_visibility="collapsed")
        st.image("Pictures/def_axe_trou_oblong.PNG", use_column_width=True)
        type_trou = type_trou + " " + type_trou_oblong + " " + axe_longi
        st.write("") # Saut de ligne
    st.write("") # Saut de ligne
    
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
        kb = 0.8                   # Coefficient de trou
    elif type_trou == "Oblong" :
        kb = 0.6                   # Coefficient de trou
    else :
        kb = 1.0                   # Coefficient de trou

    if type_trou == "Surdimensionné" or type_trou == "Oblong Court Perpendiculaire" :
        ksp = 0.85
    elif type_trou == "Oblong Long Perpendiculaire" :
        ksp = 0.7
    elif type_trou == "Oblong Court Parallèle" :
        ksp = 0.76
    elif type_trou == "Oblong Long Parallèle" :
        ksp = 0.63
    else :
        ksp = 1.0
        
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
    st.write("Est-ce que les notions d'entraxe longitudinal et d'entraxe transversal, respectivement notées $p_1$ et $p_2$, visibles sur la figure ci-dessous sont définies ?")
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

    st.image("Pictures/definition_donnee_assemblage.PNG", use_column_width=True, caption="Définition des données d'assemblage")
    
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
    with but_col1 :
        indice_boulon = 1
        # Bouton pour ajouter les données au DataFrame
        if st.button('Ajouter', use_container_width = True):
            new_data = pd.DataFrame({'N° Boulon': [indice_boulon], 'Position': [position], 'Effort de traction, Ft,Ed [N]' : [float(FtEd)], 'Effort de cisaillement selon x, Fvx,Ed [N]': [FvxEd], 'Effort de cisaillement selon y, Fvy,Ed [N]' : [FvyEd]})
            st.session_state.efforts_ext = pd.concat([st.session_state.efforts_ext, new_data], ignore_index=True)
            indice_boulon = indice_boulon + 1
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
            st.write("Valeur de l'effort de précontrainte $F_{p,C}$.")
            F0 = st.text_input("$F_{p,C}$ [N] :", placeholder = "0.0")
            F0 = float(F0) if F0 else 0.0
            
            st.write("$F_{p,C}$ pris en compte dans les efforts saisis ?")
            F0_selection = st.radio("", ("oui", "non"), horizontal=True, label_visibility="collapsed", key="test")
    
            if F0_selection == "non" :
                # On demande la valeur de Lambda
                st.write("Valeur du coefficient de rigidité $\Lambda$.")
                Lambda = st.text_input("$\Lambda$ [-] :", placeholder = "0.0")
                Lambda = float(Lambda) if Lambda else 0.0
                st.info("Prendre $\Lambda$ = 0 revient à prendre l'hypothèse d'une liaison infiniment rigide.")
    
                # On ajoute une colonne pour noter F0 dans le tableau et pour écrire Ft,Ed,p
                torseur_effort_full = []
                for index, ligne in enumerate(torseur_effort) :
                    if index == 0 :
                        # Si c'est la première ligne (entête), ajouter le nom des nouvelles colonnes
                        nouvelle_ligne = ligne + ["Effort de précontrainte, Fp,C [N]", "Effort de traction d'origine externe et interne, Ft,Ed,p [N]"]  # Ajout des en-têtes pour les nouvelles colonnes
                    else :
                        # Convertir les valeurs numériques de Col1
                        col2_val = float(ligne[2])
    
                        # Calcul pour la nouvelle colonne Ft,Ed,p 
                        FtEdp = F0 + float(Lambda)*col2_val

                    # Ajouter la nouvelle colonne 6 (F0) et colonne 7 (Ft,Ed,p)
                    nouvelle_ligne = ligne + [str(F0), str(FtEdp)]
                    
                # Ajouter la nouvelle ligne modifiée à la liste finale
                torseur_effort_full.append(nouvelle_ligne)
                    
                    

    else :
        check_preload = False
        torseur_effort_full = torseur_effort

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
            
        
            

    # saut de ligne
    st.write("\n")
    
    # saut de ligne
    st.write("\n")




    # =======================================
    # Calculs
    # =======================================

    Result_Cat_A = [["N° Boulon", "Nom du critère", "Valeur de l'effort de calcul [N]", "Valeur de l'effort de résistance [N]", "Marge [%]"]]
    Result_Cat_B = [["N° Boulon", "Nom du critère", "Valeur de l'effort de calcul [N]", "Valeur de l'effort de résistance [N]", "Marge [%]"]]
    Result_Cat_C = [["N° Boulon", "Nom du critère", "Valeur de l'effort de calcul [N]", "Valeur de l'effort de résistance [N]", "Marge [%]"]]
    Result_Cat_D = [["N° Boulon", "Nom du critère", "Valeur de l'effort de calcul [N]", "Valeur de l'effort de résistance [N]", "Marge [%]"]]
    Result_Cat_E = [["N° Boulon", "Nom du critère", "Valeur de l'effort de calcul [N]", "Valeur de l'effort de résistance [N]", "Marge [%]"]]
    Result_Cat_Combine = [["N° Boulon", "Nom du critère", "Valeur de l'effort de calcul [N]", "Valeur de l'effort de résistance [N]", "Marge [%]"]]
    st.write(Result_Cat_A)

    # On parcourt l'ensemble des valeurs des efforts
    for i in range(1, len(torseur_effort_full)) :

        position = torseur_effort_full[i][1]
        FtEd = float(torseur_effort_full[i][2])
        FvxEd = float(torseur_effort_full[i][3])
        FvyEd = float(torseur_effort_full[i][4])
        
        if check_preload :
            FtEdp = float(torseur_effort_full[i][6])
                     

        ###############
        # Catégorie A #
        ###############
    
        if check_cat_A :
            
            # Résistance au cisaillement 
            FvEd = (FvxEd**2 + FvyEd**2)**(0.5)

            if type_boulonnerie == "Rivet" :
                alpha_v = 0.6
            else :
                if classe == "4.6" or classe == "5.6" or classe == "8.8" :
                    alpha_v = 0.6
                else :
                    alpha_v = 0.5
            FvRd = alpha_v*fub*As/GammaM2

            if tp > d/3 :
                Betap = 9*d/(8*d+3*tp)
                FvRd = Betap*FvRd

            marge = round(calculer_marge(FvEd, FvRd), 2)

            Result_Cat_A.append(["Boulon n°" + str(i), "Résistance au cisaillement", round(FvEd,2), round(FvRd, 2)])


            # Résistance à la pression diamétrale
            # Dans la direction x
            if position == "Intérieure" :
                FbxRd = 4
            else :
                FbxRd = 4

                                
            
            


            
        
    
    

    
    
    
    # =======================================
    # Résultats
    # =======================================
    
    st.subheader("Résultats")




    


    st.write(df_bolt_geom_data)


