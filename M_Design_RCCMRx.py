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


from M_Createur_Rapport_PDF import create_rapport_pdf_rccmrx
from M_Calcul_Contraintes import calculate_sigma_m, calculate_sigma_m_plus_b, calculate_tau_th, calculate_tau_h, calculate_p_th, calculate_p_h, calculate_sigma_N, calculate_sigma_M, calculate_tau_T
from M_Manipulation_Donnees_Materiaux_2 import get_grandeur_T_quelconque, get_donnees_grandeur_fonction_T



def traitement_resultats_Ansys(T_Results_Ansys, check_preload, adherence_selection, F0_selection, selection2, L_Donnees_Geo_Boulonnerie_Full, F0, ft, fv, Lambda) :    
    
    # L_Donnees_Geo_Boulonnerie_Full = L_Valeur + [d1, d2, d3, D, L_prime, Dm, a_prime, Dp_prime] 
    
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
                if F0_selection == "non" :
                    T_Results_Ansys_Bilan[i][2] = Lambda*T_Results_Ansys_Bilan[i][1] + F0
                T_Results_Ansys_Bilan[i][3] = 0.0
                T_Results_Ansys_Bilan[i][4] = 0.0
                T_Results_Ansys_Bilan[i][7] = Cr
                T_Results_Ansys_Bilan[i][8] = Ct
                T_Results_Ansys_Bilan[i][9] = F0
            
        else :
            #On ajoute seulement la valeur de F0 et de Cr et Ct
            for i in range(0, len(T_Results_Ansys_Bilan)) :
                if F0_selection == "non" :
                    T_Results_Ansys_Bilan[i][2] = Lambda*T_Results_Ansys_Bilan[i][1] + F0
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





