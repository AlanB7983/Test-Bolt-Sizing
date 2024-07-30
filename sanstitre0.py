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

from M_Createur_Rapport_PDF import create_pdf_template


from M_Manipulation_Donnees_Materiaux_2 import get_grandeur_T_quelconque, get_donnees_grandeur_fonction_T


# Fonctions pour le calcul des élongations pour notamment tracer le diagramme des efforts
def elong_bolt_F0(DL) :
    return (Kb*DL+F0)

def elong_pieces_F0(DL) :
    return (-Ka*DL+F0)

def elong_bolt_Fprime(DL) :
    return (Kb*(Fprime/F0)*DL+Fprime)

def elong_pieces_Fprime(DL) :
    return (-Ka*(Fprime/F0)*DL+Fprime)    

def elong_bolt_F0prime(DL) :
    return (Kbprime*DL+F0prime)

def elong_pieces_F0prime(DL) :
    return (-Kaprime*DL+F0prime)   





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


# Configuration du titre de la page et du logo
st.set_page_config(page_title="G-MET Bolt", page_icon="Pictures/G-MET-Bolts-Logo-Grand-Detoure.ico")
# st.set_option('deprecation.showPyplotGlobalUse', False)

# Variables
liste_material = ["304L SS", "316L SS", "660 SS", "Acier Classe 6-8", "Alloy 718"]


# Titre de l'application
st.title("Modélisation de la précharge")



# =============================================================================
# RAPPELS ET OBJECTIFS
# =============================================================================

st.header("RAPPELS ET OBJECTIFS") # Partie

st.write("Le fait de précontraindre un élément de serrage grâce à l'application d'un couple de serrage permet d'améliorer les performances de tenue mécanique de la liaison boulonnées. Le fonctionnement d'une liaison boulonnée précontrainte est relativement complexe. L'intérêt principal d'une liaison boulonnée précontrainte est que les efforts externes, qu'ils soient normaux ou tranchants seront repris par l'élément de serrage. L'évolution des efforts vus par les pièces assemblées et l'élément de serrage dépendent notamment des matériaux et de la géométrie.")
st.write("Les vidéos ci-dessous permettent d'illustrer le mécanisme dans le cas d'un effort extérieur normal et dans le cas d'un effort extérieur tranchant.")


# Chemin vers la vidéo locale
# video_eff_normal = open('C:/Users/alanb/Downloads/RPReplay_Final1717588648.MOV', 'rb')
# video_eff_tranch = open('C:/Users/alanb/Downloads/video_cisaillement.MOV', 'rb')

# video_bytes_eff_normal = video_eff_normal.read()
# video_bytes_eff_tranch = video_eff_tranch.read()

minutes = 5
seconds = 40
start_time = minutes * 60 + seconds
video_url = f"https://youtu.be/XLzTB4KLCxU?i=4t1fLmZBP0D7VOnl={start_time}s"

# Afficher la vidéo dans Streamlit
with st.expander("ILLUSTRATION DU PRINCIPE DE FONCTONNEMENT D'UNE LIAISON BOULONNÉE PRÉCONTRAINTE.") :
    choix_video = st.radio("", ("Cas d'un effort extérieur normal", "Cas d'un effort extérieur tranchant"), horizontal=True)
    if choix_video == "Cas d'un effort extérieur normal" :
        st.write("In developpement")
        # st.video(video_eff_normal.read())
    else :
        st.video(video_url)
    
st.write("L'objectif de ce logiciel est de modéliser le comportement de la liaison boulonnée précontrainte. L'utilisateur pourra notamment :")
st.write("- déterminer les efforts qui transitent réellement dans les pièces assemblées et l'élément de serrage en fonction de l'effort extérieur appliqué") 
st.write("- déterminer les déformations subies par les pièces assemblées et l'élément de serrage en fonction de l'effort extérieur appliqué")
st.write("- prendre en compte un éventuel chargement thermique sur le comportement de la liaison boulonnée")

st.write("Les calculs réalisés sur ce logiciel sont basés sur les recommandations du § A6.2000 du code de dimensionnement RCC-MRx. Ces calculs reposent sur la méthode dite « méthode simplifiée ressort ». Celle-ci consiste à assimiler la liaison boulonnée à l'ensemble de 2 ressorts associés en parallèle, l'un ayant la rigidité $K_a$ des pièces assemblées, l'autre la rigidité $K_b$ de l'élément de serrage. (voir $ A6.2420)")


# Chemin relatif de l'image
image_path = 'Pictures/vocabulaire_assemblage_boulonne.png'

with st.expander("RAPPELS DE VOCABULAIRE") :
    # Vérifiez si le fichier existe
    if os.path.exists(image_path):
        st.image(image_path, caption='Vocabulaire Assemblage Boulonné')
    else:
        st.error(f"L'image '{image_path}' n'a pas été trouvée.")
        # Affichez les fichiers disponibles pour le diagnostic
        st.write("Fichiers disponibles :")
        st.write(os.listdir('.'))
        st.write("Fichiers dans 'Pictures' :")
        st.write(os.listdir('Pictures'))
    # st.image('vocabulaire_assemblage_boulonné.png', caption="Assemblage boulonné", use_column_width=True)


# saut de ligne
st.write("\n")




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
        ll = st.text_input("$l_{l} [mm]$ :", placeholder = "0.0")
        ln = st.text_input("$l_{n} [mm]$ :", placeholder = "0.0")


        
    with col2:
        a = st.text_input("$a [mm]$ :", placeholder = "0.0")
        Dp = st.text_input("$D_p [mm]$ :", placeholder = "0.0")
        De = st.text_input("$D_e [mm]$ :", placeholder = "0.0")
        Le = st.text_input("$L_{e} [mm]$ :", placeholder = "0.0")
        
    with col3:
        st.image("Pictures/Vis_Dimensions.png", use_column_width=True)

    
    # if d and p and ll and ln and a and Dp and De and Le :
    #     try:
    #         d = float(d)
    #         p = float(p)
    #         ll = float(ll)
    #         ln = float(ln)
    #         a = float(a)
    #         Dp = float(Dp)
    #         De = float(De)
    #         Le = float(Le)
    #         # st.write(f"Valeurs converties : {d} et {p}")
    #         st.write("Valeurs converties")
    #     except ValueError:
    #         st.error("Les entrées doivent être des nombres valides.")
    # else:
    #     st.info("Veuillez entrer des valeurs dans les champs ci-dessus.")
    
    
    d = float(d)
    p = float(p)
    ll = float(ll)
    ln = float(ln)
    a = float(a)
    Dp = float(Dp)
    De = float(De)
    Le = float(Le)
    lb = ll + ln + Le
    
    L_Designation = ["Diamètre nominal", "Pas", "Longueur du fût lisse", "Longueur du filetage non en prise \n avec les pièces assemblées",
                     "Diamètre sur le plat de la tête", "Diamètre de perçage", "Longueur d'engagement des filets \n en prise", "Etendue des pièces assemblées autour \n de l'axe de l'élément de serrage"]
    L_Symbole = ["d", "p", "ll", "ln", "a", "Dp", "Le", "De"]
    L_Valeur = [d, p, ll, ln, a, Dp, Le, De]
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


    with col2: 
        De = st.text_input("$D_e [mm]$ :", placeholder = "0.0")
        a = st.text_input("$a [mm]$ :", placeholder = "0.0")
        Dp = st.text_input("$D_p [mm]$ :", placeholder = "0.0")

        
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

