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
    st.title("Dimensionnement de la boulonnerie selon le SDC-IC")
    st.write("En cours de développement...")