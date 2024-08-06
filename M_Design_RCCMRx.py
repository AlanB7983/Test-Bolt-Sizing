# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 11:34:31 2024

@author: alanb
"""

import streamlit as st
# Ajouter un graphique simple
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import os


from M_Createur_Rapport_PDF import create_pdf_template
from M_Calcul_Contraintes import calculate_sigma_m, calculate_sigma_m_plus_b, calculate_tau_th, calculate_tau_h, calculate_p_th, calculate_p_h, calculate_sigma_N, calculate_sigma_M, calculate_tau_T
from M_Manipulation_Donnees_Materiaux_2 import get_grandeur_T_quelconque, get_donnees_grandeur_fonction_T



def traitement_resultats_Ansys(T_Results_Ansys, check_preload, adherence_selection, F0_selection, selection2, L_Donnees_Geo_Boulonnerie_Full, F0, ft, fv) :    
    
    # L_Donnees_Geo_Boulonnerie_Full = L_Valeur + [d1, d2, d3, D, L_prime, Dm, a_prime, Dp_prime] 
    st.write("T_Results_Ansys", T_Results_Ansys)
    
    # On construit le tableau de résultats Ansys bilan #
    T_Results_Ansys_PL = T_Results_Ansys
    T_Results_Ansys_AL = T_Results_Ansys
    
    #T_Results_Ansys_Bilan = | Nom Boulon | NbPL | NbAL | TbPL | TbAL | MbPL | MbAL | Cr | Ct | F0 |
    T_Results_Ansys_Bilan = []
    
    for i in range(0, len(T_Results_Ansys_PL)) : #On ne prend pas en compte la première ligne d'entete
        ligne = [T_Results_Ansys_PL[i][0],                                         #Nom Boulon
                 float(T_Results_Ansys_PL[i][1]), float(T_Results_Ansys_AL[i][1]), #NbPL, NbAL
                 float(T_Results_Ansys_PL[i][3]), float(T_Results_Ansys_AL[i][3]), #TbPL, TbAL
                 float(T_Results_Ansys_PL[i][4]), float(T_Results_Ansys_AL[i][4]), #MbPL, MbAL
                 0.0, 0.0, 0.0]                                                    #Cr, Ct, F0
        T_Results_Ansys_Bilan.append(ligne)
    
    
    # Si precontraint == True => On ajoute on calcule Cr et Ct et on demande s'il y a adhérence
    
    if check_preload == True :
        #On récupère les données sur la précharge
        p = float(L_Donnees_Geo_Boulonnerie_Full[1])
        Dm = float(L_Donnees_Geo_Boulonnerie_Full[-3])
        d2 = float(L_Donnees_Geo_Boulonnerie_Full[-7])
        
        st.write("p = ", p)
        st.write("Dm = ", Dm)
        st.write("d2 = ", d2)
        st.write("fv = ", fv)
        st.write("ft = ", ft)
        
        #######################################
        # GESTION DE LA REPRISE PAR ADHERENCE #
        #######################################
        
        #mu_contact = 0.25
        

        
        Cr = F0*(0.16*p + 0.583*fv*d2)
        Ct = F0*0.5*ft*Dm
        
        Cr = round(Cr, 2)
        Ct = round(Ct, 2)
         
        
        if adherence_selection == 'tester avec les données saisies' :
            st.write("a venir")
            # #On compare F0 à Ne+Te/µ pour chaque boulon
            # ok_adherence = verif_adherence(T_Results_Ansys_Bilan, F0, mu_contact)
                    
            # if ok_adherence == True :
            #     adherence = 'oui'
            # else :
            #     adherence = 'non'
            
        if adherence_selection == 'oui' :
            #On parcourt le tableau bilan, on ajoute F0 à NbAL, on met T à 0, on ajoute Cr et Ct et F0 dans le tableau
            for i in range(0, len(T_Results_Ansys_Bilan)) :
                if F0_selection == True :
                    T_Results_Ansys_Bilan[i][2] = F0
                T_Results_Ansys_Bilan[i][3] = 0.0
                T_Results_Ansys_Bilan[i][4] = 0.0
                T_Results_Ansys_Bilan[i][7] = Cr
                T_Results_Ansys_Bilan[i][8] = Ct
                T_Results_Ansys_Bilan[i][9] = F0
            
        else :
            #On ajoute seulement la valeur de F0 et de Cr et Ct
            for i in range(0, len(T_Results_Ansys_Bilan)) :
                if F0_selection == True :
                    T_Results_Ansys_Bilan[i][2] = F0
                T_Results_Ansys_Bilan[i][7] = Cr
                T_Results_Ansys_Bilan[i][8] = Ct
                T_Results_Ansys_Bilan[i][9] = F0
        
        
        
    ################################
    # GESTION DU MOMENT DE FLEXION #
    ################################
    
    if selection2 == "non" :
        #On parcourt le tableau bilan, on met M PL et AL à 0
        for i in range(0, len(T_Results_Ansys_Bilan)) :
            T_Results_Ansys_Bilan[i][5] = 0.0
            T_Results_Ansys_Bilan[i][6] = 0.0
        
    return T_Results_Ansys_Bilan





def calculer_contraintes(T_Results_Ansys_Bilan_i, L_Donnees_Geo_Boulonnerie_Full, e, Study_Case, Sumin_T, Symin_T) :
    #On récupère les données dans des variables
    
    #Efforts
    NbPL = T_Results_Ansys_Bilan_i[1]
    NbAL = T_Results_Ansys_Bilan_i[2]
    TbPL = T_Results_Ansys_Bilan_i[3]
    TbAL = T_Results_Ansys_Bilan_i[4]
    MbPL = T_Results_Ansys_Bilan_i[5]
    MbAL = T_Results_Ansys_Bilan_i[6]
    Cr = T_Results_Ansys_Bilan_i[7]
    Ct = T_Results_Ansys_Bilan_i[8]
    
    #Données géométriques boulonnerie

    #[d, p, dl, ln, a, H, Dp, Le, De, B, C, d1, d2, d3, D, L_prime, Dm, a_prime, Dp_prime] 
    d = L_Donnees_Geo_Boulonnerie_Full[0]
    p = L_Donnees_Geo_Boulonnerie_Full[1]
    H = L_Donnees_Geo_Boulonnerie_Full[5]
    Le = L_Donnees_Geo_Boulonnerie_Full[7]
    dl = L_Donnees_Geo_Boulonnerie_Full[2]
    d1 = L_Donnees_Geo_Boulonnerie_Full[11]
    d2 = L_Donnees_Geo_Boulonnerie_Full[12]
    d3 = L_Donnees_Geo_Boulonnerie_Full[13]
    D = L_Donnees_Geo_Boulonnerie_Full[14]
    L_prime = L_Donnees_Geo_Boulonnerie_Full[15]
    a_prime = L_Donnees_Geo_Boulonnerie_Full[17]
    Dp_prime = L_Donnees_Geo_Boulonnerie_Full[18]
    
    L_Contraintes = []
    
    
    
    ######
    # B1 #
    ######
    
    if Study_Case == "B1_A" or Study_Case == "B1_C" : 
        st.write("calculer_contraintes : Cas B1_A ou B1_C")
        
        nom_contrainte_1 = "Contrainte equivalente fictive moyenne"
        contrainte_1 = calculate_sigma_m(NbPL, TbPL, min(d3, dl))
        nom_contrainte_2 = "Contrainte equivalente moyenne"
        contrainte_2 = calculate_sigma_m(NbAL, TbAL, min(d3, dl))
        nom_contrainte_3 = "Contrainte equivalente maximale"
        contrainte_3 = calculate_sigma_m_plus_b(NbAL, MbAL, TbAL, Cr, min(d3, dl))
        nom_contrainte_4 = "Contrainte de cisaillement fictive dans les filets de la vis"
        contrainte_4 = calculate_tau_th(NbPL, MbPL, d2, L_prime)
        nom_contrainte_5 = "Contrainte de cisaillement fictive dans la tete de la vis"
        contrainte_5 = calculate_tau_h(NbPL, MbPL, 0.0, d1, H)
        nom_contrainte_6 = "Pression de contact fictive sur les filets"
        contrainte_6 = calculate_p_th(NbPL, MbPL, p, d, D, Le)
        nom_contrainte_7 = "Pression de contact fictive sur la tete de la vis"
        contrainte_7 = calculate_p_h(NbPL, MbPL, a_prime, Dp_prime)
        nom_contrainte_8 = "Contrainte de cisaillement dans les filets de la vis"
        contrainte_8 = calculate_tau_th(NbAL, MbAL, d2, L_prime)
        nom_contrainte_9 = "Contrainte de cisaillement dans la tete de la vis"
        contrainte_9 = calculate_tau_h(NbAL, MbAL, Ct, d1, H)
        nom_contrainte_10 = "Pression de contact sur les filets"
        contrainte_10 = calculate_p_th(NbAL, MbAL, p, d, D, Le)
        nom_contrainte_11 = "Pression de contact sur la tete de la vis"
        contrainte_11 = calculate_p_h(NbAL, MbAL, a_prime, Dp_prime)
        
        L_Contraintes.append([nom_contrainte_1, contrainte_1])
        L_Contraintes.append([nom_contrainte_2, contrainte_2])
        L_Contraintes.append([nom_contrainte_3, contrainte_3])
        L_Contraintes.append([nom_contrainte_4, contrainte_4])
        L_Contraintes.append([nom_contrainte_5, contrainte_5])
        L_Contraintes.append([nom_contrainte_6, contrainte_6])
        L_Contraintes.append([nom_contrainte_7, contrainte_7])
        L_Contraintes.append([nom_contrainte_8, contrainte_8])
        L_Contraintes.append([nom_contrainte_9, contrainte_9])
        L_Contraintes.append([nom_contrainte_10, contrainte_10])
        L_Contraintes.append([nom_contrainte_11, contrainte_11])
        
        
    if Study_Case == "B1_D" :
        st.write("calculer_contraintes : Cas B1_D")
        
        nom_contrainte_1 = "Contrainte equivalente moyenne"
        contrainte_1 = calculate_sigma_m(NbAL, TbAL, min(d3, dl))
        nom_contrainte_2 = "Contrainte equivalente maximale"
        contrainte_2 = calculate_sigma_m_plus_b(NbAL, MbAL, TbAL, Cr, min(d3, dl))
        nom_contrainte_3 = "Contrainte de cisaillement dans les filets de la vis"
        contrainte_3 = calculate_tau_th(NbAL, MbAL, d2, L_prime)
        nom_contrainte_4 = "Contrainte de cisaillement dans la tete de la vis"
        contrainte_4 = calculate_tau_h(NbAL, MbAL, Ct, d1, H)
        
        L_Contraintes.append([nom_contrainte_1, contrainte_1])
        L_Contraintes.append([nom_contrainte_2, contrainte_2])
        L_Contraintes.append([nom_contrainte_3, contrainte_3])
        L_Contraintes.append([nom_contrainte_4, contrainte_4])
    
            
    
    
    ######
    # B2 #
    ######
    
    if Study_Case == "B2_A" :
        st.write("calculer_contraintes : Cas B2_A")
        
        nom_contrainte_1 = "Contrainte equivalente moyenne (chargements mecaniques)"
        contrainte_1 = calculate_sigma_m(NbPL, TbPL, min(d3, dl))
        nom_contrainte_2 = "Contrainte equivalente moyenne"
        contrainte_2 = calculate_sigma_m(NbAL, TbAL, min(d3, dl))
        nom_contrainte_3 = "Contrainte equivalente maximale"
        contrainte_3 = calculate_sigma_m_plus_b(NbAL, MbAL, TbAL, Cr, min(d3, dl))
        nom_contrainte_4 = "Contrainte de cisaillement dans les filets de la vis (chargements mecaniques)"
        contrainte_4 = calculate_tau_th(NbPL, MbPL, d2, L_prime)
        nom_contrainte_5 = "Contrainte de cisaillement dans la tete de la vis (chargements mecaniques)"
        contrainte_5 = calculate_tau_h(NbPL, MbPL, 0.0, d1, H)
        nom_contrainte_6 = "Contrainte de cisaillement dans les filets de la vis"
        contrainte_6 = calculate_tau_th(NbAL, MbAL, d2, L_prime)
        nom_contrainte_7 = "Contrainte de cisaillement dans la tete de la vis"
        contrainte_7 = calculate_tau_h(NbAL, MbAL, Ct, d1, H)
        nom_contrainte_8 = "Pression de contact sur la tete de la vis"
        contrainte_8 = calculate_p_h(NbAL, MbAL, a_prime, Dp_prime)
        
        L_Contraintes.append([nom_contrainte_1, contrainte_1])
        L_Contraintes.append([nom_contrainte_2, contrainte_2])
        L_Contraintes.append([nom_contrainte_3, contrainte_3])
        L_Contraintes.append([nom_contrainte_4, contrainte_4])
        L_Contraintes.append([nom_contrainte_5, contrainte_5])
        L_Contraintes.append([nom_contrainte_6, contrainte_6])
        L_Contraintes.append([nom_contrainte_7, contrainte_7])
        L_Contraintes.append([nom_contrainte_8, contrainte_8])
        
        
    if Study_Case == "B2_C" :
        st.write("calculer_contraintes : Cas B2_C")
        
        #Resistance Normale
        if Sumin_T < 700 :
            st.write("Résistance Normale")
            
            nom_contrainte_1 = "Contrainte equivalente moyenne (chargements mecaniques)"
            contrainte_1 = calculate_sigma_m(NbPL, TbPL, min(d3, dl))
            nom_contrainte_2 = "Contrainte equivalente maximale (chargements mecaniques"
            contrainte_2 = calculate_sigma_m_plus_b(NbPL, MbPL, TbPL, 0.0, min(d3, dl))
            
            L_Contraintes.append([nom_contrainte_1, contrainte_1])
            L_Contraintes.append([nom_contrainte_2, contrainte_2])
            
        #Haute Résistance
        else :
            st.write("Haute Résistance")
            
            nom_contrainte_1 = "Contrainte equivalente moyenne (chargements mecaniques)"
            contrainte_1 = calculate_sigma_m(NbPL, TbPL, min(d3, dl))
            nom_contrainte_2 = "Contrainte equivalente moyenne"
            contrainte_2 = calculate_sigma_m(NbAL, TbAL, min(d3, dl))
            nom_contrainte_3 = "Contrainte equivalente maximale"
            contrainte_3 = calculate_sigma_m_plus_b(NbAL, MbAL, TbAL, Cr, min(d3, dl))
            nom_contrainte_4 = "Contrainte de cisaillement dans les filets de la vis (chargements mecaniques)"
            contrainte_4 = calculate_tau_th(NbPL, MbPL, d2, L_prime)
            nom_contrainte_5 = "Contrainte de cisaillement dans la tete de la vis (chargements mecaniques)"
            contrainte_5 = calculate_tau_h(NbPL, MbPL, 0.0, d1, H)
            nom_contrainte_6 = "Contrainte de cisaillement dans les filets de la vis"
            contrainte_6 = calculate_tau_th(NbAL, MbAL, d2, L_prime)
            nom_contrainte_7 = "Contrainte de cisaillement dans la tete de la vis"
            contrainte_7 = calculate_tau_h(NbAL, MbAL, Ct, d1, H)
            nom_contrainte_8 = "Pression de contact sur la tete de la vis"
            contrainte_8 = calculate_p_h(NbAL, MbAL, a_prime, Dp_prime)
            
            L_Contraintes.append([nom_contrainte_1, contrainte_1])
            L_Contraintes.append([nom_contrainte_2, contrainte_2])
            L_Contraintes.append([nom_contrainte_3, contrainte_3])
            L_Contraintes.append([nom_contrainte_4, contrainte_4])
            L_Contraintes.append([nom_contrainte_5, contrainte_5])
            L_Contraintes.append([nom_contrainte_6, contrainte_6])
            L_Contraintes.append([nom_contrainte_7, contrainte_7])
            L_Contraintes.append([nom_contrainte_8, contrainte_8])
    
    
    if Study_Case == "B2_D" :
        st.write("calculer_contraintes : Cas B2_D")
        
        nom_contrainte_1 = "Contrainte equivalente moyenne (chargements mecaniques)"
        contrainte_1 = calculate_sigma_m(NbPL, TbPL, min(d3, dl))
        nom_contrainte_2 = "Contrainte equivalente maximale (chargements mecaniques"
        contrainte_2 = calculate_sigma_m_plus_b(NbPL, MbPL, TbPL, 0.0, min(d3, dl))
        
        L_Contraintes.append([nom_contrainte_1, contrainte_1])
        L_Contraintes.append([nom_contrainte_2, contrainte_2])
    
    
    
    ######
    # B3 #
    ######
    
    if Study_Case == "B3_A" :
        st.write("calculer_contraintes : Cas B3_A")
        
        acier_aust = True # A compléter
        
        nom_contrainte_1 = "Contrainte due aux efforts de traction"
        contrainte_1 = calculate_sigma_N(NbAL, d3)
        nom_contrainte_2 = "Contrainte de cisaillement"
        contrainte_2 = calculate_tau_T(TbAL, d3)
        
        nom_contrainte_3 = "Sollicitations traction + cisaillement combinees"
        if acier_aust == True :
            critere_1 = 0.3*Sumin_T
            critere_2 = Sumin_T/8
        else :
            critere_1 = 0.5*Sumin_T
            critere_2 = 5*Sumin_T/24
        contrainte_3 = (contrainte_1**2)/(critere_1**2) + (contrainte_2**2)/(critere_2**2)
        
        nom_contrainte_4 = "Pression laterale"
        contrainte_4 = TbAL/(e*d)
        
        L_Contraintes.append([nom_contrainte_1, contrainte_1])
        L_Contraintes.append([nom_contrainte_2, contrainte_2])
        L_Contraintes.append([nom_contrainte_3, contrainte_3])
        L_Contraintes.append([nom_contrainte_4, contrainte_4])
        
        
    if Study_Case == "B3_C" :
        st.write("calculer_contraintes : Cas B3_C")
        
        nom_contrainte_1 = "Contrainte due aux efforts de traction"
        contrainte_1 = calculate_sigma_N(NbAL, d3)
        nom_contrainte_2 = "Contrainte de cisaillement"
        contrainte_2 = calculate_tau_T(TbAL, d3)
        
        nom_contrainte_3 = "Sollicitations traction + cisaillement combinees"
        if acier_aust == False :
            critere_1 = min(1.25*0.5*Sumin_T, Symin_T)
            critere_2 = min(1.25*5*Sumin_T/24, Symin_T)
        
        else :
            critere_1 = min(1.25*0.3*Sumin_T, Symin_T)
            critere_2 = min(1.25*Sumin_T/8, Symin_T)
        contrainte_3 = (contrainte_1**2)/(critere_1**2) + (contrainte_2**2)/(critere_2**2)
        
        nom_contrainte_4 = "Pression laterale"
        contrainte_4 = TbAL/(e*d)
        
        L_Contraintes.append([nom_contrainte_1, contrainte_1])
        L_Contraintes.append([nom_contrainte_2, contrainte_2])
        L_Contraintes.append([nom_contrainte_3, contrainte_3])
        L_Contraintes.append([nom_contrainte_4, contrainte_4])
        
        
    if Study_Case == "B3_D" :
        st.write("calculer_contraintes : Cas B3_D")
        
        nom_contrainte_1 = "Contrainte due aux efforts de traction"
        contrainte_1 = calculate_sigma_N(NbAL, d3)
        nom_contrainte_2 = "Contrainte de cisaillement"
        contrainte_2 = calculate_tau_T(TbAL, d3)
        
        nom_contrainte_3 = "Sollicitations traction + cisaillement combinees"
        if acier_aust == True :
            critere_1 = 0.3*Sumin_T
            critere_2 = Sumin_T/8
        else :
            critere_1 = 0.5*Sumin_T
            critere_2 = 5*Sumin_T/24
        contrainte_3 = (contrainte_1**2)/(critere_1**2) + (contrainte_2**2)/(critere_2**2)
        
        L_Contraintes.append([nom_contrainte_1, contrainte_1])
        L_Contraintes.append([nom_contrainte_2, contrainte_2])
        L_Contraintes.append([nom_contrainte_3, contrainte_3])
        
        if Sumin_T > 700 :
            nom_contrainte_4 = "Contrainte due aux efforts de traction et aux moments de flexion"
            contrainte_4 = calculate_sigma_N(NbAL, d3) + calculate_sigma_M(MbAL, d3)
            
            L_Contraintes.append([nom_contrainte_4, contrainte_4])
    
    return L_Contraintes





def calculer_criteres(d, Symin_T, Sumin_T, Sm_T, SmB_T, Study_Case, L) :
    
    L_Criteres = []


    ######
    # B1 #
    ######
    
    if Study_Case == "B1_A" or Study_Case == "B1_C" : 
        st.write("calculer_criteres : Cas B1_A ou B1_C")
        critere_1 = SmB_T
        critere_2 = 2*SmB_T
        critere_3 = 3*SmB_T
        critere_4 = min(0.6*SmB_T, 0.3*Sm_T)
        critere_5 = 0.6*SmB_T
        critere_6 = 0.5*Symin_T
        critere_7 = 0.5*Symin_T
        critere_8 = min(1.2*SmB_T, 0.6*Sm_T)
        critere_9 = 1.2*SmB_T
        critere_10 = Symin_T
        critere_11 = Symin_T
        
        L_Criteres = [critere_1, critere_2, critere_3, critere_4, critere_5, critere_6, critere_7, critere_8, critere_9, critere_10, critere_11]
    
    if Study_Case == "B1_D" : 
        st.write("calculer_criteres : Cas B1_D")
        critere_1 = min(Symin_T, 0.7*Sumin_T)
        critere_2 = Sumin_T
        critere_3 = min(0.6*Symin_T, 0.42*Sumin_T)
        critere_4 = min(0.6*Symin_T, 0.42*Sumin_T)
        
        L_Criteres = [critere_1, critere_2, critere_3, critere_4]


    
    ######
    # B2 #
    ######
    
    if Study_Case == "B2_A" : 
        st.write("calculer_criteres : Cas B2_A")
        critere_1 = SmB_T
        critere_2 = min(0.9*Symin_T, 0.67*Sumin_T)
        critere_3 = 1.33*min(0.9*Symin_T, 0.67*Sumin_T)
        critere_4 = 0.6*SmB_T
        critere_5 = 0.6*SmB_T
        critere_6 = 0.6*Symin_T
        critere_7 = 0.6*Symin_T
        critere_8 = 2.7*Symin_T
        
        L_Criteres = [critere_1, critere_2, critere_3, critere_4, critere_5, critere_6, critere_7, critere_8]
            
    if Study_Case == "B2_C" : 
        st.write("calculer_criteres : Cas B2_C")
        #Resistance Normale
        if Sumin_T < 700 :
            critere_1 = 1.5*SmB_T
            critere_2 = 2.25*SmB_T
            
            L_Criteres = [critere_1, critere_2]
        
        #Haute Résistance
        else :
            critere_1 = SmB_T
            critere_2 = min(0.9*Symin_T, 0.67*Sumin_T)
            critere_3 = 1.33*min(0.9*Symin_T, 0.67*Sumin_T)
            critere_4 = 0.6*SmB_T
            critere_5 = 0.6*SmB_T
            critere_6 = 0.6*Symin_T
            critere_7 = 0.6*Symin_T
            critere_8 = 2.7*Symin_T
            
            L_Criteres = [critere_1, critere_2, critere_3, critere_4, critere_5, critere_6, critere_7, critere_8]
    
    if Study_Case == "B2_D" : 
        st.write("calculer_criteres : Cas B2_D")
        #Resistance Normale
        if Sumin_T < 700 :
            critere_1 = min(2.4*SmB_T, 0.7*Sumin_T)
            critere_2 = 1.5*min(2.4*SmB_T, 0.7*Sumin_T)
            
            L_Criteres = [critere_1, critere_2]
        
        #Haute Résistance
        else :
            critere_1 = 2*SmB_T
            critere_2 = 3*SmB_T
            
            L_Criteres = [critere_1, critere_2]
    
    
    
    ######
    # B3 #
    ######
    
    if Study_Case == "B3_A" : 
        st.write("calculer_criteres : Cas B3_A")
        
        acier_aust = True
        

        if acier_aust == False :
            critere_1 = 0.5*Sumin_T
            critere_2 = 5*Sumin_T/24
        
        else :
            critere_1 = 0.3*Sumin_T
            critere_2 = Sumin_T/8
        
        critere_3 = 1
        critere_4 = min(L*Sumin_T/(2*d), 1.5*Sumin_T)
    
        L_Criteres = [critere_1, critere_2, critere_3, critere_4]
        
        
    if Study_Case == "B3_C" : 
        st.write("calculer_criteres : Cas B3_C")
        if acier_aust == False :
            critere_1 = min(1.25*0.5*Sumin_T, Symin_T)
            critere_2 = min(1.25*5*Sumin_T/24, Symin_T)
        
        else :
            critere_1 = min(1.25*0.3*Sumin_T, Symin_T)
            critere_2 = min(1.25*Sumin_T/8, Symin_T)
        
        critere_3 = 1
        critere_4 = min(L*Sumin_T/(2*d), 1.5*Sumin_T)
    
        L_Criteres = [critere_1, critere_2, critere_3, critere_4]

    
    if Study_Case == "B3_D" : 
        st.write("calculer_criteres : Cas B3_D")
        critere_1 = min(Symin_T, 0.7*Sumin_T)
        critere_2 = min(0.6*Symin_T, 0.42*Sumin_T)
        critere_3 = 1
        
        L_Criteres = [critere_1, critere_2, critere_3]
                      
        #Haute Normale
        if Sumin_T > 700 :
            critere_4 = Sumin_T
            
            L_Criteres.append(critere_4)
    
    
    return L_Criteres


def calculer_marge(valeur, critere):
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
    
    marge = 100*(critere - valeur)/critere
    
    return marge


def calculer_marges_all_results(L_Contraintes, L_Criteres) :
    L_Bilan_Boulon_i = []
    
    #On ajoute l'entete
    L_Bilan_Boulon_i.append(['Nom de la contrainte', 'Contrainte [MPa]', 'Critere [MPa]', 'Marge [%]'])
    
    
    for i in range(0, len(L_Contraintes)) :
        contrainte = round(L_Contraintes[i][1], 2)
        critere = round(L_Criteres[i], 2)
        marge = calculer_marge(contrainte, critere)
        marge = round(marge, 2)
        
        ligne = [L_Contraintes[i][0], contrainte, critere, marge]
        
        L_Bilan_Boulon_i.append(ligne)
    
    return L_Bilan_Boulon_i


def find_first_zero_index(lst):
    """
    Trouve l'indice du premier zéro dans une liste.

    Parameters:
    lst (list): La liste à parcourir.

    Returns:
    int: L'indice du premier zéro dans la liste ou -1 si aucun zéro n'est trouvé.
    """
    try:
        return lst.index(0)
    except ValueError:
        return -1
    
    
    
def supprimer_retour_ligne(L_Fichier) :
    
    """
    
    Parameters
    ----------
    L_Fichier : TYPE = Liste de liste de str
        L_Fichier = [['toto', 'tata\n], ..., ['titi', 'tutu\n']]

    Returns
    -------
    L_Fichier : TYPE = Liste de liste de str
        L_Fichier = [['toto', 'tata'], ..., ['titi', 'tutu']]

    """
    
    for i in range(0, len(L_Fichier)):
        ch = L_Fichier[i][-1]
        ch = ch[:-1]
        L_Fichier[i][-1] = ch
        
        
def traduire_fichier_to_liste(name) :
    
    """

    Parameters
    ----------
    name : TYPE = str
        Nom du fichier csv séparateur point-virgule dont on veut récupérer les données

    Returns
    -------
    L_Fichier : TYPE = Liste de liste de str
        Liste de liste de chaînes de caractères contenant les données du fichier csv et 
        dont on a enlevé les retours à la ligne '\n'

    """
    
    L_Fichier = []
    f = open(name, 'r')
    for line in f:
        currentline = line.split(";")
        L_Fichier.append(currentline)
    f.close()

    supprimer_retour_ligne(L_Fichier)

    return(L_Fichier)





def page_RCCMRx() :

    # Variables
    liste_material = ["304L SS", "316L SS", "660 SS", "Acier Classe 6-8", "Alloy 718"]
      
    
    # =============================================================================
    # DONNEES D'ENTREE    
    # =============================================================================
    
    st.header("SAISIE DES DONNÉES D'ENTRÉE") # Partie
    
    st.subheader("Type d'élément de serrage") #Sous-Partie
    
    selection = st.radio("", ("Vis", "Boulon", "Goujon", "Lacet"), horizontal=True)
    st.write("") # Saut de ligne
    
    st.subheader("Données géométriques à $T_0$")
    
    st.write("- ##### *Données liées à l'élément de serrage*")
    
    col1, col2, col3 = st.columns([1, 1, 3])
    
    if selection == "Vis" :
        with col1:
            d = st.text_input("$d [mm]$ :", placeholder = "0.0")
            p = st.text_input("$p [mm]$ :", placeholder = "0.0")
            dl = st.text_input("$d_{l} [mm]$ :", placeholder = "0.0")
            ln = st.text_input("$l_{n} [mm]$ :", placeholder = "0.0")
            a = st.text_input("$a [mm]$ :", placeholder = "0.0")
            H = st.text_input("$H [mm]$ :", placeholder = "0.0")
    
    
            
        with col2:
            Dp = st.text_input("$D_p [mm]$ :", placeholder = "0.0")
            De = st.text_input("$D_e [mm]$ :", placeholder = "0.0")
            Le = st.text_input("$L_{e} [mm]$ :", placeholder = "0.0")
            B = st.text_input("$B [mm]$", placeholder = "0.0")
            C = st.text_input("$C [mm]$", placeholder = "0.0")
            
        with col3:
            st.image("Pictures/Vis_Dimensions.png", use_column_width=True)
        
        
        d = float(d)
        p = float(p)
        dl = float(dl)
        ln = float(ln)
        a = float(a)
        H = float(H)
        Dp = float(Dp)
        De = float(De)
        Le = float(Le)
        #lb = ll + ln + Le
        B = float(B)
        C = float(C)
        
        L_Designation = ["Diamètre nominal", "Pas", "Diamètre du fût lisse", "Longueur du filetage non en prise \n avec les pièces assemblées",
                         "Diamètre sur le plat de la tête", "Hauteur de la tête", "Diamètre de perçage", "Longueur d'engagement des filets \n en prise", "Etendue des pièces assemblées autour \n de l'axe de l'élément de serrage",
                         "Diamètre intérieur de la rondelle", "Epaisseur de la rondelle"]
        L_Symbole = ["d", "p", "dl", "ln", "a", "H", "Dp", "Le", "De", "B", "C"]
        L_Valeur = [d, p, dl, ln, a, H, Dp, Le, De, B, C]
        L_Unite = ["[mm]"]*len(L_Valeur)
        
        # Création d'un dictionnaire
        D_bolt_geom_data = {
            'Désignation' : L_Designation,
            'Symbole' : L_Symbole,
            'Valeur' : L_Valeur,
            'Unité' : L_Unite
            }
        
        # Création du DataFrame pandas à partir du dictionnaire
        df_bolt_geom_data = pd.DataFrame(D_bolt_geom_data)
    
        
    elif selection == "Boulon" :
        with col1:
            d = st.text_input("$d [mm]$ :", placeholder = "0.0")
            p = st.text_input("$p [mm]$ :", placeholder = "0.0")
            ln1 = st.text_input("$l_{n1} [mm]$ :", placeholder = "0.0")
            ln2 = st.text_input("$l_{n2} [mm]$ :", placeholder = "0.0")
            De = st.text_input("$D_e [mm]$ :", placeholder = "0.0")
    
    
        with col2: 
            a = st.text_input("$a [mm]$ :", placeholder = "0.0")
            Dp = st.text_input("$D_p [mm]$ :", placeholder = "0.0")
            B = st.text_input("$B [mm]$", placeholder = "0.0")
            C = st.text_input("$C [mm]$", placeholder = "0.0")
    
            
        with col3:
            st.image("Pictures/Boulon_Dimensions.png", use_column_width=True)
        
        d = float(d)
        p = float(p)
        ln1 = float(ln1)
        ln2 = float(ln2)
        a = float(a)
        Dp = float(Dp)
        De = float(De)
        lb = ln1 + ln2
        B = float(B)
        C = float(C)
        
        L_Designation = ["Diamètre nominal", "Pas", "Longueur du filetage non en prise \n avec les pièces assemblées 1", "Longueur du filetage non en prise \n avec les pièces assemblées 2",
                         "Diamètre sur le plat de la tête", "Diamètre de perçage", "Etendue des pièces assemblées autour \n de l'axe de l'élément de serrage",
                         "Diamètre intérieur de la rondelle", "Epaisseur de la rondelle"]
        L_Symbole = ["d", "p", "ln1", "ln2", "a", "Dp", "De", "B", "C"]
        L_Valeur = [d, p, ln1, ln2, a, Dp, De, B, C]
        L_Unite = ["[mm]"]*len(L_Valeur)
        
        # Création d'un dictionnaire
        D_bolt_geom_data = {
            'Désignation' : L_Designation,
            'Symbole' : L_Symbole,
            'Valeur' : L_Valeur,
            'Unité' : L_Unite
            }
        
        # Création du DataFrame pandas à partir du dictionnaire
        df_bolt_geom_data = pd.DataFrame(D_bolt_geom_data)
    
    elif selection == "Goujon" :
        with col1:
            d = st.text_input("$d [mm]$ :", placeholder = "0.0")
            p = st.text_input("$p [mm]$ :", placeholder = "0.0")
            ln1 = st.text_input("$l_{n1} [mm]$ :", placeholder = "0.0")
            ll = st.text_input("$l_{l} [mm]$ :", placeholder = "0.0")
            ln2 = st.text_input("$l_{n2} [mm]$ :", placeholder = "0.0")
            dl = st.text_input("$d_l [mm]$ :", placeholder = "0.0")
    
        with col2: 
            De = st.text_input("$D_e [mm]$ :", placeholder = "0.0")
            a = st.text_input("$a [mm]$ :", placeholder = "0.0")
            Dp = st.text_input("$D_p [mm]$ :", placeholder = "0.0")
            B = st.text_input("$B [mm]$", placeholder = "0.0")
            C = st.text_input("$C [mm]$", placeholder = "0.0")
            
        with col3:
            st.image("Pictures/Goujon_Dimensions.png", use_column_width=True)
        
        d = float(d)
        p = float(p)
        ln1 = float(ln1)
        ll = float(ll)
        ln2 = float(ln2)
        a = float(a)
        Dp = float(Dp)
        De = float(De)
        dl = float(dl)
        B = float(B)
        C = float(C)
        # lb = ln1 + ln2 + ll + Le
        
    
    elif selection == "Lacet" :
        with col1:
            d = st.text_input("$d [mm]$ :", placeholder = "0.0")
            p = st.text_input("$p [mm]$ :", placeholder = "0.0")
            ln1 = st.text_input("$l_{n1} [mm]$ :", placeholder = "0.0")
            ll = st.text_input("$l_{l} [mm]$ :", placeholder = "0.0")
            ln2 = st.text_input("$l_{n2} [mm]$ :", placeholder = "0.0")
            dl = st.text_input("$d_l [mm]$ :", placeholder = "0.0")
    
        with col2: 
            De = st.text_input("$D_e [mm]$ :", placeholder = "0.0")
            a = st.text_input("$a [mm]$ :", placeholder = "0.0")
            Dp = st.text_input("$D_p [mm]$ :", placeholder = "0.0")
            B = st.text_input("$B [mm]$", placeholder = "0.0")
            C = st.text_input("$C [mm]$", placeholder = "0.0")
            
        with col3:
            st.image("Pictures/Lacet_Dimensions.png", use_column_width=True)
        
        d = float(d)
        p = float(p)
        ln1 = float(ln1)
        ll = float(ll)
        ln2 = float(ln2)
        a = float(a)
        Dp = float(Dp)
        De = float(De)
        dl = float(dl)
        B = float(B)
        C = float(C)
    
    
        
    # Calcul des dimensions intermédiaires
    #D'après le paragraphe A6.2400 du RCC-MRx
    d1 = d - 1.0825*p  # Diamètre au sommet de l'écrou [mm]
    d2 = d - 0.6495*p  # Diamètre moyen de la vis [mm]
    d3 = d - 1.2268*p  # Diamètre à fond de filet (ou diamètre du noyau), noté aussi dn [mm]
    D = d - p  # Diamètre intérieur de l'écrou [mm]
    L_prime = Le - p  # Longueur pour le calcul au cisaillement (Lé < Le) [mm]
    
    if B == 0.0 :
        Dm = (2/3)*(a**3 - Dp**3)/(a**2 - Dp**2)
        a_prime = a #Pour le calcul de p_h et p_th
        Dp_prime = Dp #Pour le calcul de p_h et p_th
    else :
        Dm = (2/3)*(a**3 - B**3)/(a**2 - B**2)
        a_prime = a + 2*C #Pour le calcul de p_h et p_th
        Dp_prime = max(Dp, B) #Pour le calcul de p_h et p_th
    
    Dm = round(Dm, 2)    
    
    L_Donnees_Geo_Boulonnerie_Full = L_Valeur + [d1, d2, d3, D, L_prime, Dm, a_prime, Dp_prime] 
    
    
    mat_bolt_col1, mat_bolt_col2 = st.columns([1, 2])
    with mat_bolt_col1 :
        # saut de ligne
        st.write("\n")
        # saut de ligne
        st.write("\n")
    
    
        
        st.write("###### Matériau de l'élément de serrage")
        materiau_bolt = st.selectbox("Matériau de l'élément de serrage : ", liste_material, label_visibility="collapsed")
        # saut de ligne
        st.write("\n")
        st.write("###### Grandeur à afficher")
        bolt_data_to_print = st.selectbox("Grandeur à afficher", ["Module d'Young", "Masse volumique", "Coefficient de dilatation thermique moyen"], label_visibility="collapsed")
        
        Tb = st.text_input("Température de calcul $T_b$, en °C :", placeholder = "0.0")
        Tb = float(Tb)
        
        
        
        # On récupère le fichier des données matériaux du matériau choisi, et on le converti en liste
        F_Bolt_Material_Properties = "Material_Properties/" + materiau_bolt + '.csv'
        L_Bolt_Material_Properties = traduire_fichier_to_liste(F_Bolt_Material_Properties)
        
        
        
        
    with mat_bolt_col2 :    
        if bolt_data_to_print == "Coefficient de dilatation thermique moyen" :
            L_Alpha_m_bolt = get_donnees_grandeur_fonction_T(L_Bolt_Material_Properties, "Alpha_m")
            Unite = "[10-6/K]" # Unité de la grandeur sélectionnée pour l'afficher dans le graphe
            L_T = [] # Liste des températures (abscisse du graphe)
            L_G = [] # Liste des valeurs de la grandeur (ordonnées du graphe)
            
            for i in range (0, len(L_Alpha_m_bolt)) :
                L_T.append(L_Alpha_m_bolt[i][0])
                L_G.append(float(L_Alpha_m_bolt[i][1]))
    
        
        elif bolt_data_to_print == "Module d'Young" :
            L_E_bolt = get_donnees_grandeur_fonction_T(L_Bolt_Material_Properties, "E")
            Unite = "[MPa]" # Unité de la grandeur sélectionnée pour l'afficher dans le graphe
            L_T = [] # Liste des températures (abscisse du graphe)
            L_G = [] # Liste des valeurs de la grandeur (ordonnées du graphe)
            
            for i in range (0, len(L_E_bolt)) :
                L_T.append(L_E_bolt[i][0])
                L_G.append(L_E_bolt[i][1])
            
        # elif materiau_bolt == "Masse volumique" :
        else :
            L_Rho_bolt = get_donnees_grandeur_fonction_T(L_Bolt_Material_Properties, "Rho")
            Unite = "[kg/m3]" # Unité de la grandeur sélectionnée pour l'afficher dans le graphe
            L_T = [] # Liste des températures (abscisse du graphe)
            L_G = [] # Liste des valeurs de la grandeur (ordonnées du graphe)
            
            for i in range (0, len(L_Rho_bolt)) :
                L_T.append(L_Rho_bolt[i][0])
                L_G.append(L_Rho_bolt[i][1])
            
        fig_bolt_material_property = go.Figure()
        fig_bolt_material_property.add_trace(go.Scatter(x=L_T, y=L_G, mode='lines+markers', name=r'$N_b$', line = dict(color = '#C00000', width = 1)))
        
        # Ajouter des noms aux axes
        fig_bolt_material_property.update_layout(
            title = dict(text = "Evolution de la grandeur en fonction de la température", x = 0.5, xanchor = 'center'),
            xaxis=dict(
                title = dict(text = 'T [°C]', font = dict(color = 'black')),
                showline=True,  # Afficher la barre de l'axe X
                linecolor='black',  # Couleur de la barre de l'axe X
                linewidth=1,  # Largeur de la barre de l'axe X
                tickformat=',.0f',
                tickfont=dict(color='black'),
                minor=dict(ticks="outside", ticklen=1, tickcolor='black')
                ),
            yaxis=dict(
                title = dict(text = bolt_data_to_print + " " + Unite, font = dict(color = 'black')),
                showline=True,  # Afficher la barre de l'axe Y
                linecolor='black',  # Couleur de la barre de l'axe Y
                linewidth=1,  # Largeur de la barre de l'axe Y
                tickformat='.1f',
                tickfont=dict(color='black'),
                minor=dict(ticks="outside", ticklen=1, tickcolor='black')
                ), 
        )
        
    
        # Afficher le graphique dans Streamlit
        st.plotly_chart(fig_bolt_material_property, use_container_width=True)
    
    
    
                                                         
    # saut de ligne
    st.write("\n")
    
    
    
    
    
    
    # ===================================
    # Saisie du fichier de résultat Ansys
    # ===================================
    
    # Bouton pour uploader un fichier CSV
    uploaded_file = st.file_uploader("Sélection du fichier de résultat ANSYS au format CSV", type="csv")
    
    if uploaded_file is not None:
        # Lire le fichier CSV
        df = pd.read_csv(uploaded_file, sep = ';')
    
        # Afficher le dataframe
        st.write(df)
        
        # Transformer le DataFrame en une liste de listes
        T_Results_Ansys = df.values.tolist()
    
    else:
        st.write("Veuillez uploader un fichier CSV.")
    
    # Pour afficher un message une fois le fichier lu
    if uploaded_file is not None:
        st.success('Fichier téléchargé et lu avec succès !')
    
    # saut de ligne
    st.write("\n")
    
    # saut de ligne
    st.write("\n")
    
    
    
    
    
    
    # =======================================
    # Saisie de la fonction de la boulonnerie
    # =======================================
    
    fct_bolt_col_1, fct_bolt_col_2 = st.columns([1, 1])
    with fct_bolt_col_1 :
        check_preload = st.checkbox("Boulonnerie précontrainte")
    
    with fct_bolt_col_2 :
        if check_preload :
            check_etancheite = st.checkbox("Fonction d'étanchéité")
      
            
      
        
      
    # ==============================
    # Sélection du niveau de critère
    # ==============================
    
    st.subheader("Niveau critère") #Sous-Partie
    critere_selection = st.radio("", ("A", "C", "D"), horizontal=True, label_visibility="collapsed")
    
    
    
    
    
    # ===================================================================
    # Saisie des données complémentaires en fonction des données d'entrée
    # ===================================================================
    
    # Détermination du cas d'étude
    if check_preload and check_etancheite :
        if critere_selection == "A" :
            Study_Case = "B1_A"
            st.write(Study_Case)
        elif critere_selection == "C" :
            Study_Case = "B1_C"
            st.write(Study_Case)
        elif critere_selection == "D" :
            Study_Case = "B1_D"
            st.write(Study_Case)
            
            
    elif check_preload and not check_etancheite :
        if critere_selection == "A" :
            Study_Case = "B2_A"
            st.write(Study_Case)
        elif critere_selection == "C" :
            Study_Case = "B2_C"
            st.write(Study_Case)
        elif critere_selection == "D" :
            Study_Case = "B2_D"
            st.write(Study_Case)
    
    
    elif not check_preload  :
        if critere_selection == "A" :
            Study_Case = "B3_A"
            st.write(Study_Case)
        elif critere_selection == "C" :
            Study_Case = "B3_C"
            st.write(Study_Case)
        elif critere_selection == "D" :
            Study_Case = "B3_D"
            st.write(Study_Case)
            
            
            
            
    if "B3" in Study_Case :
        st.write("Moments de flexion dus à une flexion locale par effet levier ?")
        selection1 = st.radio("", ("oui", "non"), horizontal=True, label_visibility="collapsed", key="cas 1")
        
        # saut de ligne
        st.write("\n")
        
        st.write("Entraxe ou distance de l'axe des éléments de serrage au bord de la pièce assemblée dans la direction de l'effort.")
        L = st.text_input("$L [mm]$ :", placeholder = "0.0")    
        
        # saut de ligne
        st.write("\n")
        
        st.write("Epaisseur de la pièce.")
        L = st.text_input("$e [mm]$ :", placeholder = "0.0")
        
        # Traitement des résultats Ansys
        # T_Results_Ansys_Bilan = traitement_resultats_Ansys(T_Results_Ansys, check_preload, adherence_selection, F0_selection, selection1, L_Donnees_Geo_Boulonnerie_Full, F0, ft, fv)
        
    
    else :
        st.write("Valeur du coefficient de rigidité")
        Lambda = st.text_input("$\Lambda [-]$ :", placeholder = "0.0")
        
        # saut de ligne
        st.write("\n")
        
        st.write("Valeur du coefficient de frottement sous tête ou sous écrou.")
        ft = st.text_input("$f_t [-]$ :", placeholder = "0.0")  
        ft = float(ft)
        
        # saut de ligne
        st.write("\n")
        
        st.write("Valeur du coefficient de frottement entre filet en prise.")
        fv = st.text_input("$f_v [-]$ :", placeholder = "0.0")
        fv = float(fv)
        
        # saut de ligne
        st.write("\n")
        
        st.write("Valeur de l'effort de précontrainte à la température $T$.")
        F0 = st.text_input("$F_0 [N]$ :", placeholder = "0.0")
        F0 = float(F0)
        
        # saut de ligne
        st.write("\n")
        
        st.write("$F_0$ pris en compte dans les calculs ANSYS ?")
        F0_selection = st.radio("", ("oui", "non"), horizontal=True, key="test")
        
        # saut de ligne
        st.write("\n")
        
        st.write("Efforts extérieurs repris par adhérence ?")
        adherence_selection = st.radio("", ("oui", "non", "tester avec les données saisies"), horizontal=True, label_visibility="collapsed", key="cas test")
        
        # saut de ligne
        st.write("\n")
        
        st.write("Moments de flexion dus à une flexion locale par effet levier ?")
        selection2 = st.radio("", ("oui", "non"), horizontal=True, label_visibility="collapsed", key="cas 2") 
        
    
        # Traitement des résultats Ansys
        T_Results_Ansys_Bilan = traitement_resultats_Ansys(T_Results_Ansys, check_preload, adherence_selection, F0_selection, selection2, L_Donnees_Geo_Boulonnerie_Full, F0, ft, fv)
        
        # On met une valeur arbitraire pour e pour que la fonction calculer_contraintes ait toutes ses données d'entrée
        e = 0.0
        
        # On met une valeur arbitraire pour L pour que la fonction calculer_criteres ait toutes ses données d'entrée
        L = 0.0
    
    # On récupère les propriétés méca 
    
    Sumin_T = float(get_grandeur_T_quelconque('Su.min', L_Bolt_Material_Properties, float(Tb)))
    Symin_T = float(get_grandeur_T_quelconque('Sy.min', L_Bolt_Material_Properties, float(Tb)))
    Sm_T = float(get_grandeur_T_quelconque('Sm', L_Bolt_Material_Properties, float(Tb)))
    SmB_T = float(get_grandeur_T_quelconque('SmB_non_etanche', L_Bolt_Material_Properties, float(Tb)))
    
    # L_Nom_full = []
    # L_contraintes_full = []
    # L_criteres_full = []
    L_marge_full = []
    
    st.write("T_Results_Ansys_Bilan : ", T_Results_Ansys_Bilan)
    for i in range (0, len(T_Results_Ansys_Bilan)) :
        st.write("T_Results_Ansys_Bilan[i] : ", T_Results_Ansys_Bilan[i])
        
        L_contraintes = calculer_contraintes(T_Results_Ansys_Bilan[i], L_Donnees_Geo_Boulonnerie_Full, e, Study_Case, Sumin_T, Symin_T)
        
        L_Criteres = calculer_criteres(d, Symin_T, Sumin_T, Sm_T, SmB_T, Study_Case, L)
        
        L_Bilan_Boulon_i = calculer_marges_all_results(L_contraintes, L_Criteres)
        st.write(L_Bilan_Boulon_i)
        #L_Nom_full.append("Boulon " + str(i+1))
        #L_contraintes_full.append(L_contraintes)
        #L_criteres_full.append(L_Criteres)
        L_marge_full.append(L_Bilan_Boulon_i)
        
    
    # st.write(L_bilan)
    # num_boulon = st.number_input("Numéro du boulo, dont on veut afficher les résultats", 0, int(len(T_Results_Ansys)))
    
    # L_Result_Boulon_i = L_marge_full[0]
    # df_bilan = pd.DataFrame(L_Bilan_Boulon_i)
    # st.write(df_bilan)    