elif selection == "Goujon" :
    with col1:
        d = st.text_input("$d [mm]$ :", placeholder = "0.0")
        p = st.text_input("$p [mm]$ :", placeholder = "0.0")
        ln1 = st.text_input("$l_{n1} [mm]$ :", placeholder = "0.0")
        ll = st.text_input("$l_{l} [mm]$ :", placeholder = "0.0")
        ln2 = st.text_input("$l_{n2} [mm]$ :", placeholder = "0.0")

    with col2: 
        dl = st.text_input("$d_l [mm]$ :", placeholder = "0.0")
        De = st.text_input("$D_e [mm]$ :", placeholder = "0.0")
        a = st.text_input("$a [mm]$ :", placeholder = "0.0")
        Dp = st.text_input("$D_p [mm]$ :", placeholder = "0.0")
        
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
    lb = ln1 + ln2 + ll + Le
    

elif selection == "Lacet" :
    with col1:
        d = st.text_input("$d [mm]$ :", placeholder = "0.0")
        p = st.text_input("$p [mm]$ :", placeholder = "0.0")
        ln1 = st.text_input("$l_{n1} [mm]$ :", placeholder = "0.0")
        ll = st.text_input("$l_{l} [mm]$ :", placeholder = "0.0")
        ln2 = st.text_input("$l_{n2} [mm]$ :", placeholder = "0.0")

    with col2: 
        dl = st.text_input("$d_l [mm]$ :", placeholder = "0.0")
        De = st.text_input("$D_e [mm]$ :", placeholder = "0.0")
        a = st.text_input("$a [mm]$ :", placeholder = "0.0")
        Dp = st.text_input("$D_p [mm]$ :", placeholder = "0.0")
        
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
    lb = ln1 + ln2 + ll + Le

    
dn = d-1.2268*p


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

# =============================================================================
# Données liées aux pièces assemblées
# =============================================================================

st.write("- ##### *Données liées aux pièces assemblées*")

# Initialiser le DataFrame vide
if 'test_data' not in st.session_state:
    st.session_state.test_data = pd.DataFrame(columns=['Numéro de la pièce assemblée', 'Longueur [mm]', 'Matériau'])

# Saisies utilisateur pour ajouter des données
saisie_col1, saisie_col2 = st.columns([1, 1])
with saisie_col1 :
    Longueur = st.number_input('Longueur [mm]', min_value=0.0, step=0.1)
with saisie_col2 :
    materiau = st.selectbox('Matériau', liste_material)

but_col1, but_col2, but_col3 = st.columns([1,1,4])
with but_col1:
    # Bouton pour ajouter les données au DataFrame
    if st.button('Ajouter', use_container_width = True):
        nombre_lignes = st.session_state.test_data.shape[0]
        num_piece = 'Pièce assemblée n°' + str(int(nombre_lignes)+1)
        # new_data = {'Numéro de la pièce assemblée' : num_piece, 'Longueur [mm]' : float(Longueur), 'Matériau' : materiau}
        # st.write("nombre de lignes : ", nombre_lignes)
        # st.write("numéro pièce : ", num_piece)
        # st.write("new data : ", new_data)
        # st.session_state.test_data.append(new_data, ignore_index=True)
        new_data = pd.DataFrame({'Numéro de la pièce assemblée': [num_piece], 'Longueur [mm]': [float(Longueur)], 'Matériau': [materiau]})
        st.session_state.test_data = pd.concat([st.session_state.test_data, new_data], ignore_index=True)
with but_col2:
    if st.button('Effacer', use_container_width = True):
        st.session_state.test_data = pd.DataFrame(columns=['Numéro de la pièce assemblée', 'Longueur [mm]', 'Matériau'])

# Afficher les données sous forme de tableau
st.dataframe(st.session_state.test_data)

longueur_piece = st.session_state.test_data['Longueur [mm]'].tolist()
materiau_piece = st.session_state.test_data['Matériau'].tolist()


# Calcul de L
L = 0
for i in range(0, len(longueur_piece)) :
    L = L + longueur_piece[i]
st.write("La longueur total des pièces assemblées vaut $L$ = " + str(round(float(L),1)) + " mm.")

# saut de ligne
st.write("\n")

    
# =============================================================================
# Détails sur les données géométriques à remplir
# =============================================================================

with st.expander("Détails sur les données géométriques à saisir") :
    # st.info("- $d$ : diamètre nominal\n- $p$ : pas\n- $l_l$ : longueur du fût lisse\n- $l_n$ : longueur du filetage non en prise avec les pièces assemblées\n- $a$ : Diamètre sur plat de la tête\n- $D_p$ : Diamètre de perçage\n- $l_{a1}$ : Longueur de la pièce assemblée 1\n- $l_{a2}$ : Longueur de la pièce assemblée 2\n- $l_{a3}$ : Longueur de la pièce assemblée 3") 
    st.write("- $d$ : Diamètre nominal")
    st.write("- $p$ : Pas") 
    st.write("- $l_l$ : Longueur du fût lisse") 
    st.write("- $l_{ni}$ : Longueur du filetage non en prise avec les pièces assemblées") 
    st.write("*Remarque : Dans le cas de goujons ou lacets par exemple, il peut y avoir plusieurs zones de filetage non en prise avec les pièces assemblées.*")
    st.write("- $d_l$ : Diamètre du fût lisse")
    st.write("- $a$ : Diamètre sur plat de la tête")
    st.write("- $D_p$ : Diamètre de perçage")
    st.write("- $l_{aj}$ : Longueur de la pièce assemblée j")
    st.write("*Remarque : Les rondelles doivent être considérées comme une pièce assemblée. D'après le § A6.2423 du RCC MRx, dans le cas de vis et de goujons, la longueur à prendre en compte pour la pièce taraudée sera égale à 40 % du diamètre nominal (0,4 d).*")
    st.write("- $L_e$ : Longueur d'engagement des filets en prise")
    st.write("- $D_e$ : l'étendue des pièces assemblées autour de l'axe de l'élément de serrage") 
    De_col1, De_col2 = st.columns([2, 3])
    with De_col1 :
        st.write("*D'après le § A6.2850 du RCC MRx, $D_e$ est le diamètre du plus grand cercle pouvant être inscrit dans le plan des pièces assemblées, sans qu'il y ait interférence avec un cercle homologue d'un élément de serrage voisin, ni intersection avec l'un quelconque des bords libres des pièces à assembler.*")
    with De_col2 :
        st.image("Pictures/Definition de De.png", caption="", use_column_width=True)


# saut de ligne
st.write("\n")
st.write("\n")


# =============================================================================
# Données de serrage
# =============================================================================

st.subheader("Données de serrage")
    
press_col1, press_col2 = st.columns([1, 1])
with press_col1:
    F0 = st.text_input("Donner la valeur du présserrage initial $F_0$ en N :", placeholder = "10000.0")
with press_col2:
    T0 = st.text_input("Donner la température initiale $T_0$ en °C à laquelle le présserrage a été effectué :", placeholder = "20.0")
    



L_Ea = []
for i in range(0, len(materiau_piece)) :
    # st.write(materiau_piece[i])
    F_Assembly_Part_Material_Properties = "Material_Properties/" + materiau_piece[i] + '.csv'
    L_Assembly_Part_Material_Properties = traduire_fichier_to_liste(F_Assembly_Part_Material_Properties)

    # On trouve le numéro de la colonne correspondant à la grandeur renseignée par l'utilisateur
    # j = 0
    # while L_Assembly_Part_Material_Properties[0][j] != "E" and j < len(L_Assembly_Part_Material_Properties[0]) :
    #     st.write("j = ", j)
    #     st.write("L_Assembly_Part_Material_Properties[0][j] : ", L_Assembly_Part_Material_Properties[0][j])
    #     st.write("len(L_Assembly_Part_Material_Properties[0]) : ", len(L_Assembly_Part_Material_Properties[0]))
    #     j = j + 1
    #     num_colonne = j

    
    Ea = float(get_grandeur_T_quelconque('E', L_Assembly_Part_Material_Properties, float(T0)))
    L_Ea.append(Ea)

Eb = float(get_grandeur_T_quelconque('E', L_Bolt_Material_Properties, float(T0)))

