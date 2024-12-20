#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfgen import canvas




from io import BytesIO
import pandas as pd
from PIL import Image as PILImage



def header_footer(canvas, doc):
    # Récupérer la date du jour
    date = datetime.datetime.now()
    year = date.strftime("%Y")
    month = date.strftime("%m")
    day = date.strftime("%d")
    full_date = str(day) + "/" + str(month) + "/" + str(year)
    
    # Dessiner l'en-tête
    canvas.saveState()
    canvas.setFont('Times-Roman', 10)
    canvas.drawString(6.95 * inch, 10.5 * inch, full_date)

    # Ajouter le logo en haut à gauche 
    logo_path = "Pictures/logo-blanc.PNG"  # Le chemin vers votre logo
    canvas.drawImage(logo_path, 1 * inch, 9.9 * inch, width=1.1 * inch, height=1.1 * inch, preserveAspectRatio=True)
    
    # Dessiner le pied de page avec le numéro de page
    canvas.drawString(7.2 * inch, 0.75 * inch, f"Page {doc.page}")
    canvas.drawString(3 * inch, 0.75 * inch, "Document powered by G-MET Technologies")
    canvas.restoreState()



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
        fontSize = 9,  # Set the desired font size
        alignment=TA_JUSTIFY  # Justification du texte
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