def calculer_contraintes(T_Results_Ansys_Bilan_i, L_Donnees_Geo_Boulonnerie_Full, e, Study_Case, h, Sumin_T, SyminB_T, SyminP_T, type_boulonnerie, B_acier_aust) :
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

    #[d, p, dl, a, H, Dp, Le, B, C, A, d1, d2, d3, D, L_prime, Dm, a_prime, Dp_prime] 
    d = L_Donnees_Geo_Boulonnerie_Full[0]
    p = L_Donnees_Geo_Boulonnerie_Full[1]
    H = L_Donnees_Geo_Boulonnerie_Full[4]
    Le = L_Donnees_Geo_Boulonnerie_Full[6]
    dl = L_Donnees_Geo_Boulonnerie_Full[2]
    d1 = L_Donnees_Geo_Boulonnerie_Full[10]
    d2 = L_Donnees_Geo_Boulonnerie_Full[11]
    d3 = L_Donnees_Geo_Boulonnerie_Full[12]
    D = L_Donnees_Geo_Boulonnerie_Full[13]
    L_prime = L_Donnees_Geo_Boulonnerie_Full[14]
    a_prime = L_Donnees_Geo_Boulonnerie_Full[16]
    Dp_prime = L_Donnees_Geo_Boulonnerie_Full[17]
    B = L_Donnees_Geo_Boulonnerie_Full[7]
    a = L_Donnees_Geo_Boulonnerie_Full[3]
    Dp = L_Donnees_Geo_Boulonnerie_Full[5]
    
    L_Contraintes = []
    
    if B == 0.0 :
        rondelle = False
    else :
        rondelle = True
    
    ######
    # B1 #
    ######
    
    if Study_Case == "B1_A" or Study_Case == "B1_C" : 
        # st.write("calculer_contraintes : Cas B1_A ou B1_C")
        # st.write("h = ", h)
        # st.write("0.8xd = ", 0.8*d)
        # st.write("h < 0.8*d", h < 0.8*d)
        if h < 0.8*d : # h = 0.0 (ie: pas d'écrou) est compris dans ce cas. Il n'y a pas d'écrou, on vérifie tous les critères
            # st.write("contrainte, cas 1")
            nom_contrainte_1 = "Contrainte équivalente fictive moyenne" #(sigma_m)f
            contrainte_1 = calculate_sigma_m(NbPL, TbPL, min(d3, dl)) 
            nom_contrainte_2 = "Contrainte équivalente moyenne" #sigma_m
            contrainte_2 = calculate_sigma_m(NbAL, TbAL, min(d3, dl))
            nom_contrainte_3 = "Contrainte équivalente maximale" #sigma_m+b
            contrainte_3 = calculate_sigma_m_plus_b(NbAL, MbAL, TbAL, Cr, min(d3, dl))
            nom_contrainte_4 = "Contrainte fictive de cisaillement dans les filets de la vis" #(tau_th_v)f ou (tau_f_v)f
            contrainte_4 = calculate_tau_th(NbPL, MbPL, d2, L_prime)
            if type_boulonnerie == 'Vis' or type_boulonnerie == 'Goujon' :
                nom_contrainte_4bis = "Contrainte fictive de cisaillement dans les filets de la pièce" #(tau_th_p)f ou (tau_f_p)f
                contrainte_4bis = calculate_tau_th(NbPL, MbPL, d2, L_prime)
            nom_contrainte_5 = "Contrainte fictive de cisaillement dans la tête de la vis" #(tau_t)f 
            contrainte_5 = calculate_tau_h(NbPL, MbPL, 0.0, d1, dl, H)
            nom_contrainte_6 = "Pression de contact fictive sur les filets" #(p_th)f ou (p_f)f
            contrainte_6 = calculate_p_th(NbPL, MbPL, p, d, D, Le)
            nom_contrainte_7 = "Pression de contact fictive sur la tête de la vis" # (p_t)f 
            
            if rondelle == False : #S'il n'y a pas de rondelle
                # st.write("contrainte, cas 1.1")
                contrainte_7 = calculate_p_h(NbPL, MbPL, a, Dp) 
            else : #S'il y a une rondelle
                # st.write("contrainte, cas 1.2")
                if SyminP_T > SyminB_T :
                    # st.write("contrainte, cas 1.2.1")
                    contrainte_7 = calculate_p_h(NbPL, MbPL, a, B)
                else :
                    # st.write("contrainte, cas 1.2.2")
                    contrainte_7 = calculate_p_h(NbPL, MbPL, a_prime, Dp_prime)
                
            nom_contrainte_8 = "Contrainte de cisaillement dans les filets de la vis" #tau_th_v ou tau_f_v
            contrainte_8 = calculate_tau_th(NbAL, MbAL, d2, L_prime)
            if type_boulonnerie == 'Vis' or type_boulonnerie == 'Goujon' :
                nom_contrainte_8bis = "Contrainte de cisaillement dans les filets de la pièce" #tau_th_p ou tau_f_p
                contrainte_8bis = calculate_tau_th(NbAL, MbAL, d2, L_prime)
            nom_contrainte_9 = "Contrainte de cisaillement dans la tête de la vis" #tau_t
            contrainte_9 = calculate_tau_h(NbAL, MbAL, Ct, d1, dl, H)
            nom_contrainte_10 = "Pression de contact sur les filets" #p_th ou p_f
            contrainte_10 = calculate_p_th(NbAL, MbAL, p, d, D, Le)
            nom_contrainte_11 = "Pression de contact sur la tête de la vis" #p_t
    
            if rondelle == False : #S'il n'y a pas de rondelle
                # st.write("contrainte, cas 1.3")
                contrainte_11 = calculate_p_h(NbAL, MbAL, a, Dp)
            else : #S'il y a une rondelle
                # st.write("contrainte, cas 1.4")
                if SyminP_T > SyminB_T :
                    # st.write("contrainte, cas 1.4.1")
                    contrainte_11 = calculate_p_h(NbAL, MbAL, a, B)
                else :
                    # st.write("contrainte, cas 1.4.2")
                    contrainte_11 = calculate_p_h(NbAL, MbAL, a_prime, Dp_prime)
                
            L_Contraintes.append([nom_contrainte_1, contrainte_1])
            L_Contraintes.append([nom_contrainte_2, contrainte_2])
            L_Contraintes.append([nom_contrainte_3, contrainte_3])
            L_Contraintes.append([nom_contrainte_4, contrainte_4])
            if type_boulonnerie == 'Vis' or type_boulonnerie == 'Goujon' :
                L_Contraintes.append([nom_contrainte_4bis, contrainte_4bis])
            L_Contraintes.append([nom_contrainte_5, contrainte_5])
            L_Contraintes.append([nom_contrainte_6, contrainte_6])
            L_Contraintes.append([nom_contrainte_7, contrainte_7])
            L_Contraintes.append([nom_contrainte_8, contrainte_8])
            if type_boulonnerie == 'Vis' or type_boulonnerie == 'Goujon' :
                L_Contraintes.append([nom_contrainte_8bis, contrainte_8bis])
            L_Contraintes.append([nom_contrainte_9, contrainte_9])
            L_Contraintes.append([nom_contrainte_10, contrainte_10])
            L_Contraintes.append([nom_contrainte_11, contrainte_11])
        
        else : # h >= 0.8*d
            # st.write("critere, cas 2")
            if type_boulonnerie == 'Boulon' or type_boulonnerie == 'Lacet' :
                # st.write("contraintes, cas 2.1")
                nom_contrainte_1 = "Contrainte équivalente fictive moyenne" #(sigma_m)f
                contrainte_1 = calculate_sigma_m(NbPL, TbPL, min(d3, dl)) 
                nom_contrainte_2 = "Contrainte équivalente moyenne" #sigma_m
                contrainte_2 = calculate_sigma_m(NbAL, TbAL, min(d3, dl))
                nom_contrainte_3 = "Contrainte équivalente maximale" #sigma_m+b
                contrainte_3 = calculate_sigma_m_plus_b(NbAL, MbAL, TbAL, Cr, min(d3, dl))
                
                L_Contraintes.append([nom_contrainte_1, contrainte_1])
                L_Contraintes.append([nom_contrainte_2, contrainte_2])
                L_Contraintes.append([nom_contrainte_3, contrainte_3])
                
            else : # si c'est une vis ou un goujon
                # st.write("contraintes, cas 2.2")
                if SyminP_T < SyminB_T :
                    # st.write("contraintes, cas 2.2.1")
                    nom_contrainte_1 = "Contrainte équivalente fictive moyenne" #(sigma_m)f
                    contrainte_1 = calculate_sigma_m(NbPL, TbPL, min(d3, dl)) 
                    nom_contrainte_2 = "Contrainte équivalente moyenne" #sigma_m
                    contrainte_2 = calculate_sigma_m(NbAL, TbAL, min(d3, dl))
                    nom_contrainte_3 = "Contrainte équivalente maximale" #sigma_m+b
                    contrainte_3 = calculate_sigma_m_plus_b(NbAL, MbAL, TbAL, Cr, min(d3, dl))
                    nom_contrainte_4bis = "Contrainte fictive de cisaillement dans les filets de la pièce" #(tau_th_p)f ou (tau_f_p)f
                    contrainte_4bis = calculate_tau_th(NbPL, MbPL, d2, L_prime)
                    nom_contrainte_8bis = "Contrainte de cisaillement dans les filets de la pièce" #tau_th_p ou tau_f_p
                    contrainte_8bis = calculate_tau_th(NbAL, MbAL, d2, L_prime)
                    
                    L_Contraintes.append([nom_contrainte_1, contrainte_1])
                    L_Contraintes.append([nom_contrainte_2, contrainte_2])
                    L_Contraintes.append([nom_contrainte_3, contrainte_3])
                    L_Contraintes.append([nom_contrainte_4bis, contrainte_4bis])
                    L_Contraintes.append([nom_contrainte_8bis, contrainte_8bis])
                    
                else : # SyminP_T >= SyminB_T
                    # st.write("contraintes, cas 2.2.2")
                    # st.write("Le = ", Le)
                    # st.write("0.8xd = ", 0.8*d)
                    # st.write("Le >= 0.8*d", Le >= 0.8*d)
                    if Le >= 0.8*d :
                        # st.write("contraintes, cas 2.2.2.1")
                        nom_contrainte_1 = "Contrainte équivalente fictive moyenne" #(sigma_m)f
                        contrainte_1 = calculate_sigma_m(NbPL, TbPL, min(d3, dl)) 
                        nom_contrainte_2 = "Contrainte équivalente moyenne" #sigma_m
                        contrainte_2 = calculate_sigma_m(NbAL, TbAL, min(d3, dl))
                        nom_contrainte_3 = "Contrainte équivalente maximale" #sigma_m+b
                        contrainte_3 = calculate_sigma_m_plus_b(NbAL, MbAL, TbAL, Cr, min(d3, dl))
                        
                        L_Contraintes.append([nom_contrainte_1, contrainte_1])
                        L_Contraintes.append([nom_contrainte_2, contrainte_2])
                        L_Contraintes.append([nom_contrainte_3, contrainte_3])
                        
                    else : # Le < 0.8*d
                        # st.write("contraintes, cas 2.2.2.2")
                        nom_contrainte_1 = "Contrainte équivalente fictive moyenne" #(sigma_m)f
                        contrainte_1 = calculate_sigma_m(NbPL, TbPL, min(d3, dl)) 
                        nom_contrainte_2 = "Contrainte équivalente moyenne" #sigma_m
                        contrainte_2 = calculate_sigma_m(NbAL, TbAL, min(d3, dl))
                        nom_contrainte_3 = "Contrainte équivalente maximale" #sigma_m+b
                        contrainte_3 = calculate_sigma_m_plus_b(NbAL, MbAL, TbAL, Cr, min(d3, dl))
                        nom_contrainte_4 = "Contrainte fictive de cisaillement dans les filets de la vis" #(tau_th_v)f ou (tau_f_v)f
                        contrainte_4 = calculate_tau_th(NbPL, MbPL, d2, L_prime)
                        nom_contrainte_4bis = "Contrainte fictive de cisaillement dans les filets de la pièce" #(tau_th_p)f ou (tau_f_p)f
                        contrainte_4bis = calculate_tau_th(NbPL, MbPL, d2, L_prime)
                        nom_contrainte_8 = "Contrainte de cisaillement dans les filets de la vis" #tau_th_v ou tau_f_v
                        contrainte_8 = calculate_tau_th(NbAL, MbAL, d2, L_prime)
                        nom_contrainte_8bis = "Contrainte de cisaillement dans les filets de la pièce" #tau_th_p ou tau_f_p
                        contrainte_8bis = calculate_tau_th(NbAL, MbAL, d2, L_prime)
                        
                        L_Contraintes.append([nom_contrainte_1, contrainte_1])
                        L_Contraintes.append([nom_contrainte_2, contrainte_2])
                        L_Contraintes.append([nom_contrainte_3, contrainte_3])
                        L_Contraintes.append([nom_contrainte_4, contrainte_4])
                        L_Contraintes.append([nom_contrainte_4bis, contrainte_4bis])
                        L_Contraintes.append([nom_contrainte_8, contrainte_8])
                        L_Contraintes.append([nom_contrainte_8bis, contrainte_8bis])

            
            
            
            
            
            
    if Study_Case == "B1_D" :
        # st.write("calculer_contraintes : Cas B1_D")
        # st.write("contraintes, cas 3")
        
        nom_contrainte_1 = "Contrainte équivalente moyenne" #sigma_m
        contrainte_1 = calculate_sigma_m(NbAL, TbAL, min(d3, dl))
        nom_contrainte_2 = "Contrainte équivalente maximale" #sigma_m+b
        contrainte_2 = calculate_sigma_m_plus_b(NbAL, MbAL, TbAL, Cr, min(d3, dl))
        nom_contrainte_3 = "Contrainte de cisaillement dans les filets de la vis"  #tau_th_v ou tau_f_v
        contrainte_3 = calculate_tau_th(NbAL, MbAL, d2, L_prime)
        nom_contrainte_4 = "Contrainte de cisaillement dans la tête de la vis"#tau_t
        contrainte_4 = calculate_tau_h(NbAL, MbAL, Ct, d1, dl, H)
        nom_contrainte_4bis = "Contrainte de cisaillement dans les filets de la pièce" #tau_th_p ou tau_f_p
        contrainte_4bis = calculate_tau_th(NbAL, MbAL, d2, L_prime)
        
        L_Contraintes.append([nom_contrainte_1, contrainte_1])
        L_Contraintes.append([nom_contrainte_2, contrainte_2])
        L_Contraintes.append([nom_contrainte_3, contrainte_3])
        L_Contraintes.append([nom_contrainte_4, contrainte_4])
        L_Contraintes.append([nom_contrainte_4bis, contrainte_4bis])
    
            
    
    
    ######
    # B2 #
    ######
    
    if Study_Case == "B2_A" :
        # st.write("calculer_contraintes : Cas B2_A")
        # st.write("contraites, cas 4")
        
        nom_contrainte_1 = "Contrainte équivalente fictive moyenne" #(sigma_m)f
        contrainte_1 = calculate_sigma_m(NbPL, TbPL, min(d3, dl))
        nom_contrainte_2 = "Contrainte équivalente moyenne" # sigma_m
        contrainte_2 = calculate_sigma_m(NbAL, TbAL, min(d3, dl))
        nom_contrainte_3 = "Contrainte équivalente maximale" # sigma_m+b
        contrainte_3 = calculate_sigma_m_plus_b(NbAL, MbAL, TbAL, Cr, min(d3, dl))
        nom_contrainte_4 = "Contrainte fictive de cisaillement dans les filets de la vis" #(tau_th_v)f ou (tau_f_v)f
        contrainte_4 = calculate_tau_th(NbPL, MbPL, d2, L_prime)
        if type_boulonnerie == 'Vis' or type_boulonnerie == 'Goujon' :
            # st.write("contraites, cas 4.1")
            nom_contrainte_4bis = "Contrainte fictive de cisaillement dans les filets de la pièce" #(tau_th_p)f ou (tau_f_p)f
            contrainte_4bis = calculate_tau_th(NbPL, MbPL, d2, L_prime)
        nom_contrainte_5 = "Contrainte fictive de cisaillement dans la tête de la vis" #(tau_h)f ou (tau_t)f
        contrainte_5 = calculate_tau_h(NbPL, MbPL, 0.0, d1, dl, H)
        nom_contrainte_6 = "Contrainte de cisaillement dans les filets de la vis"
        contrainte_6 = calculate_tau_th(NbAL, MbAL, d2, L_prime)
        if type_boulonnerie == 'Vis' or type_boulonnerie == 'Goujon' :
            # st.write("contraites, cas 4.2")
            nom_contrainte_6bis = "Contrainte de cisaillement dans les filets de la pièce"
            contrainte_6bis = calculate_tau_th(NbAL, MbAL, d2, L_prime)
        nom_contrainte_7 = "Contrainte de cisaillement dans la tête de la vis"
        contrainte_7 = calculate_tau_h(NbAL, MbAL, Ct, d1, dl, H)
        nom_contrainte_8 = "Pression de contact sur la tête de la vis"
        if rondelle == False : #S'il n'y a pas de rondelle
            # st.write("contraintes, cas 4.3")
   
            contrainte_8 = calculate_p_h(NbAL, MbAL, a, Dp)
        else : #S'il y a une rondelle
            # st.write("contrainte, cas 4.4")
            if SyminP_T > SyminB_T :
                # st.write("contrainte, cas 4.4.1")
                contrainte_8 = calculate_p_h(NbAL, MbAL, a, B)
            else :
                # st.write("contrainte, cas 4.4.2")
                contrainte_8 = calculate_p_h(NbAL, MbAL, a_prime, Dp_prime)
                
        
        L_Contraintes.append([nom_contrainte_1, contrainte_1])
        L_Contraintes.append([nom_contrainte_2, contrainte_2])
        L_Contraintes.append([nom_contrainte_3, contrainte_3])
        L_Contraintes.append([nom_contrainte_4, contrainte_4])
        if type_boulonnerie == 'Vis' or type_boulonnerie == 'Goujon' :
            L_Contraintes.append([nom_contrainte_4bis, contrainte_4bis])
        L_Contraintes.append([nom_contrainte_5, contrainte_5])
        L_Contraintes.append([nom_contrainte_6, contrainte_6])
        if type_boulonnerie == 'Vis' or type_boulonnerie == 'Goujon' :
            L_Contraintes.append([nom_contrainte_6bis, contrainte_6bis])
        L_Contraintes.append([nom_contrainte_7, contrainte_7])
        L_Contraintes.append([nom_contrainte_8, contrainte_8])
        
        
    if Study_Case == "B2_C" :
        # st.write("calculer_contraintes : Cas B2_C")
        # st.write("contrainte, cas 5")
        
        #Resistance Normale
        if Sumin_T < 700 :
            # st.write("contrainte, cas 5.1")
            # st.write("Résistance Normale")
            
            nom_contrainte_1 = "Contrainte équivalente ficitve moyenne"
            contrainte_1 = calculate_sigma_m(NbPL, TbPL, min(d3, dl))
            nom_contrainte_2 = "Contrainte équivalente fictive maximale"
            contrainte_2 = calculate_sigma_m_plus_b(NbPL, MbPL, TbPL, 0.0, min(d3, dl))
            
            L_Contraintes.append([nom_contrainte_1, contrainte_1])
            L_Contraintes.append([nom_contrainte_2, contrainte_2])
            
        #Haute Résistance
        else :
            # st.write("Haute Résistance")
            # st.write("contrainte, cas 5.2")
            
            nom_contrainte_1 = "Contrainte équivalente fictive moyenne"
            contrainte_1 = calculate_sigma_m(NbPL, TbPL, min(d3, dl))
            nom_contrainte_2 = "Contrainte équivalente moyenne"
            contrainte_2 = calculate_sigma_m(NbAL, TbAL, min(d3, dl))
            nom_contrainte_3 = "Contrainte équivalente maximale"
            contrainte_3 = calculate_sigma_m_plus_b(NbAL, MbAL, TbAL, Cr, min(d3, dl))
            nom_contrainte_4 = "Contrainte fictive de cisaillement dans les filets de la vis"
            contrainte_4 = calculate_tau_th(NbPL, MbPL, d2, L_prime)
            nom_contrainte_5 = "Contrainte fictive de cisaillement dans la tête de la vis"
            contrainte_5 = calculate_tau_h(NbPL, MbPL, 0.0, d1, dl, H)
            if type_boulonnerie == 'Vis' or type_boulonnerie == 'Goujon' :
                # st.write("contrainte, cas 5.2.1")
                nom_contrainte_5bis = "Contrainte fictive de cisaillement dans les filets de la pièce" #(tau_th_p)f ou (tau_f_p)f
                contrainte_5bis = calculate_tau_th(NbPL, MbPL, d2, L_prime)
            nom_contrainte_6 = "Contrainte de cisaillement dans les filets de la vis"
            contrainte_6 = calculate_tau_th(NbAL, MbAL, d2, L_prime)
            nom_contrainte_7 = "Contrainte de cisaillement dans la tête de la vis"
            contrainte_7 = calculate_tau_h(NbAL, MbAL, Ct, d1, dl, H)
            if type_boulonnerie == 'Vis' or type_boulonnerie == 'Goujon' :
                # st.write("contrainte, cas 5.2.2")
                nom_contrainte_7bis = "Contrainte de cisaillement dans les filets de la pièce"
                contrainte_7bis = calculate_tau_th(NbAL, MbAL, d2, L_prime)
            nom_contrainte_8 = "Pression de contact sur la tête de la vis"
            if rondelle == False : #S'il n'y a pas de rondelle
                # st.write("contrainte, cas 5.3")
                contrainte_8 = calculate_p_h(NbAL, MbAL, a, Dp)
            else : #S'il y a une rondelle
                # st.write("contrainte, cas 5.4")
                if SyminP_T > SyminB_T :
                    # st.write("contrainte, cas 5.4.1")
                    contrainte_8 = calculate_p_h(NbAL, MbAL, a, B)
                else :
                    # st.write("contrainte, cas 5.4.2")
                    contrainte_8 = calculate_p_h(NbAL, MbAL, a_prime, Dp_prime)
            
            L_Contraintes.append([nom_contrainte_1, contrainte_1])
            L_Contraintes.append([nom_contrainte_2, contrainte_2])
            L_Contraintes.append([nom_contrainte_3, contrainte_3])
            L_Contraintes.append([nom_contrainte_4, contrainte_4])
            L_Contraintes.append([nom_contrainte_5, contrainte_5])
            if type_boulonnerie == 'Vis' or type_boulonnerie == 'Goujon' :
                L_Contraintes.append([nom_contrainte_5bis, contrainte_5bis])
            L_Contraintes.append([nom_contrainte_6, contrainte_6])
            L_Contraintes.append([nom_contrainte_7, contrainte_7])
            if type_boulonnerie == 'Vis' or type_boulonnerie == 'Goujon' :
                L_Contraintes.append([nom_contrainte_7bis, contrainte_7bis])
            L_Contraintes.append([nom_contrainte_8, contrainte_8])
    
    
    if Study_Case == "B2_D" :
        # st.write("calculer_contraintes : Cas B2_D")
        # st.write("contrainte, cas 6")
        
        nom_contrainte_1 = "Contrainte équivalente fictive moyenne"
        contrainte_1 = calculate_sigma_m(NbPL, TbPL, min(d3, dl))
        nom_contrainte_2 = "Contrainte équivalente fictive maximale"
        contrainte_2 = calculate_sigma_m_plus_b(NbPL, MbPL, TbPL, 0.0, min(d3, dl))
        
        L_Contraintes.append([nom_contrainte_1, contrainte_1])
        L_Contraintes.append([nom_contrainte_2, contrainte_2])
    
    
    
    ######
    # B3 #
    ######
    
    if Study_Case == "B3_A" :
        # st.write("calculer_contraintes : Cas B3_A")
        # st.write("contrainte, cas 7")
        
        nom_contrainte_1 = "Contrainte de traction moyenne"
        contrainte_1 = calculate_sigma_N(NbAL, d3)
        nom_contrainte_2 = "Contrainte de cisaillement"
        contrainte_2 = calculate_tau_T(TbAL, d3)
        
        nom_contrainte_3 = "Contraintes combinées"
        if B_acier_aust == True :
            # st.write("contrainte, cas 6.1")
            critere_1 = 0.3*Sumin_T
            critere_2 = Sumin_T/8
        else :
            # st.write("contrainte, cas 6.2")
            critere_1 = 0.5*Sumin_T
            critere_2 = 5*Sumin_T/24
        contrainte_3 = (contrainte_1**2)/(critere_1**2) + (contrainte_2**2)/(critere_2**2)
        
        nom_contrainte_4 = "Pression latérale"
        contrainte_4 = TbAL/(e*d)
        
        L_Contraintes.append([nom_contrainte_1, contrainte_1])
        L_Contraintes.append([nom_contrainte_2, contrainte_2])
        L_Contraintes.append([nom_contrainte_3, contrainte_3])
        L_Contraintes.append([nom_contrainte_4, contrainte_4])
        
        
    if Study_Case == "B3_C" :
        # st.write("calculer_contraintes : Cas B3_C")
        # st.write("contrainte, cas 7")
        nom_contrainte_1 = "Contrainte de traction moyenne"
        contrainte_1 = calculate_sigma_N(NbAL, d3)
        nom_contrainte_2 = "Contrainte de cisaillement"
        contrainte_2 = calculate_tau_T(TbAL, d3)
        
        nom_contrainte_3 = "Contraintes combinées"
        if B_acier_aust == False :
            # st.write("contrainte, cas 7.1")
            critere_1 = min(1.25*0.5*Sumin_T, SyminB_T)
            critere_2 = min(1.25*5*Sumin_T/24, SyminB_T)
        
        else :
            # st.write("contrainte, cas 7.2")
            critere_1 = min(1.25*0.3*Sumin_T, SyminB_T)
            critere_2 = min(1.25*Sumin_T/8, SyminB_T)
        contrainte_3 = (contrainte_1**2)/(critere_1**2) + (contrainte_2**2)/(critere_2**2)
        
        nom_contrainte_4 = "Pression latérale"
        contrainte_4 = TbAL/(e*d)
        
        L_Contraintes.append([nom_contrainte_1, contrainte_1])
        L_Contraintes.append([nom_contrainte_2, contrainte_2])
        L_Contraintes.append([nom_contrainte_3, contrainte_3])
        L_Contraintes.append([nom_contrainte_4, contrainte_4])
        
        
    if Study_Case == "B3_D" :
        # st.write("calculer_contraintes : Cas B3_D")
        # st.write("contrainte, cas 8")
        
        nom_contrainte_1 = "Contrainte de traction moyenne"
        contrainte_1 = calculate_sigma_N(NbAL, d3)
        nom_contrainte_2 = "Contrainte de cisaillement"
        contrainte_2 = calculate_tau_T(TbAL, d3)
        
        nom_contrainte_3 = "Contraintes combinées"
        critere_1 = min(SyminB_T, 0.7*Sumin_T)
        critere_2 = min(0.6*SyminB_T, 0.42*Sumin_T)
 
        contrainte_3 = (contrainte_1**2)/(critere_1**2) + (contrainte_2**2)/(critere_2**2)
        
        L_Contraintes.append([nom_contrainte_1, contrainte_1])
        L_Contraintes.append([nom_contrainte_2, contrainte_2])
        L_Contraintes.append([nom_contrainte_3, contrainte_3])
        
        if Sumin_T >= 700 :
            # st.write("contrainte, cas 8.1")
            nom_contrainte_4 = "Contrainte de traction maximale"
            contrainte_4 = calculate_sigma_N(NbAL, d3) + calculate_sigma_M(MbAL, d3)
            
            L_Contraintes.append([nom_contrainte_4, contrainte_4])
    
    return L_Contraintes