# st.write("le module de Young de la bolt vaut : ", Eb)
# st.write("le module de Young des pièces assemblées vaut : ", Ea)

# CALCUL DE LAMBDA
# Calcul de Kb
if selection == "Boulon" or selection == "Vis" :
    Kb = (np.pi*Eb/4)/(0.4*d*((1/(d**2))+(1/(dn**2)))+(ll/(d**2))+(ln/(dn**2)))
else :
    Kb = (np.pi*Eb/4)/((0.8*d/(dn**2))+(ln1/(dn**2))+(ln2/(dn**2))+(ll/(dn**2)))
    
# Calcul de Ka
denom = 0.0
for i in range(0, len(materiau_piece)) :
    denom = denom + longueur_piece[i]/L_Ea[i]
    
# st.write("denom = ", denom)
if float(De) <= float(a) :
    cas = 'cas 1'
    Ka = (np.pi/4)*(De**2 - Dp**2)/denom
    
elif float(De) > float(a) and float(De) <= 3*float(a) :
    cas = 'cas 2'
    Ka = (np.pi/4)*((a**2 - Dp**2)+0.5*((De/a)-1)*((a*L/5)+(L**2)/100))/(denom)
    
else :
    cas = 'cas 3'
    Ka = (np.pi/4)*((a+(L/10))**2 - Dp**2)/(denom)





# =============================================================================
# Prise en compte de la thermique
# =============================================================================

st.subheader("Prise en compte de la thermique")

if 'Tb' not in st.session_state:
    st.session_state.Tb = '200.0'
    
if 'Ta' not in st.session_state:
    st.session_state.Ta = '200.0'
    
checked_thq = st.checkbox("Prise en compte des chargements thermiques")

if checked_thq :

    thq_col1, thq_col2 = st.columns([1, 1])
    with thq_col1:
        st.session_state.Tb = st.text_input("Valeur de la température moyenne de l'élément de serrage établie suite à l'application d'un chargement thermique, noté $T_b$, en °C :", st.session_state.Tb)
    with thq_col2:
        st.session_state.Ta = st.text_input("Valeur de la température moyenne des pièces assemblées établie suite à l'application d'un chargement thermique, noté $T_a$, en °C :", st.session_state.Ta)
        

    Tb = st.session_state.Tb
    Ta = st.session_state.Ta

    Ebprime = float(get_grandeur_T_quelconque('E', L_Bolt_Material_Properties, float(Tb)))
    
    L_Eaprime = []
    for i in range(0, len(materiau_piece)) :
        # F_Assembly_Part_Material_Properties = "Material_Properties/" + materiau_piece[i] + '.csv'
        # L_Assembly_Part_Material_Properties = traduire_fichier_to_liste(F_Assembly_Part_Material_Properties)
        Eaprime = float(get_grandeur_T_quelconque('E', L_Assembly_Part_Material_Properties, float(Ta)))
        L_Eaprime.append(Eaprime)

    
    # Calcul de Kb
    if selection == "Boulon" or selection == "Vis" :
        Kbprime = (np.pi*Ebprime/4)/(0.4*d*((1/(d**2))+(1/(dn**2)))+(ll/(d**2))+(ln/(dn**2)))
    else :
        Kbprime = (np.pi*Ebprime/4)/((0.8*d/(dn**2))+(ln1/(dn**2))+(ln2/(dn**2))+(ll/(dn**2)))
        
    # Calcul de Ka
    denom = 0.0
    for i in range(0, len(materiau_piece)) :
        denom = denom + longueur_piece[i]/L_Eaprime[i]
    if float(De) <= float(a) :
        cas = 'cas 1'
        Kaprime = (np.pi/4)*(De**2 - Dp**2)/(denom)
        
    elif float(De) > float(a) and float(De) <= 3*float(a) :
        cas = 'cas 2'
        Kaprime = (np.pi/4)*((a**2 - Dp**2)+0.5*((De/a)-1)*((a*L/5)+(L**2)/100))/(denom)
        
    else :
        cas = 'cas 3'
        Kaprime = (np.pi/4)*((a+(L/10))**2 - Dp**2)/(denom)
    
    
    alpha_b = float(get_grandeur_T_quelconque('Alpha_m', L_Bolt_Material_Properties, float(Tb)))*10**(-6) #coefficient de dilatation moyen de l'élément de serrage
    L_alpha_a = [] # Liste contenant l'ensemble des valeurs de alpha_a pour chacunes des pièces assemblées
    for i in range(0, len(materiau_piece)) :
        # F_Assembly_Part_Material_Properties = D_Material_Properties + materiau_piece[i] + '.csv'
        # L_Assembly_Part_Material_Properties = traduire_fichier_to_liste(F_Assembly_Part_Material_Properties)
        alpha_a = float(get_grandeur_T_quelconque('Alpha_m', L_Assembly_Part_Material_Properties, float(Ta)))*10**(-6)
        L_alpha_a.append(alpha_a)

    
    Fprime = (Kaprime*Kbprime/(Kaprime + Kbprime))*((Ka + Kb)/(Kb*Ka))*float(F0)
    Temp = 0
    for i in range(0, len(L_alpha_a)) :
        Temp = Temp + longueur_piece[i]*L_alpha_a[i]
    Qi = (Kaprime*Kbprime/(Kaprime + Kbprime))*(Temp*(float(Ta)-float(T0))-float(lb)*alpha_b*(float(Tb)-float(T0)))
    F0prime = Qi + Fprime
    
    # On récupère les valeurs des grandeurs qui nous intéress lorsque la thermique est activée pour pouvoir les transmettre facilement à la fonction qui permet de générer un rapport
    L_Data_thq = [round(float(F0), 0), round(float(Fprime), 0), round(float(Qi), 0), round(float(F0prime), 0), round(float(F0)/float(Kb), 3), round(float(F0)/float(Ka), 3), round(float(F0prime)/float(Kbprime), 3), round(float(F0prime)/float(Kaprime), 3)]
    

    # Affichage des propriétés thermiques des différents matériaux
    L_alpha_a_V2 = [round(x * 10**(6),1) for x in L_alpha_a]
    L_print_alpha = [round(alpha_b*10**(6),1)] + L_alpha_a_V2 # On rassemble les valeurs de alpha pour la bolt (alpha_b) et pour les pièces assemblées (L_alpha_a_V2) en mettant dans les bonnes unités pour l'affichage
    L_print_E = [Ebprime] + L_Eaprime
    L_print_Temp = [float(Tb)] + [float(Ta)]*(len(L_print_alpha)-1)
    L_print_elem = ["Elément de serrage"] + ["Pièces assemblées"]*(len(L_print_alpha)-1)
    L_print_material = [str(materiau_bolt)] + materiau_piece
    D_thermal_property_assembly_parts = {
        'Matériau' : L_print_material,
        'Elément correspondant' : L_print_elem,
        'Température [°C]' : L_print_Temp,
        "Module d'Young [MPa]" : L_print_E,
        "Coefficient de dilatation\n thermique moyen [E-6/°C]" : L_print_alpha
        }
    df_thermal_property_assembly_parts = pd.DataFrame(D_thermal_property_assembly_parts)
    
    # On supprime la première colonne avec les index
    # df_thermal_property_assembly_parts.reset_index(drop=True, inplace=True)

    st.dataframe(df_thermal_property_assembly_parts)
    

    
# =============================================================================
# RESULTATS 
# =============================================================================

# saut de ligne
st.write("\n")
# saut de ligne
st.write("\n")

st.header("RÉSULTATS")

# Créer des onglets dans la barre latérale
# onglet_outil_calcul = st.radio("Navigation", ["Modélisation de ma précharge", "Dimensionnement selon le SDC-IC"])



        
# On calcule Lambda et on affiche le résultat
Lambda = 0.5*Kb/(Ka + Kb)

st.write("La valeur du coefficient de rigidité est $\Lambda$ = " + str(round(Lambda, 2)))

