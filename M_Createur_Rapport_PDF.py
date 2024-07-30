#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch



from io import BytesIO
import pandas as pd
from PIL import Image as PILImage


def create_pdf_template(bolt_type, df_geom_data, image_bolt_type_path, bolt_material, df_assembly_part_data, F0, T0, check_thq, Tb, Ta, df_thermal_property_assembly_parts, Lambda, Nedecollement, L_Data_thq, df_results_with_thq, forces_evol_thq_graph_path, diagramme_chargement_thq_graph_path):
    buffer = BytesIO()
    
    
    # Configuration du document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    page_width = letter[0] # Largeur de la page

    # Styles de texte
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    subtitle2_style = styles['Heading2']
    subtitle3_style = styles['Heading3']
    subtitle4_style = styles['Heading4']
    

    normal_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['BodyText'],
        fontSize = 9  # Set the desired font size
    )
    
    # Legend
    legend_style = ParagraphStyle(
        'Legend',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.black,
        spaceBefore=6,
        alignment=1, # Centrer la légende
        fontName='Helvetica-Oblique'  # Italics
    )

    # Ajout du titre
    title = Paragraph("RAPPORT DE MODÉLISATION DE LA PRÉCONTRAINTE", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le titre
    
    
    
# =============================================================================
#     SAISIE DES DONNEES D'ENTREE
# =============================================================================
    
    subtitle_1 = Paragraph("SAISIE DES DONNÉES D'ENTRÉE", subtitle2_style)
    elements.append(subtitle_1)
    
    
    # =============================================================================
    #     Type d'élément de serrage 
    # =============================================================================

    subsubtitle_1 = Paragraph("Type d'élément de serrage", subtitle3_style)
    elements.append(subsubtitle_1)

    # Ajout de texte de démonstration
    text = Paragraph("Type d'élément de serrage choisi : " + str(bolt_type), normal_style)
    elements.append(text)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    
    
    # =============================================================================
    #     Données géométriques à T0
    # =============================================================================
    
    subsubtitle_2 = Paragraph("Donneés géométriques à T<sub>0</sub>", subtitle3_style)
    elements.append(subsubtitle_2)
    
    subsubsubtitle_1 = Paragraph("- Données liées à l'élément de serrage", subtitle4_style)
    elements.append(subsubsubtitle_1)
    elements.append(Spacer(1, 4))  # Ajouter un espace après le sous sous titre
    
    # Ajout d'un tableau de démonstration
    # Convertir le DataFrame en une liste de listes
    bolt_data = [df_geom_data.columns.tolist()] + df_geom_data.values.tolist()    
    
    col_widths = [145, 37, 35, 30]
    # table_bolt_data = Table(bolt_data, colWidths=[table_width / len(df_geom_data.columns)] * len(df_geom_data.columns))
    table_bolt_data = Table(bolt_data, colWidths=col_widths)
    table_bolt_data.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                               ('FONTSIZE', (0, 0), (-1, -1), 8),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                               # ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                               ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
                               ('BOX', (0, 0), (-1, -1), 0, colors.white), # Pas de contour
                               ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    
    
    # Load the image and calculate new dimensions
    aspect_ratio = PILImage.open(image_bolt_type_path).width/PILImage.open(image_bolt_type_path).height
    image_width = page_width/3
    image_height = image_width/aspect_ratio
    
    # Charger une image
    image_bolt_type = Image(image_bolt_type_path)
    image_bolt_type.drawHeight = image_height
    image_bolt_type.drawWidth = image_width

    # Create a table with two columns: one for the image and one for the data table
    combined_table = Table([[table_bolt_data, image_bolt_type]])
    combined_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    elements.append(combined_table)
    
    text = Paragraph("Matériau de l'élément de serrage : " + str(bolt_material), normal_style)
    elements.append(text)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    
    
    # Données liées à l'élément de serrage
    
    subsubsubtitle_2 = Paragraph("- Données liées aux pièces assemblées", subtitle4_style)
    elements.append(subsubsubtitle_2)
    
    assembly_part_data = [df_assembly_part_data.columns.tolist()] + df_assembly_part_data.values.tolist()    
    table_assembly_part_data = Table(assembly_part_data)
    table_assembly_part_data.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                               ('FONTSIZE', (0, 0), (-1, -1), 8),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                               # ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                               ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
                               ('BOX', (0, 0), (-1, -1), 0, colors.white), # Pas de contour
                               ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    elements.append(table_assembly_part_data)
    legend = Paragraph("Tableau 2 : Données liées aux pièces assemblées", legend_style)
    elements.append(legend)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    
    
    # =============================================================================
    #     Données de serrage
    # =============================================================================
    subsubtitle_3 = Paragraph("Données de serrage", subtitle3_style)
    elements.append(subsubtitle_3)
    
    text = Paragraph("Température initiale à laquelle a été effectué le préserrage : T<sub>0</sub> = " + str(T0) + " °C", normal_style)
    elements.append(text)
    text = Paragraph("Préserrage initial à T<sub>0</sub> : F<sub>0</sub> = " + str(F0) + " N", normal_style)
    elements.append(text)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    
    # =============================================================================
    #     Prise en compte de la thermique
    # =============================================================================
    subsubtitle_4 = Paragraph("Prise en compte de la thermique", subtitle3_style)
    elements.append(subsubtitle_4)
    
    if check_thq :
        text = Paragraph("Effet des dilatations thermiques pris en compte : OUI", normal_style)
        elements.append(text)
        elements.append(Spacer(1, 4))  # Ajouter un espace après le texte
        
        text = Paragraph("Température moyenne de l'élément de serrage établie suite à l'application d'un chargement thermique : T<sub>b</sub> = " + str(Tb) + " °C", normal_style)
        elements.append(text)
        
        elements.append(Spacer(1, 4))  # Ajouter un espace après le texte
        
        text = Paragraph("Température moyenne des pièces assemblées établie suite à l'application d'un chargement thermique : T<sub>a</sub> = " + str(Ta) + " °C", normal_style)
        elements.append(text)
        elements.append(Spacer(1, 8))  # Ajouter un espace après le texte
        
        thermal_property_assembly_part_data = [df_thermal_property_assembly_parts.columns.tolist()] + df_thermal_property_assembly_parts.values.tolist()    
        table_thermal_property_assembly_part_data = Table(thermal_property_assembly_part_data)
        table_thermal_property_assembly_part_data.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                                   ('FONTSIZE', (0, 0), (-1, -1), 8),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                                   # ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
                                   ('BOX', (0, 0), (-1, -1), 0, colors.white), # Pas de contour
                                   ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
        elements.append(table_thermal_property_assembly_part_data)
        
        
        legend = Paragraph("Tableau 3 : Propriétés des matériaux constituants l'assemblage boulonné pour les températures T<sub>b</sub> et T<sub>a</sub> renseignées", legend_style)
        elements.append(legend)
        
        elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
        
    
    else : 
        text = Paragraph("Effet des dilatations thermiques pris en compte : NON", normal_style)
        elements.append(text)
        elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
        
        
        
# =============================================================================
#     RESULTATS
# =============================================================================

    # Saut de page
    elements.append(PageBreak())
    
    subtitle_2 = Paragraph("RÉSULTATS", subtitle2_style)
    elements.append(subtitle_2)
    
    elements.append(Spacer(1, 8))  # Ajouter un espace après le texte
    
    text = Paragraph("Valeur du ceofficient de rigidité &Lambda; : " + str(Lambda), normal_style)
    elements.append(text)
    
    elements.append(Spacer(1, 8))  # Ajouter un espace après le texte
    
    text = Paragraph("La valeur de l'effort de décollement vaut N<sub>e,décollement</sub> = " + str(round(float(Nedecollement),2)) + " N", normal_style)
    elements.append(text)
    
    elements.append(Spacer(1, 8))  # Ajouter un espace après le texte
        
        
    # Si la prise en compte de la thermique est activée
    if check_thq :
        
        # On mets les valeurs de résultats de la thermique dans des variables
        Fprime = L_Data_thq[1]
        Qi = L_Data_thq[2]
        F0prime = L_Data_thq[3]
        Delta_Lb = L_Data_thq[4]
        Delta_La = L_Data_thq[5]
        Delta_Lbprime = L_Data_thq[6]
        Delta_Laprime = L_Data_thq[7]
        
        
        if Qi > 0 :
            text = Paragraph("L'assemblage boulonné subit un accroissement du préserrage. La valeur du préserrage à chaud vaut alors F'<sub>0</sub> = " + str(round(float(F0prime), 0)) + " N.", normal_style)
            elements.append(text)
        else :
            text = Paragraph("L'assemblage boulonné subit une diminution du préserrage. La valeur du préserrage à chaud vaut alors F'<sub>0</sub> = " + str(round(float(F0prime), 0)) + " N.", normal_style)
            elements.append(text)
            
        elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
        
        # Ajout du tableau des résultats
        result_with_thq_data = [df_results_with_thq.columns.tolist()] + df_results_with_thq.values.tolist()  
        
        result_with_thq_data = Table(result_with_thq_data)
        result_with_thq_data.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                                   ('FONTSIZE', (0, 0), (-1, -1), 8),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                                   # ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
                                   ('BOX', (0, 0), (-1, -1), 0, colors.white), # Pas de contour
                                   ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
        elements.append(result_with_thq_data)
        
        # Legende du tableau
        legend_style = ParagraphStyle(
            'Legend',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.black,
            spaceBefore=6,
            alignment=1, # Centrer la légende
            fontName='Helvetica-Oblique'  # Italics
        )
        legend = Paragraph("Tableau 4 : Ensemble des résultats liés à la précontrainte et à un chargement thermique", legend_style)
        elements.append(legend)
        
        elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
        
        
        # On affiche le graphe d'évolution de l'effort dans la liaison boulonnée en fonction de l'effort extérieur dans le cas où la thermique est prise en compte
        graph_width = page_width - 2 * inch  # graph_width equal page width minus margins
        forces_evol_thq_graph = Image(forces_evol_thq_graph_path)
        forces_evol_thq_graph.drawHeight = graph_width * forces_evol_thq_graph.drawHeight / forces_evol_thq_graph.drawWidth
        forces_evol_thq_graph.drawWidth = graph_width
        elements.append(forces_evol_thq_graph)
        
        legend = Paragraph("Figure 2 : Evolution de l'effort dans la liaison boulonnée en fonction de l'effort extérieur", legend_style)
        elements.append(legend)
        
        elements.append(Spacer(1, 12))  # Ajouter un espace entre les graphes
        
        
        # On affiche le graphe du diagramme de chargement dans le cas où la thermique est prise en compte
        graph_width = page_width - 2 * inch  # graph_width equal page width minus margins
        diagramme_chargement_thq_graph = Image(diagramme_chargement_thq_graph_path)
        diagramme_chargement_thq_graph.drawHeight = graph_width * diagramme_chargement_thq_graph.drawHeight / diagramme_chargement_thq_graph.drawWidth
        diagramme_chargement_thq_graph.drawWidth = graph_width
        elements.append(diagramme_chargement_thq_graph)
        
        legend = Paragraph("Figure 3 : Diagramme de chargement de la liaison boulonnée", legend_style)
        elements.append(legend)
        
    # Si la thermique n'est pas prise en compte    
    else :
        result_with_thq_data = [df_results_with_thq.columns.tolist()] + df_results_with_thq.values.tolist()  
        
        result_with_thq_data = Table(result_with_thq_data)
        result_with_thq_data.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                                   ('FONTSIZE', (0, 0), (-1, -1), 8),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                                   # ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
                                   ('BOX', (0, 0), (-1, -1), 0, colors.white), # Pas de contour
                                   ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
        elements.append(result_with_thq_data)
        
        # Legende du tableau
        legend_style = ParagraphStyle(
            'Legend',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.black,
            spaceBefore=6,
            alignment=1, # Centrer la légende
            fontName='Helvetica-Oblique'  # Italics
        )
        legend = Paragraph("Tableau 4 : Ensemble des résultats liés à la précontrainte sans chargement thermique", legend_style)
        elements.append(legend)
        
        elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
        
        
        # On affiche le graphe d'évolution de l'effort dans la liaison boulonnée en fonction de l'effort extérieur dans le cas où la thermique est prise en compte
        graph_width = page_width - 2 * inch  # graph_width equal page width minus margins
        forces_evol_thq_graph = Image(forces_evol_thq_graph_path)
        forces_evol_thq_graph.drawHeight = graph_width * forces_evol_thq_graph.drawHeight / forces_evol_thq_graph.drawWidth
        forces_evol_thq_graph.drawWidth = graph_width
        elements.append(forces_evol_thq_graph)
        
        legend = Paragraph("Figure 2 : Evolution de l'effort dans la liaison boulonnée en fonction de l'effort extérieur", legend_style)
        elements.append(legend)
        
        elements.append(Spacer(1, 12))  # Ajouter un espace entre les graphes
        
        
        # On affiche le graphe du diagramme de chargement dans le cas où la thermique est prise en compte
        graph_width = page_width - 2 * inch  # graph_width equal page width minus margins
        diagramme_chargement_thq_graph = Image(diagramme_chargement_thq_graph_path)
        diagramme_chargement_thq_graph.drawHeight = graph_width * diagramme_chargement_thq_graph.drawHeight / diagramme_chargement_thq_graph.drawWidth
        diagramme_chargement_thq_graph.drawWidth = graph_width
        elements.append(diagramme_chargement_thq_graph)
        
        legend = Paragraph("Figure 3 : Diagramme de chargement de la liaison boulonnée", legend_style)
        elements.append(legend)
        
    
    
    
    
    
    

    # Génération du PDF
    doc.build(elements)
    
    
    buffer.seek(0)
    return buffer








# Exemple d'utilisation
# d = 16.0
# p = 2.0
# ll = 0.0
# ln = 16.4
# a = 20.8
# Dp = 17.5
# De = 70.0
# Le = 8.0
# lb = ll + ln + Le

# L_Designation = ["Diamètre nominal", "Pas", "Longueur du fût lisse", "Longueur du filetage non en prise \n avec les pièces assemblées",
#                  "Diamètre sur le plat de la tête", "Diamètre de perçage", "Longueur d'engagement des filets \n en prise", "Etendue des pièces assemblées autour \n de l'axe de l'élément de serrage"]
# L_Symbole = ["d", "p", "l_l", "l_n", "a", "D_p", "L_e", "D_e"]
# L_Valeur = [d, p, ll, ln, a, Dp, Le, De]
# L_Unite = ["[mm]"]*len(L_Valeur)

# # Création d'un dictionnaire
# D_geom_data = {
#     'Désignation' : L_Designation,
#     'Symbole' : L_Symbole,
#     'Valeur' : L_Valeur,
#     'Unité' : L_Unite
#     }

# # Création du DataFrame pandas à partir du dictionnaire
# df_geom_data = pd.DataFrame(D_geom_data)
    
# bolt_type = 'Vis'
# image_path = "C:/Users/alanb/OneDrive/Documents/AUTOMATISATION/Post-Traitement Boulonnerie/G-MET Bolts V1/Pictures/Boulon_Dimensions.png"
# bolt_material = "660 SS"

# L_Num_Piece = ["Pièce assemblée n°1", "Pièce assemblée n°2"]
# L_Longueur = [16.4, 6.4]
# L_Materiau = ["304L SS", "Alloy 718"]

# D_assembly_part_geom_data = {
#     "Numéro de la pièce assemblée" : L_Num_Piece,
#     "Longueur [mm]" : L_Longueur,
#     "Matériau" : L_Materiau
#     }

# df_assembly_part_data = pd.DataFrame(D_assembly_part_geom_data)

# T0 = 20.0
# F0 = 57184
# check_thq = True

# create_pdf_template("template.pdf", bolt_type, df_geom_data, image_path, bolt_material, df_assembly_part_data, F0, T0, check_thq)