def create_rapport_pdf_rccmrx(bolt_type, df_bolt_geom_data_full, df_Bolt_Material_Data, B_acier_aust, df_assembly_part_data, Study_Case, Lambda, 
                              ft, fv, F0, F0_selection, adherence_selection, selection1, selection2, d, h, Le, SyminP_T, SyminB_T, L, e, T_Results_Ansys_Bilan,
                              critere_selection, L_marge_full, SuminB_T) :
    
    buffer = BytesIO()
    
    
    # Configuration du document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    page_width = letter[0] # Largeur de la page
                                  
    styles = getSampleStyleSheet()
    title_style = styles['Title']

    # Styles de texte
    heading2_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading2'],
        fontName='Times-Bold',  # Police pour Heading1
        fontSize=16,
        spaceAfter=12,
        firstLineIndent=0  # Indentation de la première ligne (en points)
    )
    
    heading3_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading3'],
        fontName='Times-Bold',  # Police pour Heading2
        fontSize=14,
        spaceAfter=10,
        spaceBefore=10,
        firstLineIndent=10  # Indentation de la première ligne (en points)
    )
    
    heading4_style = ParagraphStyle(
        'Heading3Custom',
        parent=styles['Heading4'],
        fontName='Times-Bold',  # Police pour Heading3
        fontSize=12,
        spaceAfter=8,
        spaceBefore=20,
        firstLineIndent=20  # Indentation de la première ligne (en points)
    )
                                  

    # subtitle2_style = styles['Heading2']
    # subtitle3_style = styles['Heading3']
    # subtitle4_style = styles['Heading4']
    subtitle2_style = heading2_style
    subtitle3_style = heading3_style
    subtitle4_style = heading4_style
    

    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['BodyText'],
        fontSize = 9,  # Set the desired font size
        fontName = 'Times-Roman',
        alignment=TA_JUSTIFY  # Justification du texte
    )

    equation_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['BodyText'],
        fontSize = 9,  # Set the desired font size
        alignment=1,  # Centré
        fontName = 'Times-Roman',
    )
                                  
    conclusion_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['BodyText'],
        fontName='Times-Bold',
        fontSize = 9,  # Set the desired font size
        alignment=TA_JUSTIFY  # Justification du texte
    )
    
    
    # Legend
    legend_style = ParagraphStyle(
        'Legend',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.black,
        spaceBefore=6,
        alignment=1, # Centrer la légende
        fontName='Times-Italic'  # Italics
    )

    # Ajout du titre
    title = Paragraph("ANNEXE : DIMENSIONNEMENT DE LA BOULONNERIE", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le titre
    
    
    
# =============================================================================
#     CODE
# =============================================================================
    
    subtitle_0 = Paragraph("CODE DE DIMENSIONNEMENT", subtitle2_style)
    elements.append(subtitle_0)
    
    text = Paragraph("Le code de dimensionnement utilisé pour cette étude est le RCC-MRx, selon les règles du RB 3280 pour l’évaluation des critères et de l’Annexe 6 pour le calcul des différentes contraintes. Les paragraphes correspondant aux équations utilisées seront précisés entre parenthèses. Il conviendra de s’y référer pour plus de détails.", normal_style)
    elements.append(text)
    elements.append(Spacer(1, 22))  # Ajouter un espace après le texte
    
    
# =============================================================================
#     SAISIE DES DONNEES D'ENTREE
# =============================================================================
    # Saut de page
    elements.append(PageBreak())
    subtitle_1 = Paragraph("DONNÉES D'ENTRÉE", subtitle2_style)
    elements.append(subtitle_1)
    
    
    # =============================================================================
    #     Elément de serrage 
    # =============================================================================

    subsubtitle_1 = Paragraph("Elément de serrage", subtitle3_style)
    elements.append(subsubtitle_1)
    
    # Type d'élément de serrage
    subsubsubtitle_1 = Paragraph("- Type d'élément de serrage", subtitle4_style)
    elements.append(subsubsubtitle_1)

    if str(bolt_type) == "Vis" :                                  
        text = Paragraph("L'élément de serrage étudié est une " + str(bolt_type.lower()) + " et est supposée normalisée.", normal_style)
        elements.append(text)
    else :
        text = Paragraph("L'élément de serrage étudié est un " + str(bolt_type.lower()) + " et est supposé normalisé.", normal_style)
        elements.append(text)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    # Données géométriques
    subsubsubtitle_2 = Paragraph("- Données géométriques", subtitle4_style)
    elements.append(subsubsubtitle_2)
    
    text = Paragraph("Les données géométriques de cet élément de serrage utilisées pour les calculs de dimensionnement sont résumées dans le Tableau 1 suivant.", normal_style)
    elements.append(text)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    # Convertir le DataFrame en une liste de listes
    bolt_geom_data = [df_bolt_geom_data_full.columns.tolist()] + df_bolt_geom_data_full.values.tolist()
    bolt_geom_data.append(["Hauteur de l'écrou", "h", str(h), "[mm]"])
    
    # On ajoute les valeurs de e et L si elles sont fournies
    if "B3" in Study_Case :
        bolt_geom_data.append(["Entraxe ou distance de l'axe des éléments de serrage au bord \n de la pièce assemblée dans la direction de l'effort", "L", str(L), "[mm]"])
        bolt_geom_data.append(["Epaisseur de la pièce assemblée", "t", str(e), "[mm]"])

                                  
    table_bolt_geom_data = Table(bolt_geom_data)
    table_bolt_geom_data.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                               ('FONTSIZE', (0, 0), (-1, -1), 8),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                               ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                               # ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                               ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
                               ('BOX', (0, 0), (-1, -1), 0, colors.white), # Pas de contour
                               ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    
    elements.append(table_bolt_geom_data)
    legend = Paragraph("Tableau 1 : Données géométriques liées à l'élément de serrage", legend_style)
    elements.append(legend)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    
    # Matériau
    subsubsubtitle_3 = Paragraph("- Matériau", subtitle4_style)
    elements.append(subsubsubtitle_3)
    bolt_material_data = [df_Bolt_Material_Data.columns.tolist()] + df_Bolt_Material_Data.values.tolist()
    bolt_material = bolt_material_data[1][0]
    text = Paragraph("L'élément de serrage étudié est en " + str(bolt_material) + ". Les propriétés mécaniques utilisées, évaluées selon la température de calcul, sont présentées dans le Tableau 2 suivant.", normal_style)
    elements.append(text)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    table_bolt_material_data = Table(bolt_material_data)
    table_bolt_material_data.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                               ('FONTSIZE', (0, 0), (-1, -1), 8),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                               ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                               # ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                               ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
                               ('BOX', (0, 0), (-1, -1), 0, colors.white), # Pas de contour
                               ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    elements.append(table_bolt_material_data)
    legend = Paragraph("Tableau 2 : Données matériau liées à l'élément de serrage", legend_style)
    elements.append(legend)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte

    text = Paragraph("avec", normal_style)
    elements.append(text)   
    
    list_prop_mat_bolt_def = ["S<sub>mB</sub> la contrainte admissible de l'élément de serrage pour les matériels de niveau N1<sub>Rx</sub> et N2<sub>Rx</sub>", "(R<sub>p0.2</sub>)<sub>min,B</sub> la limite d'élasticité minimale à 0,2 % de l'élément de serrage à la température T", "(R<sub>m</sub>)<sub>min,B</sub> la résistance à la traction minimale de l'élément de serrage à la température T"]
    list_prop_mat_bolt_def_flowable = ListFlowable([ListItem(Paragraph(item, normal_style)) for item in list_prop_mat_bolt_def], bulletType='bullet', bulletIndent=20)  # Type de puce ('bullet' pour une puce classique))
    elements.append(list_prop_mat_bolt_def_flowable)

    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    # Acier austhénitique
    if B_acier_aust :
        text = Paragraph("Il s'agit d'un acier austénitique.", normal_style)
        elements.append(text)
    else :
        text = Paragraph("Il ne s'agit pas d'un acier austénitique.", normal_style)
        elements.append(text)
    
    # Boulonnerie Haute Résistance
    if float(SuminB_T) >= 700 :
        text = Paragraph("La valeur de (R<sub>m</sub>)<sub>min,B</sub> est supérieure ou égale à 700 MPa, il s'agit d'une boulonnerie haute résistance.", normal_style)
        elements.append(text)
    else : 
        text = Paragraph("La valeur de (R<sub>m</sub>)<sub>min,B</sub> est inférieure à 700 MPa, il s'agit d'une boulonnerie normale.", normal_style)
        elements.append(text)

    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    # =============================================================================
    #     Pièces assemblées
    # =============================================================================
    
    subsubtitle_2 = Paragraph("Pièces assemblées", subtitle3_style)
    elements.append(subsubtitle_2)
    
    text = Paragraph("Les données liées aux pièces assemblées (matériaux et températures) sont présentées dans le Tableau 3 ci-dessous.", normal_style)
    elements.append(text)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le sous sous titre
    
    
    assembly_part_data = [df_assembly_part_data.columns.tolist()] + df_assembly_part_data.values.tolist()    
    table_assembly_part_data = Table(assembly_part_data)
    table_assembly_part_data.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                               ('FONTSIZE', (0, 0), (-1, -1), 8),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                               ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                               # ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                               ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
                               ('BOX', (0, 0), (-1, -1), 0, colors.white), # Pas de contour
                               ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    elements.append(table_assembly_part_data)
    legend = Paragraph("Tableau 3 : Données liées aux pièces assemblées", legend_style)
    elements.append(legend)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte

    text = Paragraph("avec", normal_style)
    elements.append(text)   
    
    list_prop_mat_piece_def = ["S<sub>m</sub> la contrainte admissible des pièces assemblées pour les matériels de niveau N1<sub>Rx</sub> et N2<sub>Rx</sub>", "(R<sub>p0.2</sub>)<sub>min,P</sub> la limite d'élasticité minimale à 0,2 % des pièces assemblées à la température T", "(R<sub>m</sub>)<sub>min,P</sub> la résistance à la traction minimale des pièces assemblées à la température T"]
    list_prop_mat_piece_def_flowable = ListFlowable([ListItem(Paragraph(item, normal_style)) for item in list_prop_mat_piece_def], bulletType='bullet', bulletIndent=20)  # Type de puce ('bullet' pour une puce classique))
    elements.append(list_prop_mat_piece_def_flowable)

    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    
    
    # =============================================================================
    #     Hypothèses de calcul
    # =============================================================================
                                  
    subsubtitle_3 = Paragraph("Hypothèses de calcul", subtitle3_style)
    elements.append(subsubtitle_3)
    
    # Cas B1
    if 'B1' in Study_Case :
        text = Paragraph("La liaison boulonnée est précontrainte et assure une fonction d’étanchéité. Elle entre donc dans la catégorie B1 et le dimensionnement se fait conformément au jeu de règles correspondant (RB 3281, RB 3282 et RB 3283). Le fluage ainsi que l’irradiation de la liaison sont négligés.", normal_style)
        elements.append(text)
        text = Paragraph("Les données complémentaires permettant de calculer les contraintes à vérifier sont :", normal_style)
        elements.append(text)
        
        list_B1 = ["Le coefficient de rigidité : &Lambda; = " + str(Lambda), "Le coefficient de frottement sous tête ou sous écrou : f' = " + str(ft), "Le coefficient de frottement entre les filets en prise : f = " + str(fv), "L'effort de précontrainte : F<sub>0</sub> = " + str(F0) + " N"]

        list_B1_flowable = ListFlowable([ListItem(Paragraph(item, normal_style)) for item in list_B1], bulletType='bullet', bulletIndent=20)  # Type de puce ('bullet' pour une puce classique))
        elements.append(list_B1_flowable)
        
        if F0_selection == "oui" :
            text = Paragraph("Cet effort de précontrainte est pris en compte dans les résultats des calculs ANSYS présentés ci-après.", normal_style)
            elements.append(text)
        else : 
            text = Paragraph("Cet effort de précontrainte n’est pas pris en compte dans les résultats des calculs ANSYS présentés ci-après.", normal_style)
            elements.append(text)
        
        if adherence_selection == "oui" :
            text = Paragraph("On suppose que les efforts extérieurs sont repris par adhérence.", normal_style)
            elements.append(text)
        else :
            text = Paragraph("On suppose que les efforts extérieurs ne sont pas repris par adhérence.", normal_style)
            elements.append(text)
        
        if selection1 == "oui" :
            text = Paragraph("De plus, l’élément de serrage subit un moment de flexion par effet levier dû à une flexion locale des pièces assemblées.", normal_style)
            elements.append(text)
        else :
            text = Paragraph("De plus, l’élément de serrage ne subit pas de moment de flexion par effet levier dû à une flexion locale des pièces assemblées. ", normal_style)
            elements.append(text)
        
    
        text = Paragraph("Enfin, les conditions de l’étude permettent d’obtenir les inégalités suivantes nécessaires pour la détermination des critères à évaluer.", normal_style)
        elements.append(text)
        h = float(h)
        d = float(d)
        Le = float(Le)
        SyminP_T = float(SyminP_T)
        SyminB_T = float(SyminB_T)
        
        if h >= 0.8*d :
            text = Paragraph("h >= 0,8d", equation_style)
            elements.append(text)
        else :
            text = Paragraph("h < 0,8d", equation_style)
            elements.append(text)
            
        if Le >= 0.8*d :
            text = Paragraph("L<sub>e</sub> >= 0,8d", equation_style)
            elements.append(text)
        else :
            text = Paragraph("L<sub>e</sub> < 0,8d", equation_style)
            elements.append(text)
            
        if SyminP_T >= SyminB_T :
            text = Paragraph("(R<sub>p0,2</sub>)<sub>min,p</sub> >= (R<sub>p0,2</sub>)<sub>min,b</sub>", equation_style)
            elements.append(text)
        else :
            text = Paragraph("(R<sub>p0,2</sub>)<sub>min,p</sub> < (R<sub>p0,2</sub>)<sub>min,b</sub>", equation_style)
            elements.append(text)
            
    
        elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    
    
    # Cas B2
    if 'B2' in Study_Case :
        text = Paragraph("La liaison boulonnée est précontrainte mais n’assure pas une fonction d’étanchéité. Elle entre donc dans la catégorie B2 et le dimensionnement se fait conformément au jeu de règles correspondant (RB 3281, RB 3284 et RB 3285). Le fluage ainsi que l’irradiation de la liaison sont négligés.", normal_style)
        elements.append(text)
        text = Paragraph("Les données complémentaires permettant de calculer les contraintes à vérifier sont :", normal_style)
        elements.append(text)
        
        list_B2 = ["Le coefficient de rigidité : &Lambda; = " + str(Lambda), "Le coefficient de frottement sous tête ou sous écrou : f' = " + str(ft), "Le coefficient de frottement entre les filets en prise : f = " + str(fv), "L'effort de précontrainte, F<sub>0</sub> = " + str(F0) + " N"]

        list_B2_flowable = ListFlowable([ListItem(Paragraph(item, normal_style)) for item in list_B2], bulletType='bullet', bulletIndent=20)  # Type de puce ('bullet' pour une puce classique))
        elements.append(list_B2_flowable)
                                        
        if F0_selection == "oui" :
            text = Paragraph("Cet effort de précontrainte est pris en compte dans les résultats des calculs ANSYS présentés ci-après.", normal_style)
            elements.append(text)
        else : 
            text = Paragraph("Cet effort de précontrainte n’est pas pris en compte dans les résultats des calculs ANSYS présentés ci-après.", normal_style)
            elements.append(text)
        
        if adherence_selection == "oui" :
            text = Paragraph("On suppose que les efforts extérieurs sont repris par adhérence.", normal_style)
            elements.append(text)
        else :
            text = Paragraph("On suppose que les efforts extérieurs ne sont pas repris par adhérence.", normal_style)
            elements.append(text)
        
        if selection1  == "oui" :
            text = Paragraph("De plus, l’élément de serrage subit un moment de flexion par effet levier dû à une flexion locale des pièces assemblées.", normal_style)
            elements.append(text)
        else :
            text = Paragraph("De plus, l’élément de serrage ne subit pas de moment de flexion par effet levier dû à une flexion locale des pièces assemblées. ", normal_style)
            elements.append(text)
        
        elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
        
    
    # Cas B3
    if 'B3' in Study_Case :
        text = Paragraph("La liaison boulonnée n’est pas précontrainte et a simplement une fonction de support. Elle entre donc dans la catégorie B3 et le dimensionnement se fait conformément au jeu de règles correspondant (RB 3281 et RB 3286). Le fluage ainsi que l’irradiation de la liaison sont négligés, d’autant plus qu’ils sont incompatibles avec cette catégorie de boulonnerie.", normal_style)
        elements.append(text)
        text = Paragraph("Les données complémentaires permettant de calculer les contraintes à vérifier sont :", normal_style)
        elements.append(text)
        
        list_B3 = ["L’entraxe ou la distance de l’axe des éléments de serrage au bord de la pièce assemblée dans la direction de l’effort : L = " + str(L) + " mm", "L’épaisseur de la pièce assemblée : t = " + str(e) + " mm"]
        list_B3_flowable = ListFlowable([ListItem(Paragraph(item, normal_style)) for item in list_B3], bulletType='bullet', bulletIndent=20)  # Type de puce ('bullet' pour une puce classique)
        elements.append(list_B3_flowable)
                                        

        if selection2  == "oui" :
            text = Paragraph("Enfin, l’élément de serrage subit un moment de flexion par effet levier dû à une flexion locale des pièces assemblées.", normal_style)
            elements.append(text)
        else :
            text = Paragraph("Enfin, l’élément de serrage ne subit pas de moment de flexion par effet levier dû à une flexion locale des pièces assemblées.", normal_style)
            elements.append(text)
        
        elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
        

    
    # =============================================================================
    #     Bilan des efforts sollicitant la liaison boulonnée
    # =============================================================================
                                  
    subsubtitle_4 = Paragraph("Bilan des efforts sollicitant la liaison boulonnée", subtitle3_style)
    elements.append(subsubtitle_4)
    
    text = Paragraph("Ces hypothèses permettent de dresser le tableau des efforts sollicitant l’élément de serrage, utilisés pour le calcul des contraintes.", normal_style)
    elements.append(text)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte

    Entete_T_Results_Ansys_Bilan = ["Numéro Boulon", "Ne [N]", "Nb [N]", "Te [N]", "Tb [N]", "Me [Nmm]", "Mb [Nmm]", "Cr [Nmm]", "Ct [Nmm]", "F0 [N]"]
    T_Results_Ansys_Bilan.insert(0, Entete_T_Results_Ansys_Bilan)
    table_results_ansys_bilan = Table(T_Results_Ansys_Bilan)
    table_results_ansys_bilan.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                               ('FONTSIZE', (0, 0), (-1, -1), 8),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                               ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                               # ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                               ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
                               ('BOX', (0, 0), (-1, -1), 0, colors.white), # Pas de contour
                               ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    elements.append(table_results_ansys_bilan)
    legend = Paragraph("Tableau 4 : Résultats des calculs ANSYS utilisés pour le dimensionnement de la boulonnerie en fonction des hypothèses renseignées", legend_style)
    elements.append(legend)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    text = Paragraph("avec", normal_style)
    elements.append(text)

    list_Result_Ansys = ["N<sub>e</sub> l'effort de traction ou de compression développé par les sollicitations d'origine externe, rapporté à l'axe de la liaison boulonnée",
                     "T<sub>e</sub> l'effort de cisaillement développé par les sollicitations d'origine externe, rapporté à l'axe de la liaison boulonnée",
                     "M<sub>e</sub> le moment de flexion développé par les sollicitations d'origine externe, rapporté à l'axe de la liaison boulonnée",
                     "N<sub>b</sub> l'effort de traction développé par les sollicitations d'origine externe et interne, rapporté à l'axe de la liaison boulonnée",
                     "T<sub>b</sub> l'effort de cisaillement développé par les sollicitations d'origine externe et interne, rapporté à l'axe de la liaison boulonnée",
                     "M<sub>b</sub> le moment de flexion développé par les sollicitations d'origine externe et interne, rapporté à l'axe de la liaison boulonnée",
                     "C<sub>r</sub> le couple de torsion résiduel sur les filets en prise",
                     "C<sub>t</sub> le couple de torsion résiduel sous tête",
                     "F<sub>0</sub> l'effort de préserrage initial"]
    list_Result_Ansys_flowable = ListFlowable([ListItem(Paragraph(item, normal_style)) for item in list_Result_Ansys], bulletType='bullet', bulletIndent=20)  # Type de puce ('bullet' pour une puce classique)
    elements.append(list_Result_Ansys_flowable)
    
    
    
    
    
    
    
# =============================================================================
#     Critères à vérifier
# =============================================================================
    # Saut de page
    elements.append(PageBreak())
                                  
    subtitle_2 = Paragraph("CRITÈRES À VÉRIFIER", subtitle2_style)
    elements.append(subtitle_2)
    elements.append(Spacer(1, 8))  # Ajouter un espace après le texte
        
    text = Paragraph("Les critères à vérifier dans cette étude sont de niveau "+ str(critere_selection) + '. Les hypothèses énoncées au paragraphe "Hypothèses de calcul" permettent de définir les critères dont la vérification est nécessaire. Ces critères sont les suivants.', normal_style)
    elements.append(text)

    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte

    
    if Study_Case == "B1_A" or Study_Case == "B1_C" :
        # Charger une image
        image_B1AC_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B1-AC_generaux.png"
        image_width = page_width - 2.16 * inch
        image_B1AC = Image(image_B1AC_path)
        image_B1AC.drawHeight = image_width * image_B1AC.drawHeight / image_B1AC.drawWidth
        image_B1AC.drawWidth = image_width
        elements.append(image_B1AC)
        if h >= 0.8*d :
            if str(bolt_type) == "Vis" or str(bolt_type) == "Goujon" :
                if float(SyminP_T) < float(SyminB_T) :
                    elements.append(Spacer(1, 10))  # Ajouter un espace après le texte
                    image_B1AC_h_sup_08d_2_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B1-AC_h sup 08d-2.png"
                    image_width = page_width - 2.16 * inch
                    image_B1AC_h_sup_08d_2 = Image(image_B1AC_h_sup_08d_2_path)
                    image_B1AC_h_sup_08d_2.drawHeight = image_width * image_B1AC_h_sup_08d_2.drawHeight / image_B1AC_h_sup_08d_2.drawWidth
                    image_B1AC_h_sup_08d_2.drawWidth = image_width
                    elements.append(image_B1AC_h_sup_08d_2)
                else :
                    if Le < 0.8*d :
                        elements.append(Spacer(1, 10))  # Ajouter un espace après le texte
                        image_B1AC_h_sup_08d_1_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B1-AC_h sup 08d-1.png"
                        image_width = page_width - 2.16 * inch
                        image_B1AC_h_sup_08d_1 = Image(image_B1AC_h_sup_08d_1_path)
                        image_B1AC_h_sup_08d_1.drawHeight = image_width * image_B1AC_h_sup_08d_1.drawHeight / image_B1AC_h_sup_08d_1.drawWidth
                        image_B1AC_h_sup_08d_1.drawWidth = image_width
                        elements.append(image_B1AC_h_sup_08d_1)
                    
        else :
            elements.append(Spacer(1, 10))  # Ajouter un espace après le texte
            image_B1AC_h_inf_08d_1_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B1-AC_h inf 08d-1.png"
            image_width = page_width - 2.16 * inch
            image_B1AC_h_inf_08d_1 = Image(image_B1AC_h_inf_08d_1_path)
            image_B1AC_h_inf_08d_1.drawHeight = image_width * image_B1AC_h_inf_08d_1.drawHeight / image_B1AC_h_inf_08d_1.drawWidth
            image_B1AC_h_inf_08d_1.drawWidth = image_width
            elements.append(image_B1AC_h_inf_08d_1)
            elements.append(Spacer(1, 10))  # Ajouter un espace après le texte
            image_B1AC_h_inf_08d_2_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B1-AC_h inf 08d-2.png"
            image_width = page_width - 2.16 * inch
            image_B1AC_h_inf_08d_2 = Image(image_B1AC_h_inf_08d_2_path)
            image_B1AC_h_inf_08d_2.drawHeight = image_width * image_B1AC_h_inf_08d_2.drawHeight / image_B1AC_h_inf_08d_2.drawWidth
            image_B1AC_h_inf_08d_2.drawWidth = image_width
            elements.append(image_B1AC_h_inf_08d_2)

                                  
    if Study_Case == "B1_D" :
        # Charger une image
        image_B1D_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B1-D_generaux.png"
        image_width = page_width - 2.16 * inch
        image_B1D = Image(image_B1D_path)
        image_B1D.drawHeight = image_width * image_B1D.drawHeight / image_B1D.drawWidth
        image_B1D.drawWidth = image_width
        elements.append(image_B1D)
        
        if str(bolt_type) == "Vis" or str(bolt_type) == "Goujon" :
            elements.append(Spacer(1, 10))  # Ajouter un espace après le texte
            # Charger une image
            image_B1D_vis_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B1-D_vis-goujon.png"
            image_width = page_width - 2.16 * inch
            image_B1D_vis = Image(image_B1D_vis_path)
            image_B1D_vis.drawHeight = image_width * image_B1D_vis.drawHeight / image_B1D_vis.drawWidth
            image_B1D_vis.drawWidth = image_width
            elements.append(image_B1D_vis)

    if Study_Case == "B2_A" :
        # Charger une image
        image_B2A_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B2-A_generaux.png"
        image_width = page_width - 2.16 * inch
        image_B2A = Image(image_B2A_path)
        image_B2A.drawHeight = image_width * image_B2A.drawHeight / image_B2A.drawWidth
        image_B2A.drawWidth = image_width
        elements.append(image_B2A)
        
        if str(bolt_type) == "Vis" or str(bolt_type) == "Goujon" :
            elements.append(Spacer(1, 10))  # Ajouter un espace après le texte
            # Charger une image
            image_B2A_vis_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B2-A_vis-goujon.png"
            image_width = page_width - 2.16 * inch
            image_B2A_vis = Image(image_B2A_vis_path)
            image_B2A_vis.drawHeight = image_width * image_B2A_vis.drawHeight / image_B2A_vis.drawWidth
            image_B2A_vis.drawWidth = image_width
            elements.append(image_B2A_vis)

    if Study_Case == "B2_C" :
        if float(SuminB_T) >= 700 :
            # Charger une image
            image_B2C_HR_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B2-C_HR.png"
            image_width = page_width - 2.16 * inch
            image_B2C_HR = Image(image_B2C_HR_path)
            image_B2C_HR.drawHeight = image_width * image_B2C_HR.drawHeight / image_B2C_HR.drawWidth
            image_B2C_HR.drawWidth = image_width
            elements.append(image_B2C_HR)
            if str(bolt_type) == "Vis" or str(bolt_type) == "Goujon" :
                elements.append(Spacer(1, 10))  # Ajouter un espace après le texte
                # Charger une image
                image_B2C_HR_vis_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B2-C_HR-et-vis-goujon.png"
                image_width = page_width - 2.16 * inch
                image_B2C_HR_vis = Image(image_B2C_HR_vis_path)
                image_B2C_HR_vis.drawHeight = image_width * image_B2C_HR_vis.drawHeight / image_B2C_HR_vis.drawWidth
                image_B2C_HR_vis.drawWidth = image_width
                elements.append(image_B2C_HR_vis)      
        else :
            # Charger une image
            image_B2C_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B2-C_generaux.png"
            image_width = page_width - 2.16 * inch
            image_B2C = Image(image_B2C_path)
            image_B2C.drawHeight = image_width * image_B2C.drawHeight / image_B2C.drawWidth
            image_B2C.drawWidth = image_width
            elements.append(image_B2C)
        
                            
    if Study_Case == "B2_D" :
        if float(SuminB_T) >= 700 :
            # Charger une image
            image_B2D_HR_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B2-D_HR.png"
            image_width = page_width - 2.16 * inch
            image_B2D_HR = Image(image_B2D_HR_path)
            image_B2D_HR.drawHeight = image_width * image_B2D_HR.drawHeight / image_B2D_HR.drawWidth
            image_B2D_HR.drawWidth = image_width
            elements.append(image_B2D_HR) 
        else :
            # Charger une image
            image_B2D_generaux_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B2-D_classique.png"
            image_width = page_width - 2.16 * inch
            image_B2D_generaux = Image(image_B2D_generaux_path)
            image_B2D_generaux.drawHeight = image_width * image_B2D_generaux.drawHeight / image_B2D_generaux.drawWidth
            image_B2D_generaux.drawWidth = image_width
            elements.append(image_B2D_generaux)                                       
        
    if Study_Case == "B3_A" :
        # Charger une image
        image_B3A_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B3-A.png"
        image_width = page_width - 2.16 * inch
        image_B3A = Image(image_B3A_path)
        image_B3A.drawHeight = image_width * image_B3A.drawHeight / image_B3A.drawWidth
        image_B3A.drawWidth = image_width
        elements.append(image_B3A)
        
    if Study_Case == "B3_C" :
        # Charger une image
        image_B3C_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B3-C.png"
        image_width = page_width - 2.16 * inch
        image_B3C = Image(image_B3C_path)
        image_B3C.drawHeight = image_width * image_B3C.drawHeight / image_B3C.drawWidth
        image_B3C.drawWidth = image_width
        elements.append(image_B3C)

    if Study_Case == "B3_D" :
        if float(SuminB_T) >= 700 :
            # Charger une image
            image_B3D_HR_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B3-D_HR.png"
            image_width = page_width - 2.16 * inch
            image_B3D_HR = Image(image_B3D_HR_path)
            image_B3D_HR.drawHeight = image_width * image_B3D_HR.drawHeight / image_B3D_HR.drawWidth
            image_B3D_HR.drawWidth = image_width
            elements.append(image_B3D_HR) 
        else :
            # Charger une image
            image_B3D_generaux_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B3-D_generaux.png"
            image_width = page_width - 2.16 * inch
            image_B3D_generaux = Image(image_B3D_generaux_path)
            image_B3D_generaux.drawHeight = image_width * image_B3D_generaux.drawHeight / image_B3D_generaux.drawWidth
            image_B3D_generaux.drawWidth = image_width
            elements.append(image_B3D_generaux)                                  
        


        
            
# =============================================================================
#     RESULTATS
# =============================================================================

    # Saut de page
    elements.append(PageBreak())
    
    subtitle_3 = Paragraph("RÉSULTATS", subtitle2_style)
    elements.append(subtitle_3)
    
    elements.append(Spacer(1, 8))  # Ajouter un espace après le texte
    
    text = Paragraph("L’évaluation des contraintes subies par la liaison boulonnée et des critères dimensionnants permet d’obtenir pour chacun des éléments de serrage les valeurs et marges suivantes", normal_style)
    elements.append(text)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    num_tableau = 5                              
    marge_min = 100.0
    for i in range(0, len(L_marge_full)) :
        tableau_bilan_marge = Table(L_marge_full[i])
        
        tableau_int = L_marge_full[i] # Tableau intermédiaire utilisé seulement pour déterminer la marge min, parce que plus simple à utiliser qu'un élément de type Table
        derniere_colonne = [float(ligne[-1]) for ligne in tableau_int[1:]] #tableau_int[1:] est le tableau sans l'entête
        marge_min_int = min(derniere_colonne) #On récupère la valeur min de la liaison i étudiée
        if marge_min_int < marge_min : # si la marge min du boulon étudié est plus faible que la marge min actuelle, alors la marge min devient celle-ci
            marge_min = marge_min_int
        
        tableau_bilan_marge.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                                   ('FONTSIZE', (0, 0), (-1, -1), 8),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                                   ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                                   # ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
                                   ('BOX', (0, 0), (-1, -1), 0, colors.white), # Pas de contour
                                   ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
        elements.append(tableau_bilan_marge)
        legend = Paragraph("Tableau " + str(num_tableau) + " : Bilan des critères et marges associées pour la liaison boulonnée " + str(i+1), legend_style)
        elements.append(legend)
        elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
        num_tableau = num_tableau + 1

    if marge_min >= 0.0 :                              
        text = Paragraph("Le dimensionnement des liaisons boulonnées étudiées est validé avec une marge minimale de " + str(marge_min) + " %", conclusion_style)
        elements.append(text)
    else :
        text = Paragraph("Le dimensionnement des liaisons boulonnées étudiées n'est pas validé avec une marge minimale de " + str(marge_min) + " %", conclusion_style)
        elements.append(text)  


                                  
# =============================================================================
#     DETAILS DES FORMULES UTILISEES
# =============================================================================
    # Saut de page
    elements.append(PageBreak())
                                  
    subtitle_4 = Paragraph("DÉTAIL DES FORMULES UTILISÉES", subtitle2_style)
    elements.append(subtitle_4)

    subsubtitle_5 = Paragraph("Données géométriques", subtitle3_style)
    elements.append(subsubtitle_5)
                                  
    image_geom_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_dimensions_geom.png"
    image_width = page_width - 2.16 * inch
    image_geom = Image(image_geom_path)
    image_geom.drawHeight = image_width * image_geom.drawHeight / image_geom.drawWidth
    image_geom.drawWidth = image_width
    elements.append(image_geom)
                                  
    # Saut de page
    elements.append(PageBreak())
    subsubtitle_6 = Paragraph("Efforts sollicitant la liaison boulonnée", subtitle3_style)
    elements.append(subsubtitle_6)
                                  
    image_efforts_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_efforts.png"
    image_width = page_width - 2.16 * inch
    image_efforts = Image(image_efforts_path)
    image_efforts.drawHeight = image_width * image_efforts.drawHeight / image_efforts.drawWidth
    image_efforts.drawWidth = image_width
    elements.append(image_efforts) 
                                  
    # Saut de page
    elements.append(PageBreak())                              
    subsubtitle_7 = Paragraph("Calcul des contraintes", subtitle3_style)
    elements.append(subsubtitle_7)    

    if Study_Case == "B1_A" or Study_Case == "B1_C" :                              
        image_B1AC_formules_1_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B1-AC_formules-1.png"
        image_width = page_width - 2.16 * inch
        image_B1AC_formules_1 = Image(image_B1AC_formules_1_path)
        image_B1AC_formules_1.drawHeight = image_width * image_B1AC_formules_1.drawHeight / image_B1AC_formules_1.drawWidth
        image_B1AC_formules_1.drawWidth = image_width
        elements.append(image_B1AC_formules_1)

        image_B1AC_formules_2_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B1-AC_formules-2.png"
        image_width = page_width - 2.16 * inch
        image_B1AC_formules_2 = Image(image_B1AC_formules_2_path)
        image_B1AC_formules_2.drawHeight = image_width * image_B1AC_formules_2.drawHeight / image_B1AC_formules_2.drawWidth
        image_B1AC_formules_2.drawWidth = image_width
        elements.append(image_B1AC_formules_2)                          
    
    if Study_Case == "B1_D" :
        image_B1D_formules_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B1-D_formules.png"
        image_width = page_width - 2.16 * inch
        image_B1D_formules = Image(image_B1D_formules_path)
        image_B1D_formules.drawHeight = image_width * image_B1D_formules.drawHeight / image_B1D_formules.drawWidth
        image_B1D_formules.drawWidth = image_width
        elements.append(image_B1D_formules)
        
    if Study_Case == "B2_A" :
        image_B2A_formules_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B2-A_formules.png"
        image_width = page_width - 2.16 * inch
        image_B2A_formules = Image(image_B2A_formules_path)
        image_B2A_formules.drawHeight = image_width * image_B2A_formules.drawHeight / image_B2A_formules.drawWidth
        image_B2A_formules.drawWidth = image_width
        elements.append(image_B2A_formules)

    if Study_Case == "B2_C" :
        image_B2C_formules_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B2-C_formules.png"
        image_width = page_width - 2.16 * inch
        image_B2C_formules = Image(image_B2C_formules_path)
        image_B2C_formules.drawHeight = image_width * image_B2C_formules.drawHeight / image_B2C_formules.drawWidth
        image_B2C_formules.drawWidth = image_width
        elements.append(image_B2C_formules)
                                  
    if Study_Case == "B2_D" :
        image_B2D_formules_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B2-D_formules.png"
        image_width = page_width - 2.16 * inch
        image_B2D_formules = Image(image_B2D_formules_path)
        image_B2D_formules.drawHeight = image_width * image_B2D_formules.drawHeight / image_B2D_formules.drawWidth
        image_B2D_formules.drawWidth = image_width
        elements.append(image_B2D_formules)

    if Study_Case == "B3_A" :
        image_B3A_formules_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B3-A_formules.png"
        image_width = page_width - 2.16 * inch
        image_B3A_formules = Image(image_B3A_formules_path)
        image_B3A_formules.drawHeight = image_width * image_B3A_formules.drawHeight / image_B3A_formules.drawWidth
        image_B3A_formules.drawWidth = image_width
        elements.append(image_B3A_formules)

    if Study_Case == "B3_C" :
        image_B3C_formules_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B3-C_formules.png"
        image_width = page_width - 2.16 * inch
        image_B3C_formules = Image(image_B3C_formules_path)
        image_B3C_formules.drawHeight = image_width * image_B3C_formules.drawHeight / image_B3C_formules.drawWidth
        image_B3C_formules.drawWidth = image_width
        elements.append(image_B3C_formules)     

    if Study_Case == "B3_D" :
        if float(SuminB_T) >= 700 :
            image_B3D_HR_formules_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B3-D_formules-HR.png"
            image_width = page_width - 2.16 * inch
            image_B3D_HR_formules = Image(image_B3D_HR_formules_path)
            image_B3D_HR_formules.drawHeight = image_width * image_B3D_HR_formules.drawHeight / image_B3D_HR_formules.drawWidth
            image_B3D_HR_formules.drawWidth = image_width
            elements.append(image_B3D_HR_formules) 
        else :
            image_B3D_NR_formules_path = "Pictures/RCC-MRx_Criteres_Formules/rcc_criteres-B3-D_formules.png"
            image_width = page_width - 2.16 * inch
            image_B3D_NR_formules = Image(image_B3D_NR_formules_path)
            image_B3D_NR_formules.drawHeight = image_width * image_B3D_NR_formules.drawHeight / image_B3D_NR_formules.drawWidth
            image_B3D_NR_formules.drawWidth = image_width
            elements.append(image_B3D_NR_formules) 


                                  

                                  
    # Génération du PDF
    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
    
    
    buffer.seek(0)
                                  
    return buffer