# On affiche le détail du calcul de la valeur de Lambda dans un expander
with st.expander("Détails sur le calcul de la valeur de $\Lambda$") :
    st.write("La formule utilisée pour le calcul de $\Lambda$ est : ")
    st.write("$\Lambda = \dfrac{\zeta K_b}{K_a + K_b}$")
    st.write("avec : ")
    st.write("- $K_b$ et $K_a$ respectivement les rigidités de l'élément de serrage et des pièces assemblées à la température $T_0$ qui dépendent notamment de la géométrie et des matériaux, et dont les formules sont explicités au § A6.2850 du RCC MRx.")
    lmbda_col1, lmbda_col2 = st.columns([1, 1])
    with lmbda_col1:
        st.write("- $\zeta$ le facteur correctif pour tenir compte d'une application du chargement de l'intérieur de la matière et non de la peau, comme explicité sur la figure ci-contre.")
    with lmbda_col2:
        st.image("Pictures/Detail_Calcul_Lambda.png", caption="", use_column_width=True)

# saut de ligne
st.write("\n")


        
        
        
# =============================================================================
# SI LA THMERIQUE EST ACTIVEE
# =============================================================================

if checked_thq :
    # On calcule et on affiche la valeur de l'effort de décollement
    Nedecollement = float(F0prime)/(1-float(Lambda)) # On en déduit l'effort de décollement
    st.write("La valeur de l'effort de décollement est $N_{e,décollement} = $ " + str(round(Nedecollement, 0)) + ' $N$')
    
    # saut de ligne
    st.write("\n")
    
    # On donne la valeur de F0' en précisant si l'assemblage boulonné subit un accroissement ou une diminution du préserrage
    if Qi > 0 :
        st.write("L'assemblage boulonné subit un accroissement du préserrage. La valeur du préserrage à chaud vaut alors $F'_0$ = " + str(round(float(F0prime), 0)) + " N.")
    else :
        st.write("L'assemblage boulonné subit une diminution du préserrage. La valeur du préserrage à chaud vaut alors $F'_0$ = " + str(round(float(F0prime), 0)) + " N.")

    # saut de ligne
    st.write("\n")
    
    # On affiche l'ensemble des résultats dans un tableau Panda
    results_with_thq = {
        'Désignation' : ["Effort de presserrage à T_0", "Coefficient de rigidité", "Effort de décollement", "Elongation de l'élément de serrage du à F_0", "Elongation des pièces assemblées du à F_0", "Effort de presserrage du à la modification de K_b et K_a", "Effort axial engendré par les chargements thermiques", "Effort de presserrage engendré par les chargements thermiques", "Elongation de l'élément de serrage du à F'_0", "Elongation des pièces assemblées du à F'_0"],
        'Symbole' : ["F_0", "Lambda", "Ne,décollement", "\Delta L_b", "\Delta L_a", "F'", "Q_i", "F'_0", "\Delta L'_b", "\Delta L'_a"],
        'Valeur' : [round(float(F0), 0), round(float(Lambda), 2), round(float(Nedecollement), 0), round(float(F0)/float(Kb), 3), round(float(F0)/float(Ka), 3), round(float(Fprime), 0), round(float(Qi), 0), round(float(F0prime), 0), round(float(F0prime)/float(Kbprime), 3), round(float(F0prime)/float(Kaprime), 3)],
        'Unité' : ["[N]", "[-]", "[N]", "[mm]", "[mm]", "[N]", "[N]", "[N]", "[mm]", "[mm]"]
        }
    df_results_with_thq = pd.DataFrame(results_with_thq)
    
    with st.expander("Détails des résultats") :
        st.dataframe(df_results_with_thq)
    
    # saut de ligne
    st.write("\n")
    # saut de ligne
    st.write("\n")
        
        
else :
    # On calcule et on affiche la valeur de l'effort de décollement
    Nedecollement = float(F0)/(1-float(Lambda))
    st.write("La valeur de l'effort de décollement est $N_{e,décollement} = $ " + str(round(Nedecollement, 0)) + ' $N$')
    
    # saut de ligne
    st.write("\n")
    
    # On affiche l'ensemble des résultats dans un tableau Panda
    results_without_thq = {
        'Désignation' : ["Effort de presserrage à T_0", "Coefficient de rigidité", "Effort de décollement", "Elongation de l'élément de serrage du à F_0", "Raccourcissement des pièces assemblées du à F_0"],
        'Symbole' : ["F_0", "Lambda", "Ne,décollement", "Delta Lb", "Delta La"],           
        'Valeur' : [round(float(F0), 0), round(float(Lambda), 2), round(float(Nedecollement), 0), round(float(F0)/float(Kb), 3), round(float(F0)/float(Ka), 3)],
        'Unité' : ["[N]", "[-]", "[N]", "[mm]", "[mm]"]
        }
    df_results_without_thq = pd.DataFrame(results_without_thq)

    with st.expander("Détails des résultats") :
        st.dataframe(df_results_without_thq)
        st.image("Pictures/Interpretation Diagramme F0.png", caption = "Interprétation du diagramme de chargement", use_column_width = True)
    
    # saut de ligne
    st.write("\n")
    # saut de ligne
    st.write("\n")
        
           
# Initialiser l'état de l'application
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Evolution des efforts"
    
onglet_col1, onglet_col2, onglet_col3 = st.columns([1,1,1.5])

with onglet_col1 :  
    onglet1 = st.button("Evolution des efforts")
    if onglet1 :
        st.session_state.active_tab = "Evolution des efforts"
    
with onglet_col2 : 
    onglet2 = st.button("Efforts et élongations")
    if onglet2 :
        st.session_state.active_tab = "Efforts et élongations"



        
