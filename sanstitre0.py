#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 13:19:40 2024

@author: alanbonmort
"""
import streamlit as st
# Ajouter un graphique simple
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import os

# Import des fonctions des modules internes
# from M_Createur_Rapport_PDF import create_pdf_template
from M_Manipulation_Donnees_Materiaux_2 import get_grandeur_T_quelconque, get_donnees_grandeur_fonction_T
from M_Modelisation_Precharge import page_Modelisation_Presserage
from M_Design_SDCIC import page_SDCIC
from M_Design_RCCMRx import page_RCCMRx


# Configuration du titre de la page et du logo
st.set_page_config(page_title="G-MET Bolt", page_icon="Pictures/G-MET-Bolts-Logo-Grand-Detoure.ico")
# st.set_option('deprecation.showPyplotGlobalUse', False)

sidebar = st.sidebar

# Initialiser l'état de l'application
if 'active_page' not in st.session_state:
    st.session_state.active_page = "Modélisation de la précharge"
    
page1 = sidebar.button("Modélisation de la précharge", use_container_width = True)
page2 = sidebar.button("Dimensionnement selon le SDC-IC", use_container_width = True)
page3 = sidebar.button("Dimensionnement selon le RCC-MRx", use_container_width = True)

if page1 :
    st.session_state.active_page = "Modélisation de la précharge"
    
elif page2 : 
    st.session_state.active_page = "Dimensionnement selon le SDC-IC"
    
elif page3 : 
    st.session_state.active_page = "Dimensionnement selon le RCC-MRx"
    
    
    
if st.session_state.active_page == "Modélisation de la précharge" :
    page_Modelisation_Presserage()

elif st.session_state.active_page == "Dimensionnement selon le SDC-IC" :
    page_SDCIC()

elif st.session_state.active_page == "Dimensionnement selon le RCC-MRx" :
    page_RCCMRx()



    
    