def calculer_criteres(d, SyminB_T, SyminP_T, SuminB_T, SuminP_T, Sm_T, SmB_T, Study_Case, h, L, Le, type_boulonnerie, B_acier_aust) :
    
    L_Criteres = []


    ######
    # B1 #
    ######

    # Si le critère est A ou C
    if Study_Case == "B1_A" or Study_Case == "B1_C" : 
        # st.write("calculer_criteres : Cas B1_A ou B1_C")
        # st.write("h = ", h)
        # st.write("0.8xd = ", 0.8*d)
        # st.write("h < 0.8*d", h < 0.8*d)
        if h < 0.8*d : # h = 0.0 (ie: pas d'écrou) est compris dans ce cas. Il n'y a pas d'écrou, on vérifie tous les critères
            # st.write("critère, cas 1")
            critere_1 = SmB_T                                   #(sigma_m)f
            critere_2 = 2*SmB_T                                 #sigma_m
            critere_3 = 3*SmB_T                                 #sigma_m+b
            critere_4 = 0.6*SmB_T                               #(tau_th_v)f ou (tau_f_v)f
            critere_5 = 0.6*SmB_T                               #(tau_t)f 
            critere_6 = 0.5*min(SyminB_T, SyminP_T)             #(p_th)f ou (p_f)f
            critere_7 = 0.5*min(SyminB_T, SyminP_T)             #(p_t)f
            critere_8 = 1.2*SmB_T                               #tau_th_v ou tau_f_v
            critere_9 = 1.2*SmB_T                               #tau_t
            critere_10 = min(SyminB_T, SyminP_T)                #p_th ou p_f
            critere_11 = min(SyminB_T, SyminP_T)                #p_t

            if type_boulonnerie == 'Vis' or type_boulonnerie == 'Goujon' :
                # st.write("critère, cas 1.1")
                critere_4bis = 0.3*Sm_T                         #(tau_th_p)f ou (tau_f_p)f
                critere_8bis = 0.6*Sm_T                         #tau_th_p ou tau_f_p
                L_Criteres = [critere_1, critere_2, critere_3, critere_4, critere_4bis, critere_5, critere_6, critere_7, critere_8, critere_8bis, critere_9, critere_10, critere_11]
            else :
                # st.write("critère, cas 1.2")
                L_Criteres = [critere_1, critere_2, critere_3, critere_4, critere_5, critere_6, critere_7, critere_8, critere_9, critere_10, critere_11]

        else : # h >= 0.8*d
            # st.write("critere, cas 2")
            if type_boulonnerie == 'Boulon' or type_boulonnerie == 'Lacet' :
                # st.write("critère, cas 2.1")
                critere_1 = SmB_T                                   #(sigma_m)f
                critere_2 = 2*SmB_T                                 #sigma_m
                critere_3 = 3*SmB_T                                 #sigma_m+b

                L_Criteres = [critere_1, critere_2, critere_3]

            else : # si c'est une vis ou un goujon
                # st.write("critère, cas 2.2")
                if SyminP_T < SyminB_T :
                    # st.write("critère, cas 2.2.1")
                    critere_1 = SmB_T                                   #(sigma_m)f
                    critere_2 = 2*SmB_T                                 #sigma_m
                    critere_3 = 3*SmB_T                                 #sigma_m+b
                    critere_4bis = 0.3*Sm_T                             #(tau_th_p)f ou (tau_f_p)f
                    critere_8bis = 0.6*Sm_T                             #tau_th_p ou tau_f_p

                    L_Criteres = [critere_1, critere_2, critere_3, critere_4bis, critere_8bis]
                    
                else : # SyminP_T >= SyminB_T
                    # st.write("critère, cas 2.2.2")
                    # st.write("Le = ", Le)
                    # st.write("0.8xd = ", 0.8*d)
                    # st.write("Le >= 0.8*d", Le >= 0.8*d)
                    if Le >= 0.8*d :
                        # st.write("critère, cas 2.2.2.1")
                        critere_1 = SmB_T                                   #(sigma_m)f
                        critere_2 = 2*SmB_T                                 #sigma_m
                        critere_3 = 3*SmB_T                                 #sigma_m+b
        
                        L_Criteres = [critere_1, critere_2, critere_3]
                        
                    else : # Le < 0.8*d
                        # st.write("critère, cas 2.2.2.2")
                        critere_1 = SmB_T                                   #(sigma_m)f
                        critere_2 = 2*SmB_T                                 #sigma_m
                        critere_3 = 3*SmB_T                                 #sigma_m+b
                        critere_4 = 0.6*SmB_T                               #(tau_th_v)f ou (tau_f_v)f
                        critere_4bis = 0.3*Sm_T                             #(tau_th_p)f ou (tau_f_p)f
                        critere_8 = 1.2*SmB_T                               #tau_th_v ou tau_f_v
                        critere_8bis = 0.6*Sm_T                             #tau_th_p ou tau_f_p
                        L_Criteres = [critere_1, critere_2, critere_3, critere_4, critere_4bis, critere_8, critere_8bis]
                    
                
                
    if Study_Case == "B1_D" : 
        # st.write("calculer_criteres : Cas B1_D")
        critere_1 = min(SyminB_T, 0.7*SuminB_T)
        critere_2 = SuminB_T
        critere_3 = min(0.6*SyminB_T, 0.42*SuminB_T)
        critere_4 = min(0.6*SyminB_T, 0.42*SuminB_T)
        critere_4bis = min(0.6*SyminP_T, 0.42*SuminP_T)
        
        L_Criteres = [critere_1, critere_2, critere_3, critere_4, critere_4bis]


    
    ######
    # B2 #
    ######
    
    if Study_Case == "B2_A" : 
        # st.write("calculer_criteres : Cas B2_A")
        critere_1 = SmB_T                                         # (sigma_m)f
        critere_2 = min(0.9*SyminB_T, 0.67*SuminB_T)              # sigma_m
        critere_3 = 1.33*min(0.9*SyminB_T, 0.67*SuminB_T)         # sigma_m+b
        critere_4 = 0.6*SmB_T                                     #(tau_th_v)f ou (tau_f_v)f
        critere_5 = 0.6*SmB_T                                     #(tau_h)f ou (tau_t)f
        critere_6 = 0.6*SyminB_T                                  #tau_th_v ou tau_f_v
        critere_7 = 0.6*SyminB_T                                  #tau_h ou tau_t
        critere_8 = 2.7*min(SyminB_T, SyminP_T)                   #p_t
        
        if type_boulonnerie == 'Vis' or type_boulonnerie == 'Goujon' :
            critere_4bis = 0.3*Sm_T                               #(tau_th_p)f ou (tau_f_p)f
            critere_6bis = 0.6*SyminP_T                           #tau_th_p ou tau_f_p

        if type_boulonnerie == 'Vis' or type_boulonnerie == 'Goujon' :
            L_Criteres = [critere_1, critere_2, critere_3, critere_4, critere_4bis, critere_5, critere_6, critere_6bis, critere_7, critere_8]
        else :
            L_Criteres = [critere_1, critere_2, critere_3, critere_4, critere_5, critere_6, critere_7, critere_8]
            
    if Study_Case == "B2_C" : 
        # st.write("calculer_criteres : Cas B2_C")
        # Resistance Normale
        if SuminB_T < 700 :
            critere_1 = 1.5*SmB_T
            critere_2 = 2.25*SmB_T
            
            L_Criteres = [critere_1, critere_2]
        
        # Haute Résistance
        else :
            critere_1 = SmB_T
            critere_2 = min(0.9*SyminB_T, 0.67*SuminB_T)
            critere_3 = 1.33*min(0.9*SyminB_T, 0.67*SuminB_T)
            critere_4 = 0.6*SmB_T                               # (tau_f_v)f
            critere_5 = 0.6*SmB_T                               # (tau_t)f
            
            critere_6 = 0.6*SyminB_T                            # tau_f_v
            critere_7 = 0.6*SyminB_T                            # tau_t
            
            critere_8 = 2.7*min(SyminB_T, SyminP_T)             # p_t

            if type_boulonnerie == 'Vis' or type_boulonnerie == 'Goujon' :
                critere_5bis = 0.3*Sm_T                         # (tau_f_p)f
                critere_7bis = 0.6*SyminP_T                     # tau_f_p
            
                L_Criteres = [critere_1, critere_2, critere_3, critere_4, critere_5, critere_5bis, critere_6, critere_7, critere_7bis, critere_8]
                
            else :
                L_Criteres = [critere_1, critere_2, critere_3, critere_4, critere_5, critere_6, critere_7, critere_8]
    
    if Study_Case == "B2_D" : 
        # st.write("calculer_criteres : Cas B2_D")
        #Resistance Normale
        if SuminB_T < 700 :
            critere_1 = min(2.4*SmB_T, 0.7*SuminB_T)
            critere_2 = 1.5*min(2.4*SmB_T, 0.7*SuminB_T)
            
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
        # st.write("calculer_criteres : Cas B3_A")
        
        if B_acier_aust == False :
            critere_1 = 0.5*SuminB_T
            critere_2 = 5*SuminB_T/24
        
        else :
            critere_1 = 0.3*SuminB_T
            critere_2 = SuminB_T/8
        
        critere_3 = 1
        critere_4 = min(L*SuminP_T/(2*d), 1.5*SuminP_T)
    
        L_Criteres = [critere_1, critere_2, critere_3, critere_4]
        
        
    if Study_Case == "B3_C" : 
        # st.write("calculer_criteres : Cas B3_C")
        if B_acier_aust == False :
            critere_1 = min(1.25*0.5*SuminB_T, SyminB_T)
            critere_2 = min(1.25*5*SuminB_T/24, SyminB_T)
        
        else :
            critere_1 = min(1.25*0.3*SuminB_T, SyminB_T)
            critere_2 = min(1.25*SuminB_T/8, SyminB_T)
        
        critere_3 = 1
        critere_4 = min(min(L*SuminP_T/(2*d), 1.5*SuminP_T), SyminP_T)
    
        L_Criteres = [critere_1, critere_2, critere_3, critere_4]

    
    if Study_Case == "B3_D" : 
        # st.write("calculer_criteres : Cas B3_D")
        critere_1 = min(SyminB_T, 0.7*SuminB_T)
        critere_2 = min(0.6*SyminB_T, 0.42*SuminB_T)
        critere_3 = 1
        
        L_Criteres = [critere_1, critere_2, critere_3]
                      
        #Haute Normale
        if SuminB_T >= 700 :
            critere_4 = SuminB_T
            
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
    
    marge = 100*(float(critere) - float(valeur))/float(critere)
    
    return marge