# =============================================================================
# SI LA THMERIQUE EST ACTIVEE
# =============================================================================
if checked_thq :        
        
    # Si l'utilisateur choisie l'onglet "Evolution des efforts"
    if st.session_state.active_tab == "Evolution des efforts" :
        
        # L'utilisateur peut choisir de prendre en compte la compression en cochant la case
        checked_compression_2 = st.checkbox("Prise en compte des efforts de compression")
        
        # Si on ne prends pas en compte la compression
        if not checked_compression_2 :
            
            # On prépare le graphique
            Ne = np.linspace(0, 2*int(float(F0)), 100)
            Ne = Ne.tolist()
            Nb = []
            Na = []
            Nbinfwithout_thq = []
            Nbinfwith_thq = []
            
            # On calcule les valeurs de Nb et Na en fonction de l'effort exterieur et des valeurs de Lambda et F0prime obtenues
            for i in range(0, len(Ne)) :
                if float(F0prime)-(1-float(Lambda))*float(Ne[i]) > 0.0 :
                    Nb.append(float(F0prime) + float(Lambda)*float(Ne[i]))
                    Na.append(float(F0prime)-(1-float(Lambda))*float(Ne[i]))
            
                else : 
                    Nb.append(float(Ne[i]))
                    Na.append(0.0)
            
            for i in range(0, len(Ne)) :
                if float(Ne[i]) <= float(F0prime) :        
                    Nbinfwithout_thq.append(float(F0prime))
                else :
                    Nbinfwithout_thq.append(float(Ne[i]))
            
            for i in range(0, len(Ne)) :
                if float(Ne[i]) <= float(F0) :        
                    Nbinfwith_thq.append(float(F0))
                else :
                    Nbinfwith_thq.append(float(Ne[i]))
                
            # On crée la Figure
            fig2 = go.Figure()
            
            fig2.add_trace(go.Scatter(x=Ne, y=Nb, mode='lines', name=r'$N_b$', line = dict(color = '#C00000', width = 1)))
            fig2.add_trace(go.Scatter(x=Ne, y=Na, mode='lines', name=r'$N_a$', line = dict(color = '#002060', width = 1)))
            fig2.add_trace(go.Scatter(x=Ne, y=Nbinfwithout_thq, mode='lines', name=r"$N_{b,infiniment rigide}$", line = dict(color = '#C55A11', width = 1, dash = 'dot')))
            fig2.add_trace(go.Scatter(x=Ne, y=Nbinfwith_thq, mode='lines', name=r"$N_{b,infiniment rigide à T_0}$", line = dict(color = '#C55A11', width = 1, dash = 'dot')))
            
            # On personnalise l'affichage du graphe
            fig2.update_layout(
                title = dict(text = "Evolution de l'effort dans la liaison boulonnée en fonction de l'effort extérieur", x = 0.5, xanchor = 'center'),
                xaxis=dict(
                    title = dict(text = r'$N_e [N]$', font = dict(color = 'black')),
                    showline=True,  # Afficher la barre de l'axe X
                    linecolor='black',  # Couleur de la barre de l'axe X
                    linewidth=1,  # Largeur de la barre de l'axe X
                    tickformat=',.0f',
                    tickfont=dict(color='black'),
                    minor=dict(ticks="outside", ticklen=1, tickcolor='black')
                    ),
                yaxis=dict(
                    title = dict(text = r'$N [N]$', font = dict(color = 'black')),
                    showline=True,  # Afficher la barre de l'axe Y
                    linecolor='black',  # Couleur de la barre de l'axe Y
                    linewidth=1,  # Largeur de la barre de l'axe Y
                    tickformat=',.0f',
                    tickfont=dict(color='black'),
                    minor=dict(ticks="outside", ticklen=1, tickcolor='black')
                    ),
                legend=dict(
                    x=0,  # Position horizontale de la légende (0 est tout à gauche)
                    y=1,  # Position verticale de la légende (1 est tout en haut)
                    borderwidth=1,  # Largeur de la bordure de la légende
                ),
            )
            
            # Afficher le graphique dans Streamlit
            st.plotly_chart(fig2)

            
            # Sauvegarder le graphe en tant qu'image
            save_path = "Temp/Evolution des efforts avec thq.png"
            save_dir = os.path.dirname(save_path)

            # Vérifiez si le répertoire existe, sinon, créez-le
            # if not os.path.exists(save_dir):
            #     st.info("Dossier Temp crée avec succès.")
            #     os.makedirs(save_dir)


            # Exportation de l'image
            # try:
            #     fig2.write_image(save_path, scale=4)
            #     st.info("Image saved successfully.")
            # except Exception as e:
            #     st.info(f"Error saving image: {e}")
            
            fig2.write_image(save_path, scale=4)
            
            
            
            # On ajouter un curseur pour que l'utilisaeur puisse déterminer la valeur de Nb et Na en fonction de Ne choisi
            st.write("Sélectionnez la valeur de l'effort extérieur $N_e$ en N")
            Next = st.slider("", round(int(-2.0*float(F0prime)),-2), round(int(2.0*float(F0prime)),-2), 0, step = int(100), label_visibility="collapsed")
            res_col1, res_col2 = st.columns([1, 1])
            
            # On récupère l'effort Nb et Na résultant de l'effort Ne appliqué
            if float(F0prime) - (1-float(Lambda))*float(Next) > 0 :
                Nb_Ne = float(F0prime) + float(Lambda)*float(Next)
                Na_Ne = float(F0prime) - (1-float(Lambda))*float(Next)
            else :
                Nb_Ne = float(Next)
                Na_Ne = 0.0
                
            with res_col1:
                st.write("L'effort repris par l'élément de serrage vaut")
                st.write("$N_b$ = " + str(round(Nb_Ne,0)) + " $N$")
            with res_col2:
                st.write("L'effort repris par les pièces assemblées vaut")
                st.write("$N_a$ = " + str(round(Na_Ne,0)) + " $N$")
                
                
        
        #Si on prend en compte la compression
        else :
            # On prépare le graphique
            Ne = np.linspace(-2*int(float(F0)), 2*int(float(F0)), 100)
            Ne = Ne.tolist()
            Nb = []
            Na = []
            Nbinfwithout_thq = []
            Nbinfwith_thq = []
            
            # On calcule les valeurs de Nb et Na en fonction de l'effort exterieur et des valeurs de Lambda et F0prime obtenues
            for i in range(0, len(Ne)) :
                if float(Ne[i]) < 0.0 : # Si Ne est négatif (compression)
                    if float(F0prime) + float(Lambda)*float(Ne[i]) < 0 : # Si l'effort de la bolt est nul
                        Nb.append(0.0)
                        Na.append(float(F0prime)-(1-float(Lambda))*float(Ne[i]))
                    else :
                        Nb.append(float(F0prime) + float(Lambda)*float(Ne[i]))
                        Na.append(float(F0prime)-(1-float(Lambda))*float(Ne[i]))
                        
                else : # Si Ne est positif (traction)
                    if float(F0prime)-(1-float(Lambda))*float(Ne[i]) > 0.0 :
                        Nb.append(float(F0prime) + float(Lambda)*float(Ne[i]))
                        Na.append(float(F0prime)-(1-float(Lambda))*float(Ne[i]))
                
                    else : 
                        Nb.append(float(Ne[i]))
                        Na.append(0.0)
            
            for i in range(0, len(Ne)) :
                if float(Ne[i]) <= float(F0prime) :        
                    Nbinfwithout_thq.append(float(F0prime))
                else :
                    Nbinfwithout_thq.append(float(Ne[i]))
            
            for i in range(0, len(Ne)) :
                if float(Ne[i]) <= float(F0) :        
                    Nbinfwith_thq.append(float(F0))
                else :
                    Nbinfwith_thq.append(float(Ne[i]))
                
            # On crée la Figure
            fig2 = go.Figure()
            
            fig2.add_trace(go.Scatter(x=Ne, y=Nb, mode='lines', name=r'$N_b$', line = dict(color = '#C00000', width = 1)))
            fig2.add_trace(go.Scatter(x=Ne, y=Na, mode='lines', name=r'$N_a$', line = dict(color = '#002060', width = 1)))
            fig2.add_trace(go.Scatter(x=Ne, y=Nbinfwithout_thq, mode='lines', name=r"$N_{b,infiniment rigide}$", line = dict(color = '#C55A11', width = 1, dash = 'dot')))
            fig2.add_trace(go.Scatter(x=Ne, y=Nbinfwith_thq, mode='lines', name=r"$N_{b,infiniment rigide à T_0}$", line = dict(color = '#C55A11', width = 1, dash = 'dot')))
            
            # On personnalise l'affichage
            fig2.update_layout(
                title = dict(text = "Evolution de l'effort dans la liaison boulonnée en fonction de l'effort extérieur", x = 0.5, xanchor = 'center'),
                xaxis=dict(
                    title = dict(text = r'$N_e [N]$', font = dict(color = 'black')),
                    showline=True,  # Afficher la barre de l'axe X
                    linecolor='black',  # Couleur de la barre de l'axe X
                    linewidth=1,  # Largeur de la barre de l'axe X
                    tickformat=',.0f',
                    tickfont=dict(color='black'),
                    minor=dict(ticks="outside", ticklen=1, tickcolor='black')
                    ),
                yaxis=dict(
                    title = dict(text = r'$N [N]$', font = dict(color = 'black')),
                    showline=True,  # Afficher la barre de l'axe Y
                    linecolor='black',  # Couleur de la barre de l'axe Y
                    linewidth=1,  # Largeur de la barre de l'axe Y
                    tickformat=',.0f',
                    tickfont=dict(color='black'),
                    minor=dict(ticks="outside", ticklen=1, tickcolor='black')
                    ),
                legend=dict(
                    x=0.5,  # Position horizontale de la légende (0 est tout à gauche)
                    y=1,  # Position verticale de la légende (1 est tout en haut)
                    borderwidth=1,  # Largeur de la bordure de la légende
                ),
            )
            
            # Afficher le graphique dans Streamlit
            st.plotly_chart(fig2)

            # Sauvegarder le graphe en tant qu'image
            save_path = "Temp/Evolution des efforts avec thq.png"
            save_dir = os.path.dirname(save_path)
            
            fig2.write_image(save_path, scale=4)
            
            
            
            # Ajouter un curseur
            st.write("Sélectionnez la valeur de l'effort extérieur $N_e$ en N")
            Next = st.slider("", round(int(-2.0*float(F0prime)),-2), round(int(2.0*float(F0prime)),-2), 0, step = int(100), label_visibility="collapsed")
            res_col1, res_col2 = st.columns([1, 1])
            
            # On récupère l'effort Nb et Na résultant de l'effort Ne appliqué
            if float(F0prime) - (1-float(Lambda))*float(Next) > 0 :
                Nb_Ne = float(F0prime) + float(Lambda)*float(Next)
                Na_Ne = float(F0prime) - (1-float(Lambda))*float(Next)
            else :
                Nb_Ne = float(Next)
                Na_Ne = 0.0
                
            with res_col1:
                st.write("L'effort repris par l'élément de serrage vaut")
                st.write("$N_b$ = " + str(round(Nb_Ne,0)) + " $N$")
            with res_col2:
                st.write("L'effort repris par les pièces assemblées vaut")
                st.write("$N_a$ = " + str(round(Na_Ne,0)) + " $N$")
                
                
                
    # Si l'utilisateur choisie l'onglet "Efforts et élongations"                
    elif st.session_state.active_tab == "Efforts et élongations" :
        
        F0 = float(F0)
        
        # Créer une plage de valeurs pour x
        x1 = np.linspace(-F0/Kb, 0, 100)
        x2 = np.linspace(0, F0/Ka, 100)
        x3 = np.linspace(-Fprime/Kbprime, 0, 100)
        x4 = np.linspace(0, Fprime/Kaprime, 100)
        x5 = np.linspace(-F0prime/Kbprime, 0, 100)
        x6 = np.linspace(0, F0prime/Kaprime, 100)
        
        # Calculer les valeurs de f(x) pour ces valeurs de x
        y1 = elong_bolt_F0(x1)
        y2 = elong_pieces_F0(x2)
        y3 = elong_bolt_Fprime(x3)
        y4 = elong_pieces_Fprime(x4)
        y5 = elong_bolt_F0prime(x5)
        y6 = elong_pieces_F0prime(x6)
        
        # On convertie en liste et on rassemble les intervalles correspondant à une même courbe
        x1 = x1.tolist()
        x2 = x2.tolist()
        xF0 = x1 + x2
        x3 = x3.tolist()
        x4 = x4.tolist()
        xFprime = x3 + x4
        x5 = x5.tolist()
        x6 = x6.tolist()
        xF0prime = x5 + x6
        
        y1 = y1.tolist()
        y2 = y2.tolist()
        yF0 = y1 + y2
        y3 = y3.tolist()
        y4 = y4.tolist()
        yFprime = y3 + y4
        y5 = y5.tolist()
        y6 = y6.tolist()
        yF0prime = y5 + y6
        
        
        # On crée le graphe
        fig3 = go.Figure()
    
        fig3.add_trace(go.Scatter(x=xF0, y=yF0, mode='lines', name="du à F0", line = dict(color = '#C00000', width = 1)))
        fig3.add_trace(go.Scatter(x=xFprime, y=yFprime, mode='lines', name="du à F'", line = dict(color = '#002060', width = 1)))
        fig3.add_trace(go.Scatter(x=xF0prime, y=yF0prime, mode='lines', name="du à F'0", line = dict(color = '#C55A11', width = 1)))
        
        
        # Mettre à jour les axes pour définir les limites
        borneX_min = min(-1.2*F0/Kb, -1.2*F0prime/Kbprime)
        borneX_max = max(1.2*F0/Ka, 1.2*F0prime/Kaprime)
        borneY_max = max(1.2*F0, 1.2*Fprime, 1.2*F0prime)
        fig3.update_xaxes(title_text='x', range=[borneX_min, borneX_max])  # Définir la plage de l'axe X
        fig3.update_yaxes(title_text='f(x)', range=[0, borneY_max])  # Définir la plage de l'axe Y
        
        
        # On personnalise le graphe
        fig3.update_layout(
            title = dict(text = "Diagramme de chargement d'une liaison boulonnée", x = 0.5, xanchor = 'center'),
            xaxis=dict(
                title = dict(text = r'$\Delta_L [mm]$', font = dict(color = 'black')),
                showline=True,  # Afficher la barre de l'axe X
                linecolor='black',  # Couleur de la barre de l'axe X
                linewidth=1,  # Largeur de la barre de l'axe X
                tickformat='.3f',
                tickfont=dict(color='black'),
                minor=dict(ticks="outside", ticklen=1, tickcolor='black')
                ),
            yaxis=dict(
                title = dict(text = r'$N [N]$', font = dict(color = 'black')),
                showline=True,  # Afficher la barre de l'axe Y
                linecolor='black',  # Couleur de la barre de l'axe Y
                linewidth=1,  # Largeur de la barre de l'axe Y
                tickformat=',.0f',
                tickfont=dict(color='black'),
                minor=dict(ticks="outside", ticklen=1, tickcolor='black')
                ),
            legend=dict(
                x=0,  # Position horizontale de la légende (0 est tout à gauche)
                y=1,  # Position verticale de la légende (1 est tout en haut)
                borderwidth=1,  # Largeur de la bordure de la légende
            ),
        )

        # Afficher le grahique dans Streamlit
        st.plotly_chart(fig3)
        
        # Sauvegarder le graphe en tant qu'image
        save_path = "Temp/Diagramme de chargement avec thq.png"
        save_dir = os.path.dirname(save_path)
        
        fig3.write_image(save_path, scale=4)
        
        
        
    
# =============================================================================
# SI LA THERMIQUE N'EST PAS ACTIVEE (généré avec Ctrl+Maj+4)
# =============================================================================

else :

    # Si l'utilisateur choisie l'onglet "Evolution des efforts"
    if st.session_state.active_tab == "Evolution des efforts" :
        
        # L'utilisateur peut choisir de prendre en compte la compression en cochant la case
        checked_compression_2 = st.checkbox("Prise en compte des efforts de compression")
        
        # Si on ne prends pas en compte la compression
        if not checked_compression_2 :

                # On prépare le graphe
            Ne = np.linspace(0, 2*int(float(F0)), 100)
            Ne = Ne.tolist()
            Nb = []
            Na = []
            Nbinf = []
            
            # On calcule les valeurs de Nb et Na en fonction de l'effort exterieur et des valeurs de Lambda et F0 obtenues
            for i in range(0, len(Ne)) :
                if float(F0)-(1-float(Lambda))*float(Ne[i]) > 0.0 :
                    Nb.append(float(F0) + float(Lambda)*float(Ne[i]))
                    Na.append(float(F0)-(1-float(Lambda))*float(Ne[i]))
            
                else : 
                    Nb.append(float(Ne[i]))
                    Na.append(0.0)
            
            
            for i in range(0, len(Ne)) :
                if float(Ne[i]) <= float(F0) :        
                    Nbinf.append(float(F0))
                else :
                    Nbinf.append(float(Ne[i]))
    
            # On crée le graphe
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=Ne, y=Nb, mode='lines', name=r'$N_b$', line = dict(color = '#C00000', width = 1)))
            fig2.add_trace(go.Scatter(x=Ne, y=Na, mode='lines', name=r'$N_a$', line = dict(color = '#002060', width = 1)))
            fig2.add_trace(go.Scatter(x=Ne, y=Nbinf, mode='lines', name=r"$N_{b,infiniment rigide}$", line = dict(color = '#C55A11', width = 1, dash = 'dot')))
            
            # On personnalise le graphe
            fig2.update_layout(
                title = dict(text = "Evolution de l'effort dans la liaison boulonnée en fonction de l'effort extérieur", x = 0.5, xanchor = 'center'),
                xaxis=dict(
                    title = dict(text = r'$N_e [N]$', font = dict(color = 'black')),
                    showline=True,  # Afficher la barre de l'axe X
                    linecolor='black',  # Couleur de la barre de l'axe X
                    linewidth=1,  # Largeur de la barre de l'axe X
                    tickformat=',.0f',
                    tickfont=dict(color='black'),
                    minor=dict(ticks="outside", ticklen=1, tickcolor='black')
                    ),
                yaxis=dict(
                    title = dict(text = r'$N [N]$', font = dict(color = 'black')),
                    showline=True,  # Afficher la barre de l'axe Y
                    linecolor='black',  # Couleur de la barre de l'axe Y
                    linewidth=1,  # Largeur de la barre de l'axe Y
                    tickformat=',.0f',
                    tickfont=dict(color='black'),
                    minor=dict(ticks="outside", ticklen=1, tickcolor='black')
                    ),
                legend=dict(
                    x=0,  # Position horizontale de la légende (0 est tout à gauche)
                    y=1,  # Position verticale de la légende (1 est tout en haut)
                    borderwidth=1,  # Largeur de la bordure de la légende
                ),
            )
            
            
            # Afficher le graphique dans Streamlit
            st.plotly_chart(fig2)
            fig2.write_image("Evolution des efforts sans thq.png", scale=4)
            
            
            # Ajouter un curseur
            st.write("Sélectionnez la valeur de l'effort extérieur $N_e$ en N")
            Next = st.slider("", round(int(-2.0*float(F0)),-2), round(int(2.0*float(F0)),-2), 0, step = int(100), label_visibility="collapsed")
            res_col1, res_col2 = st.columns([1, 1])
            
            # On récupère l'effort Nb et Na résultant de l'effort Ne appliqué
            if float(F0) - (1-float(Lambda))*float(Next) > 0 :
                Nb_Ne = float(F0) + float(Lambda)*float(Next)
                Na_Ne = float(F0) - (1-float(Lambda))*float(Next)
            else :
                Nb_Ne = float(Next)
                Na_Ne = 0.0
                
            with res_col1:
                st.write("L'effort repris par l'élément de serrage vaut $N_b$ = " + str(round(Nb_Ne,0)) + " $N$")
            with res_col2:
                st.write("L'effort repris par les pièces assemblées vaut $N_a$ = " + str(round(Na_Ne,0)) + " $N$")
            

        #Si on prend en compte la compression
        else :
            # On prépare le graphe
            Ne = np.linspace(-2*int(float(F0)), 2*int(float(F0)), 200)
            Ne = Ne.tolist()
            Nb = []
            Na = []
            Nbinf = []
            
            # On calcule les valeurs de Nb et Na en fonction de l'effort exterieur et des valeurs de Lambda et F0 obtenues
            for i in range(0, len(Ne)) :
                if float(Ne[i]) < 0.0 : # Si Ne est négatif (compression)
                    if float(F0) + float(Lambda)*float(Ne[i]) < 0 : # Si l'effort de la bolt est nul
                        Nb.append(0.0)
                        Na.append(float(F0)-(1-float(Lambda))*float(Ne[i]))
                    else :
                        Nb.append(float(F0) + float(Lambda)*float(Ne[i]))
                        Na.append(float(F0)-(1-float(Lambda))*float(Ne[i]))
                        
                else : # Si Ne est positif (traction)
                    if float(F0)-(1-float(Lambda))*float(Ne[i]) > 0.0 :
                        Nb.append(float(F0) + float(Lambda)*float(Ne[i]))
                        Na.append(float(F0)-(1-float(Lambda))*float(Ne[i]))
                
                    else : 
                        Nb.append(float(Ne[i]))
                        Na.append(0.0)
                
                
                for i in range(0, len(Ne)) :
                    if float(Ne[i]) <= float(F0) :        
                        Nbinf.append(float(F0))
                    else :
                        Nbinf.append(float(Ne[i]))
    
            # On crée le graphe
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=Ne, y=Nb, mode='lines', name=r'$N_b$', line = dict(color = '#C00000', width = 1)))
            fig2.add_trace(go.Scatter(x=Ne, y=Na, mode='lines', name=r'$N_a$', line = dict(color = '#002060', width = 1)))
            fig2.add_trace(go.Scatter(x=Ne, y=Nbinf, mode='lines', name=r"$N_{b,infiniment rigide}$", line = dict(color = '#C55A11', width = 1, dash = 'dot')))
            
            # On personnalise le graphe
            fig2.update_layout(
                title = dict(text = "Evolution de l'effort dans la liaison boulonnée en fonction de l'effort extérieur", x = 0.5, xanchor = 'center'),
                xaxis=dict(
                    title = dict(text = r'$N_e [N]$', font = dict(color = 'black')),
                    showline=True,  # Afficher la barre de l'axe X
                    linecolor='black',  # Couleur de la barre de l'axe X
                    linewidth=1,  # Largeur de la barre de l'axe X
                    tickformat=',.0f',
                    tickfont=dict(color='black'),
                    minor=dict(ticks="outside", ticklen=1, tickcolor='black')
                    ),
                yaxis=dict(
                    title = dict(text = r'$N [N]$', font = dict(color = 'black')),
                    showline=True,  # Afficher la barre de l'axe Y
                    linecolor='black',  # Couleur de la barre de l'axe Y
                    linewidth=1,  # Largeur de la barre de l'axe Y
                    tickformat=',.0f',
                    tickfont=dict(color='black'),
                    minor=dict(ticks="outside", ticklen=1, tickcolor='black')
                    ),
                legend=dict(
                    x=0.5,  # Position horizontale de la légende (0 est tout à gauche)
                    y=1,  # Position verticale de la légende (1 est tout en haut)
                    borderwidth=1,  # Largeur de la bordure de la légende
                ),
            )
            
            # Afficher le graphique dans Streamlit
            st.plotly_chart(fig2)
            fig2.write_image("Evolution des efforts sans thq.png", scale=4)

            
            # Ajouter un curseur
            st.write("Sélectionnez la valeur de l'effort extérieur $N_e$ en N")
            Next = st.slider("", round(int(-2.0*float(F0)),-2), round(int(2.0*float(F0)),-2), 0, step = int(100), label_visibility="collapsed")
            res_col1, res_col2 = st.columns([1, 1])
            
            # On récupère l'effort Nb et Na résultant de l'effort Ne appliqué
            if float(F0) - (1-float(Lambda))*float(Next) > 0 :
                Nb_Ne = float(F0) + float(Lambda)*float(Next)
                Na_Ne = float(F0) - (1-float(Lambda))*float(Next)
            else :
                Nb_Ne = float(Next)
                Na_Ne = 0.0
                
            with res_col1:
                st.write("L'effort repris par l'élément de serrage vaut")
                st.write("$N_b$ = " + str(round(Nb_Ne,0)) + " $N$")
            with res_col2:
                st.write("L'effort repris par les pièces assemblées vaut")
                st.write("$N_a$ = " + str(round(Na_Ne,0)) + " $N$")
            
            
            
            
            
            
            

    # Si l'utilisateur choisie l'onglet "Efforts et élongations"                
    elif st.session_state.active_tab == "Efforts et élongations" :
        
        F0 = float(F0)
    
        # Créer une plage de valeurs pour x
        x1 = np.linspace(-F0/Kb, 0, 100)
        x2 = np.linspace(0, F0/Ka, 100)

        
        # Calculer les valeurs de f(x) pour ces valeurs de x
        y1 = elong_bolt_F0(x1)
        y2 = elong_pieces_F0(x2)
        
        
        x1 = x1.tolist()
        x2 = x2.tolist()
        xF0 = x1 + x2
        
        y1 = y1.tolist()
        y2 = y2.tolist()      
        yF0 = y1 + y2
        
        
        # On crée le graphe
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=xF0, y=yF0, mode='lines', name=r'$N_b$', line = dict(color = '#C00000', width = 1)))

        
        # Mettre à jour les axes pour définir les limites
        borneX_min = -1.2*F0/Kb
        borneX_max = 1.2*F0/Ka
        borneY_max = 1.2*F0
        fig3.update_xaxes(title_text='x', range=[borneX_min, borneX_max])  # Définir la plage de l'axe X
        fig3.update_yaxes(title_text='f(x)', range=[0, borneY_max])  # Définir la plage de l'axe Y
        
        
        # On personnalise le graphe
        fig3.update_layout(
            title = dict(text = "Diagramme de chargement d'une liaison boulonnée", x = 0.5, xanchor = 'center'),
            xaxis=dict(
                # Afficher un axe vertical centré en x = 0
                # zeroline = True,
                # zerolinecolor = 'black',
                # zerolinewidth = 1,
                title = dict(text = r'Delta L [mm]', font = dict(color = 'black')),
                showline=True,  # Afficher la barre de l'axe X
                linecolor='black',  # Couleur de la barre de l'axe X
                linewidth=1,  # Largeur de la barre de l'axe X
                tickformat='.2f',
                tickfont=dict(color='black'),
                minor=dict(ticks="outside", ticklen=1, tickcolor='black')
                ),
            yaxis=dict(
                title = dict(text = r'N [N]', font = dict(color = 'black')),
                showline=True,  # Afficher la barre de l'axe Y
                linecolor='black',  # Couleur de la barre de l'axe Y
                linewidth=1,  # Largeur de la barre de l'axe Y
                tickformat=' .0f',
                tickfont=dict(color='black'),
                minor=dict(ticks="outside", ticklen=1, tickcolor='black')
                )
        )
            
        # On affiche le graphe
        st.plotly_chart(fig3)
        
        # Sauvegarder le graphe en tant qu'image
        fig3.write_image("Diagramme de chargement sans thq.png", scale=4)
        
        
        # On ajoute un expander sur l'impact de l'application d'un effort extérieur
        
        with st.expander("Impact de l'application d'un effort extérieur") :
            # Ajouter un curseur
            Next = st.slider("Sélectionnez la valeur de l'effort extérieur $N_e$ en N:", round(int(-2.0*float(F0)),-2), round(int(2.0*float(F0)),-2), 0, step = int(100))
            

            # On calcule les différentes grandeurs qui nous intéressent
            if float(Next) >= 0.0 : # Si on est en traction
                # On récupère l'effort Nb et Na résultant de l'effort Ne appliqué
                if float(F0) - (1-float(Lambda))*float(Next) > 0 :
                    Nb_Ne = float(F0) + float(Lambda)*float(Next)
                    Na_Ne = float(F0) - (1-float(Lambda))*float(Next)
                else :
                    Nb_Ne = float(Next)
                    Na_Ne = 0.0
            else : # Si on est en compression
                # On récupère l'effort Nb et Na résultant de l'effort Ne appliqué
                if float(F0) + float(Lambda)*float(Next) > 0 : # On regarde si Nb est toujours positif
                    Nb_Ne = float(F0) + float(Lambda)*float(Next)
                    Na_Ne = float(F0) - (1-float(Lambda))*float(Next)
                else :
                    Nb_Ne = 0.0
                    Na_Ne = -float(Next)
            
            DeltaLbNe = float(Nb_Ne)/float(Kb)
            DeltaLaNe = float(Na_Ne)/float(Ka)
            
            # Imp_Fe_col1, Imp_Fe_col2 = st.columns([1, 1])
            
            st.write("L'effort repris par l'élément de serrage vaut")
            st.write("$N_b$ = " + str(round(Nb_Ne,0)) + " $N$")
            st.write("L'effort repris par les pièces assemblées vaut")
            st.write("$N_a$ = " + str(round(Na_Ne,0)) + " $N$")
            st.write("L'élongation de l'élément de serrage due à l'effort $N_e$ vaut")
            st.write("$\Delta L_{b,N_e}$ = " + str(round(DeltaLbNe, 3)) + " $mm$")
            st.write("La contraction des pièces assemblées due à l'effort $N_e$ vaut")
            st.write("$\Delta L_{a,N_e}$ = " + str(round(DeltaLaNe, 3)) + " $mm$")
            
            if float(Next) >= 0.0 : # Si on est en traction
                st.write("L'augmentation de l'élongation de l'élément de serrage due à $N_e$ est ")
                st.write("$d_{b,N_e}$ = " + str(round(DeltaLbNe-float(F0/Kb), 3)) + " $mm$, soit de " + str(round(((DeltaLbNe-float(F0/Kb))/DeltaLbNe)*100, 2)) + " %")
                st.write("La diminution de la contraction des pièces assemblées due à $N_e$ est ")
                st.write("$d_{a,N_e}$ = " + str(round(float(F0/Ka)-DeltaLaNe, 3)) + " $mm$, soit de " + str(round(((float(F0/Ka)-DeltaLaNe)/float(F0/Ka))*100, 2)) + " %")
                
                st.image("Pictures/Interprétation diagramme de chargement - traction - T0.png", caption = "Interprétation du diagramme de chargement", use_column_width = True)
            else :
                st.write("La diminution de l'élongation de l'élément de serrage due à $N_e$ est ")
                st.write("$d_{b,N_e}$ = " + str(round(float(F0/Kb)-DeltaLbNe, 3)) + " $mm$, soit de " + str(round(((float(F0/Kb)-DeltaLbNe)/float(F0/Kb))*100, 2)) + " %")
                st.write("L'augmentation de la contraction des pièces assemblées due à $N_e$ est ")
                st.write("$d_{a,N_e}$ = " + str(round(DeltaLaNe-float(F0/Ka), 3)) + " $mm$, soit de " + str(round(((DeltaLaNe-float(F0/Ka))/DeltaLaNe)*100, 2)) + " %")
                
                st.image("Pictures/Interprétation diagramme de chargement - compression- T0.png", caption = "Interprétation du diagramme de chargement", use_column_width = True)

        