def calculer_marges_all_results(L_Contraintes, L_Criteres) :
    L_Bilan_Boulon_i = []
    
    #On ajoute l'entete
    L_Bilan_Boulon_i.append(['Nom de la contrainte', 'Contrainte [MPa]', 'Critere [MPa]', 'Marge [%]'])
    
    
    for i in range(0, len(L_Contraintes)) :
        contrainte = round(L_Contraintes[i][1], 2)
        critere = round(L_Criteres[i], 2)
        marge = calculer_marge(contrainte, critere)
        marge = round(float(marge), 2)
        
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
    liste_material = ["304L SS", "316L SS", "660 SS", "Acier Classe 6-8", "Alloy 718", "316L", "A4L-80", "A4L-70", "A2L-80", "A2L-70"]
    L_Acier_Aust = ["A2L-70", "A2L-80", "A4L-70", "A4L-80"]
      
    # Titre de l'application
    st.title("Dimensionnement de la boulonnerie selon le RCC-MRx")

    with st.expander("INTRODUCTION ET RAPPEL DES HYPOTHÈSES.") :
        st.subheader("Objectifs et conditions d'application")
        st.write("Cette partie est dédiée au dimensionnement des liaisons boulonnées selon le recueil de règles rédigé par l’AFCEN, le *RCC-MRx* (*R*ègles techniques applicables à la *C*onception et la *C*onstruction des *M*atériels mécaniques des installations nucléaires). Ce document propose 3 niveaux de conception et de construction correspondant à 3 niveaux de sécurité décroissants : $N1_{RX}$, $N2_{RX}$ et $N3_{RX}$. Cette application se concentre sur le dimensionnement des éléments de serrage appartenant aux deux premiers niveaux (*RB 3000* et *RC 3000*).")
        st.write("Les règles d’analyse pour la boulonnerie sont recensées dans le *RB 3280*. Il est composé de 3 jeux de règles, applicables aux vis, boulons, goujons et lacets de niveau $N1_{RX}$ et $N2_{RX}$ :")
        st.write("- Le jeu de règles *B1* (*RB 3281*, *RB 3282* et *RB 3283*), qui concerne les liaisons boulonnées précontraintes qui assurent une fonction d’étanchéité.")
        st.write("- Le jeu de règles *B2* (*RB 3281*, *RB 3284* et *RB 3285*), qui concerne les liaisons boulonnées précontraintes qui n’assurent pas de fonction d’étanchéité.")
        st.write("- Le jeu de règles *B3* (*RB 3281* et *RB 3286*), qui concerne les liaisons boulonnées non précontraintes.")
        st.write("Pour tous les niveaux de critère, l’analyse élastique est à appliquer. Ces règles se basent sur un modèle simple de l’élément de serrage, réduit à une tige cylindrique lisse appelée *noyau*. Son diamètre est par convention égal au diamètre de la section minimale du boulon. Si elle est dans la partie filetée, il est égal au diamètre à fond de filet.")
        st.image("Pictures/Figure RB 3281-4.PNG", caption='Figure RB 3281.4')
        st.write("Pour simplifier sa mise en place, l’application ne se concentre pour le moment que sur le dimensionnement des éléments de serrage pouvant présenter des *dommages de type P*. De plus, le fluage et l’irradiation sont supposés *négligeables*. Les critères évalués relèvent ainsi des *RB 3282*, *RB 3284* et *RB 3286*. Enfin, le calcul des contraintes appliquées à l’élément de serrage suit sur les règles énoncées dans l’*Annexe 6*.")
        st.write("")
        st.subheader("Présentation")
        st.write("Cette application simple d’utilisation se compose en plusieurs parties. Après avoir choisi le type d’élément de serrage, l’utilisateur doit renseigner :")
        st.write("1. les données géométriques de son élément de serrage")
        st.write("2. le matériau qui le compose et sa température à partir d’une base de données intégrée")
        st.write("3. le matériau des pièces assemblées et leur température à partir d’une base de données intégrée")
        st.write("4. les résultats de la simulation ANSYS, au format .CSV et sous la forme :")
        st.write("Nom ou numéro de l'élément de serrage | Force axiale [N] | Couple [N.mm] | Force de cisaillement [N] | Moment de flexion [N.mm]")
        st.write("5. les conditions de calcul : fonctions de l’élément de serrage, niveau de critère à évaluer; etc.")
        st.write("Les résultats sont ensuites générés sous la forme :")
        st.write("Nom de la contrainte | Valeur de la contrainte | Critère de dimensionnement | Marge associée")
        st.write("")
        st.write("Un rapport automatique est généré et peut être téléchargé. Il rassemble les informations renseignées, les critères évalués, les résultats et le détail des formules utilisées. A titre informatif, la base de données des matériaux est issue de l’*Annexe 3* du *RCC-MRx.*")
        st.write("Bon dimensionnement !")



    
    # =============================================================================
    # DONNEES D'ENTREE    
    # =============================================================================
    
    st.header("SAISIE DES DONNÉES D'ENTRÉE") # Partie
    
    st.subheader("Type d'élément de serrage") #Sous-Partie
    
    type_boulonnerie = st.radio("", ("Vis", "Boulon", "Goujon", "Lacet"), horizontal=True)
    st.write("") # Saut de ligne
    
    st.subheader("Données liées à l'élément de serrage")
    
    st.write("- ##### *Données géométriques*")

    # On fait demande à l'utilisateur de renseigner s'il y a une rondelle et ou un écrou
    col_rondelle, col_ecrou, col_rondelle_ecrou_vide = st.columns([1, 1, 1]) # On utilise des colonnes pour afficher les cases à cocher l'une à coté de l'autre
    with col_rondelle :
        check_rondelle = st.checkbox("Présence d'une rondelle")

    with col_ecrou :
        check_ecrou = st.checkbox("Présence d'un écrou")
    
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        d = st.text_input("$d [mm]$ :", placeholder = "0.0")
        p = st.text_input("$p [mm]$ :", placeholder = "0.0")
        dl = st.text_input("$d_{l} [mm]$ :", placeholder = "0.0")
        a = st.text_input("$a [mm]$ :", placeholder = "0.0")
        H = st.text_input("$H [mm]$ :", placeholder = "0.0")


        
    with col2:
        Dp = st.text_input("$D_p [mm]$ :", placeholder = "0.0")
        Le = st.text_input("$L_{e} [mm]$ :", placeholder = "0.0")
        if check_rondelle :
            B = st.text_input("$B [mm]$", placeholder = "0.0")
            C = st.text_input("$C [mm]$", placeholder = "0.0")
            A = st.text_input("$A [mm]$", placeholder = "0.0")

            B = float(B) if B else 0.0
            C = float(C) if C else 0.0
            A = float(A) if A else 0.0        
        else : # On met une valeur nulle par défaut pour que le code puisse utiliser les fonctions suivantes (float()) et savoir qu'il n'y a pas de rondelles (cf calcul de Dm) 
            B = 0.0
            C = 0.0
            A = 0.0

        if check_ecrou :
            h = st.text_input("$h [mm]$", placeholder = "0.0")
            h = float(h) if h else 0.0
        else :
            h = 0.0
        
    with col3:
        if type_boulonnerie == "Vis" :
            st.image("Pictures/RCC-MRx_Vis.PNG", use_column_width=True)
        elif type_boulonnerie == "Boulon" :
            st.image("Pictures/RCC-MRx_Boulon.PNG", use_column_width=True)
        elif type_boulonnerie == "Goujon" :
            st.image("Pictures/RCC-MRx_Goujon.PNG", use_column_width=True)
        elif type_boulonnerie == "Lacet" :
            st.image("Pictures/RCC-MRx_Lacet.PNG", use_column_width=True)
        
    d = float(d) if d else 1.0
    p = float(p) if p else 1.0
    dl = float(dl) if dl else 1.0
    a = float(a) if a else 1.0
    H = float(H) if H else 1.0
    Dp = float(Dp) if Dp else 2.0
    Le = float(Le) if Le else 1.0
    
    
    L_Designation = ["Diamètre nominal", "Pas", "Diamètre du fût lisse",
                     "Diamètre sur le plat de la tête", "Hauteur de la tête", "Diamètre de perçage", "Longueur d'engagement des filets \n en prise",
                     "Diamètre intérieur de la rondelle", "Epaisseur de la rondelle", "Diamètre extérieur de la rondelle"]
    L_Symbole = ["d", "p", "dl", "a", "H", "Dp", "Le", "B", "C", "A"]
    L_Valeur = [d, p, dl, a, H, Dp, Le, B, C, A]
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
        a_prime = min(a + 2*C, A) #Pour le calcul de p_h et p_th
        Dp_prime = max(Dp, B) #Pour le calcul de p_h et p_th
    
    Dm = round(Dm, 2)    
    
    L_Donnees_Geo_Boulonnerie_Full = L_Valeur + [d1, d2, d3, D, round(float(L_prime),2), Dm, a_prime, Dp_prime] 

    with st.expander("Détails sur les données géométriques à saisir") :
        # st.info("- $d$ : diamètre nominal\n- $p$ : pas\n- $l_l$ : longueur du fût lisse\n- $l_n$ : longueur du filetage non en prise avec les pièces assemblées\n- $a$ : Diamètre sur plat de la tête\n- $D_p$ : Diamètre de perçage\n- $l_{a1}$ : Longueur de la pièce assemblée 1\n- $l_{a2}$ : Longueur de la pièce assemblée 2\n- $l_{a3}$ : Longueur de la pièce assemblée 3") 
        st.write("- $d$ : Diamètre nominal")
        st.write("- $p$ : Pas") 
        st.write("- $d_l$ : Diamètre du fût lisse") 
        st.write("- $a$ : Diamètre sur le plat de la tête") 
        st.write("- $H$ : Hauteur de la tête")
        st.write("- $D_p$ : Diamètre de perçage")
        st.write("- $L_e$ : Longueur d'engagement des filets en prise")
        st.write("- $B$ : Diamètre intérieur de la rondelle")
        st.write("- $C$ : Epaisseur de la rondelle")
        st.write("- $A$ : Diamètre extérieur de la rondelle")
        st.write("- $h$ : Hauteur de l'écrou")
        # st.write("*Remarque : Les rondelles doivent être considérées comme une pièce assemblée. D'après le § A6.2423 du RCC MRx, dans le cas de vis et de goujons, la longueur à prendre en compte pour la pièce taraudée sera égale à 40 % du diamètre nominal (0,4 d).*")

    # saut de ligne
    st.write("\n")



    
    st.write("- ##### *Données matériau*")
    
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

        st.write("\n")
        st.write("###### Température de calcul (en °C)")
        Tb = st.text_input("Température de calcul $T_b$, en °C :", placeholder = "0.0", label_visibility="collapsed")
        Tb = float(Tb) if Tb else 20.0
        
        
        
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

    
    # On récupère les propriétés méca 
    SuminB_T = float(get_grandeur_T_quelconque('Su.min', L_Bolt_Material_Properties, float(Tb)))
    SyminB_T = float(get_grandeur_T_quelconque('Sy.min', L_Bolt_Material_Properties, float(Tb)))
    SmB_T = float(get_grandeur_T_quelconque('SmB_non_etanche', L_Bolt_Material_Properties, float(Tb)))

    # On les affiches dans un dataframe
    T_Bolt_Data = [['Matériau', 'Température [°C]', 'SmB [MPa]', '(Rp0,2)min,B [MPa]', '(Rm)min,B [MPa]'], [materiau_bolt, float(Tb), SmB_T, SyminB_T, SuminB_T]]
    df_Bolt_Material_Data = pd.DataFrame(T_Bolt_Data[1:], columns=T_Bolt_Data[0])
    st.write(df_Bolt_Material_Data)
                                                         
    # saut de ligne
    st.write("\n")

    
    
    st.subheader("Données liées aux pièces assemblées")

    st.write("- ##### *Données matériaux*")


    # Initialiser le DataFrame vide
    if 'propriete_mat_pieces_RCCMRx' not in st.session_state:
        st.session_state.propriete_mat_pieces_RCCMRx = pd.DataFrame(columns=['Matériau', 'Température [°C]', 'Sm [MPa]', '(Rp0,2)min,P [MPa]', '(Rm)min,P [MPa]'])
    
    # Saisies utilisateur pour ajouter des données
    saisie_col1, saisie_col2 = st.columns([1, 1])
    with saisie_col1 :
        materiau = st.selectbox('Matériau', liste_material)
    with saisie_col2 :
        T_piece_assemblee = st.text_input('Température [°C]', placeholder = 0.0)
    
    but_col1, but_col2, but_col3 = st.columns([1,1,4])
    with but_col1:
        # Bouton pour ajouter les données au DataFrame
        if st.button('Ajouter', use_container_width = True):
            F_Assembly_Part_Material_Properties = "Material_Properties/" + materiau + '.csv'
            L_Assembly_Part_Material_Properties = traduire_fichier_to_liste(F_Assembly_Part_Material_Properties)
            Sm_piece_assemblee = float(get_grandeur_T_quelconque('Sm', L_Assembly_Part_Material_Properties, float(T_piece_assemblee)))
            Symin_piece_assemblee = float(get_grandeur_T_quelconque('Sy.min', L_Assembly_Part_Material_Properties, float(T_piece_assemblee)))
            Sumin_piece_assemblee = float(get_grandeur_T_quelconque('Su.min', L_Assembly_Part_Material_Properties, float(T_piece_assemblee)))
            new_data = pd.DataFrame({'Matériau': [materiau], 'Température [°C]' : [float(T_piece_assemblee)], 'Sm [MPa]': [Sm_piece_assemblee], '(Rp0,2)min,P [MPa]' : [Symin_piece_assemblee], '(Rm)min,P [MPa]' : [Sumin_piece_assemblee]})
            st.session_state.propriete_mat_pieces_RCCMRx = pd.concat([st.session_state.propriete_mat_pieces_RCCMRx, new_data], ignore_index=True)
    with but_col2:
        if st.button('Effacer', use_container_width = True):
            st.session_state.propriete_mat_pieces_RCCMRx = pd.DataFrame(columns=['Matériau', 'Température [°C]', 'Sm [MPa]', '(Rp0,2)min,P [MPa]', '(Rm)min,P [MPa]'])
    
    # Afficher les données sous forme de tableau
    st.dataframe(st.session_state.propriete_mat_pieces_RCCMRx)
    
    
    materiau_piece = st.session_state.propriete_mat_pieces_RCCMRx['Matériau'].tolist()
    L_Sm = st.session_state.propriete_mat_pieces_RCCMRx['Sm [MPa]'].tolist()
    Sm_T = float(min(L_Sm))

    L_SyminP = st.session_state.propriete_mat_pieces_RCCMRx['(Rp0,2)min,P [MPa]'].tolist()
    SyminP_T = float(min(L_SyminP))

    L_SuminP = st.session_state.propriete_mat_pieces_RCCMRx['(Rm)min,P [MPa]'].tolist()
    SuminP_T = float(min(L_SuminP))
    
    # saut de ligne
    st.write("\n")
    
    
    
    # ===================================
    # Saisie du fichier de résultat Ansys
    # ===================================
    st.subheader("Fichier de résultats ANSYS")
    
    # Bouton pour uploader un fichier CSV
    uploaded_file = st.file_uploader("Sélection du fichier de résultat ANSYS au format CSV", type="csv", label_visibility="collapsed")
    
    if uploaded_file is not None:
        # Lire le fichier CSV
        df = pd.read_csv(uploaded_file, sep = ';')
    
        # Afficher le dataframe
        st.write(df)
        
        # Transformer le DataFrame en une liste de listes
        T_Results_Ansys = df.values.tolist()
    
    else:
        # st.write("Veuillez uploader un fichier CSV.")
        st.write(" ")
    
    # Pour afficher un message une fois le fichier lu
    if uploaded_file is not None:
        st.success('Fichier téléchargé et lu avec succès !')

    else : 
        st.warning("Aucun fichier téléchargé.")
    
    # saut de ligne
    st.write("\n")
    
    # saut de ligne
    st.write("\n")
    
    
    
    
    
    st.subheader("Conditions de calcul")
    
    # =======================================
    # Saisie de la fonction de la boulonnerie
    # =======================================

    st.write("- ##### *Fonction de l'élément de serrage*")
    
    fct_bolt_col_1, fct_bolt_col_2 = st.columns([1, 1])
    with fct_bolt_col_1 :
        check_preload = st.checkbox("Boulonnerie précontrainte")
    
    with fct_bolt_col_2 :
        if check_preload :
            check_etancheite = st.checkbox("Fonction d'étanchéité")

    # saut de ligne
    st.write("\n")
    
    # saut de ligne
    st.write("\n")
      
            
      
        
      
    # ==============================
    # Sélection du niveau de critère
    # ==============================
    
    st.write("- ##### *Niveau de critère*") #Sous-Partie
    critere_selection = st.radio("", ("A", "C", "D"), horizontal=True, label_visibility="collapsed")
    # saut de ligne
    st.write("\n")
    
    # saut de ligne
    st.write("\n")
    
    
    
    
    
    # ===================================================================
    # Saisie des données complémentaires en fonction des données d'entrée
    # ===================================================================
    st.write("- ##### *Données complémentaires*")
    
    # Détermination du cas d'étude
    if check_preload and check_etancheite :
        if critere_selection == "A" :
            Study_Case = "B1_A"
            # st.write(Study_Case)
        elif critere_selection == "C" :
            Study_Case = "B1_C"
            # st.write(Study_Case)
        elif critere_selection == "D" :
            Study_Case = "B1_D"
            # st.write(Study_Case)
            
            
    elif check_preload and not check_etancheite :
        if critere_selection == "A" :
            Study_Case = "B2_A"
            # st.write(Study_Case)
        elif critere_selection == "C" :
            Study_Case = "B2_C"
            # st.write(Study_Case)
        elif critere_selection == "D" :
            Study_Case = "B2_D"
            # st.write(Study_Case)
    
    
    elif not check_preload  :
        if critere_selection == "A" :
            Study_Case = "B3_A"
            # st.write(Study_Case)
        elif critere_selection == "C" :
            Study_Case = "B3_C"
            # st.write(Study_Case)
        elif critere_selection == "D" :
            Study_Case = "B3_D"
            # st.write(Study_Case)
            
            
            
            
    if "B3" in Study_Case :
        st.write("Moments de flexion dus à une flexion locale par effet levier ?")
        selection1 = st.radio("", ("oui", "non"), horizontal=True, label_visibility="collapsed", key="cas 1")
        
        # saut de ligne
        st.write("\n")
        
        st.write("Entraxe ou distance de l'axe des éléments de serrage au bord de la pièce assemblée dans la direction de l'effort.")
        L = st.text_input("$L [mm]$ :", placeholder = "0.0")   
        L = float(L) if L else 1.0
        
        # saut de ligne
        st.write("\n")
        
        st.write("Epaisseur de la pièce.")
        e = st.text_input("$t [mm]$ :", placeholder = "0.0")
        e = float(e) if e else 1.0
        
        # Traitement des résultats Ansys
        # On met des valeurs par défaut pour les données non nécessaires au cas B3
        adherence_selection = "non"
        F0_selection = "non"
        selection2 = selection1
        F0 = 0.0
        ft = 0.0
        fv = 0.0
        Lambda = 0.0
        T_Results_Ansys_Bilan = traitement_resultats_Ansys(T_Results_Ansys, check_preload, adherence_selection, F0_selection, selection1, L_Donnees_Geo_Boulonnerie_Full, F0, ft, fv, Lambda)
        
    
    else :
        st.write("Valeur du coefficient de rigidité")
        Lambda = st.text_input("$\Lambda [-]$ :", placeholder = "0.0")
        if Lambda : # Vérifier si la valeur n'est pas vide avant de la convertir en float
            try :
                Lambda = float(Lambda)
            except ValueError :
                st.write("")
        #else :
        #    st.write("")
        
        
        # saut de ligne
        st.write("\n")
        
        st.write("Valeur du coefficient de frottement sous tête ou sous écrou.")
        ft = st.text_input("$f' [-]$ :", placeholder = "0.0") 
        if ft :
            try :
                ft = float(ft)
            except ValueError :
                st.write("")

        
        # saut de ligne
        st.write("\n")
        
        st.write("Valeur du coefficient de frottement entre filet en prise.")
        fv = st.text_input("$f [-]$ :", placeholder = "0.0")
        fv = float(fv) if fv else 0.15
        
        # saut de ligne
        st.write("\n")
        
        st.write("Valeur de l'effort de précontrainte à la température $T$.")
        F0 = st.text_input("$F_0 [N]$ :", placeholder = "0.0")
        F0 = float(F0) if F0 else 0.0
        
        # saut de ligne
        st.write("\n")
        
        st.write("$F_0$ pris en compte dans les calculs ANSYS ?")
        F0_selection = st.radio("", ("oui", "non"), horizontal=True, label_visibility="collapsed", key="test")
        
        # saut de ligne
        st.write("\n")
        
        st.write("Efforts extérieurs repris par adhérence ?")
        adherence_selection = st.radio("", ("oui", "non", "tester avec les données saisies"), horizontal=True, label_visibility="collapsed", key="cas test")
        
        # saut de ligne
        st.write("\n")
        
        st.write("Moments de flexion dus à une flexion locale par effet levier ?")
        selection2 = st.radio("", ("oui", "non"), horizontal=True, label_visibility="collapsed", key="cas 2") 
        
    
        # Traitement des résultats Ansys
        T_Results_Ansys_Bilan = traitement_resultats_Ansys(T_Results_Ansys, check_preload, adherence_selection, F0_selection, selection2, L_Donnees_Geo_Boulonnerie_Full, F0, ft, fv, Lambda)
        
        # On met une valeur arbitraire pour e pour que la fonction calculer_contraintes ait toutes ses données d'entrée
        e = 0.0
        
        # On met une valeur arbitraire pour L pour que la fonction calculer_criteres ait toutes ses données d'entrée
        L = 0.0

        # On met la même valeur dans les deux cas par défaut
        selection1 = selection2




    
    # saut de ligne
    st.write("\n")
    
    # saut de ligne
    st.write("\n")
    

    
    st.subheader("Résultats")
    
    L_marge_full = []
    
    # st.write("T_Results_Ansys_Bilan : ", T_Results_Ansys_Bilan)
    for i in range (0, len(T_Results_Ansys_Bilan)) :
        # st.write("T_Results_Ansys_Bilan[i] : ", T_Results_Ansys_Bilan[i])

        if materiau_bolt in L_Acier_Aust :
            B_acier_aust = True 
        else :
            B_acier_aust = False
        
        L_contraintes = calculer_contraintes(T_Results_Ansys_Bilan[i], L_Donnees_Geo_Boulonnerie_Full, e, Study_Case, h, SuminB_T, SyminB_T, SyminP_T, type_boulonnerie, B_acier_aust)
        
        L_Criteres = calculer_criteres(d, SyminB_T, SyminP_T, SuminB_T, SuminP_T, Sm_T, SmB_T, Study_Case, h, L, Le, type_boulonnerie, B_acier_aust)
        
        L_Bilan_Boulon_i = calculer_marges_all_results(L_contraintes, L_Criteres)

        L_marge_full.append(L_Bilan_Boulon_i)



    # Affichage d'un tableau avec une partie des données d'entrée
    # L_Donnees_Geo_Boulonnerie_Full = L_Valeur + [d1, d2, d3, D, round(float(L_prime),2), Dm, a_prime, Dp_prime] 
    
    L_Designation_full = L_Designation + ["Diamètre au sommet d'écrou", "Diamètre à flan de filet", "Diamètre à fond de filet (du noyau)", "Diamètre intérieur du taraudage", "Longueur pour le calcul au cisaillement", "Diamètre moyen sous tête", "Diamètre sur plat de la tête si rondelle", "Diamètre de perçage si rondelle"]
    L_Symbole_full = L_Symbole + ["d1", "df", "dn", "D", "Le'", "Dm", "a'", "Dp'"]
    L_Unite_full = L_Unite + ["[mm]", "[mm]", "[mm]", "[mm]", "[mm]", "[mm]", "[mm]", "[mm]"]
    
    # Création d'un dictionnaire
    D_bolt_geom_data_full = {
        'Désignation' : L_Designation_full,
        'Symbole' : L_Symbole_full,
        'Valeur' : L_Donnees_Geo_Boulonnerie_Full,
        'Unité' : L_Unite_full
        }
    
    # Création du DataFrame pandas à partir du dictionnaire
    df_bolt_geom_data_full = pd.DataFrame(D_bolt_geom_data_full)

    rappel_geom_data_check_box = st.checkbox("Afficher les données géométriques utilisées pour le calcul")
    if rappel_geom_data_check_box :
        st.write(df_bolt_geom_data_full)

        # saut de ligne
        st.write("\n")
        
        # saut de ligne
        st.write("\n")


    
    
    num_boulon = st.number_input("Numéro du boulon dont on veut afficher les résultats", 1, int(len(T_Results_Ansys)))
    
    L_Result_Boulon_i = L_marge_full[num_boulon-1]
    df_bilan = pd.DataFrame(L_Result_Boulon_i[1:], columns=L_Result_Boulon_i[0])
    st.write(df_bilan)    

    
    # On récupère les données des pièces assemblées sous forme d'un tableau DataFrame
    df_assembly_part_data = st.session_state.propriete_mat_pieces_RCCMRx
    
    # On crée le rapport pdf
    pdf_buffer = create_rapport_pdf_rccmrx(type_boulonnerie, df_bolt_geom_data_full, df_Bolt_Material_Data, B_acier_aust, df_assembly_part_data, Study_Case, Lambda, 
                              ft, fv, F0, F0_selection, adherence_selection, selection1, selection2, d, h, Le, SyminP_T, SyminB_T, L, e, T_Results_Ansys_Bilan,
                              critere_selection, L_marge_full, SuminB_T)
    
    
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

    # if st.download_button :
    #     st.success("PDF exporté avec succès")
    