# Bouton pour exporter le DataFrame en tant qu'image
if st.button("Générer Rapport"):
    df_assembly_part_data = st.session_state.test_data
    

    
    if checked_thq :

        
        df_results = df_results_with_thq
        
        forces_evol_graph_path = "Temp/Evolution des efforts avec thq.png"
        diagramme_chargement_graph_path = "Temp/Diagramme de chargement avec thq.png"
    
    else :
        Tb = T0
        Ta = T0
        df_thermal_property_assembly_parts = ""
        L_Data_thq = []
        
        df_results = df_results_without_thq
        
        forces_evol_graph_path = "Temp/Evolution des efforts sans thq.png"
        
        diagramme_chargement_graph_path = "Temp/Diagramme de chargement sans thq.png"
        
        


    bolt_type = selection
    if bolt_type == 'Vis' :
        image_bolt_type_path = "Pictures/Vis_Dimensions.png"
        
    pdf = create_pdf_template("Test Rapport.pdf", bolt_type, df_bolt_geom_data, image_bolt_type_path, materiau_bolt, df_assembly_part_data, F0, T0, checked_thq, Tb, Ta, df_thermal_property_assembly_parts, round(Lambda, 3), Nedecollement, L_Data_thq, df_results, forces_evol_graph_path, diagramme_chargement_graph_path)
    
    
    st.success("PDF exporté avec succès")

    
    # Proposer le téléchargement
        with open(pdf, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
            st.download_button(
                label="Télécharger le rapport PDF",
                data=pdf_bytes,
                file_name="Rapport.pdf",
                mime="application/pdf"
            )
    
    

