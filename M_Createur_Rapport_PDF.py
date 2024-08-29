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






def create_rapport_pdf_rccmrx(bolt_type, df_bolt_geom_data_full, df_Bolt_Material_Data, B_acier_aust, df_assembly_part_data, Study_Case, Lambda, 
                              ft, fv, F0, F0_selection, adherence_selection, selection1, selection2, d, h, Le, SyminP_T, SyminB_T, L, e, T_Results_Ansys_Bilan,
                              critere_selection, L_marge_full) :
    
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
    title = Paragraph("ANNEXE : DIMENSIONNEMENT DE LA BOULONNERIE", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le titre
    
    
    
# =============================================================================
#     CODE
# =============================================================================
    
    subtitle_0 = Paragraph("CODE DE DIMENSIONNEMENT", subtitle2_style)
    elements.append(subtitle_0)
    
    text = Paragraph("Le code de dimensionnement utilisé pour cette étude est le RCC-MRx, selon les règles du RB 3280 pour l’évaluation des critères et de l’Annexe 6 pour le calcul des différentes contraintes. Les paragraphes correspondant aux équations utilisées seront précisés entre parenthèses. Il conviendra de s’y référer pour plus de détail.")
    elements.append(text)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    
# =============================================================================
#     SAISIE DES DONNEES D'ENTREE
# =============================================================================
    
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

    text = Paragraph("L'élément de serrage étudié est un/une " + str(bolt_type) + " et est supposé normalisé", normal_style)
    elements.append(text)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    # Données géométriques
    subsubsubtitle_2 = Paragraph("- Données géométriques", subtitle4_style)
    elements.append(subsubsubtitle_2)
    
    text = Paragraph("Les données géométriques de cet élément de serrage utilisées pour les calculs de dimensionnement sont résumées dans le Tableau 1 suivant.", normal_style)
    elements.append(text)
    # Convertir le DataFrame en une liste de listes
    bolt_geom_data = [df_bolt_geom_data_full.columns.tolist()] + df_bolt_geom_data_full.values.tolist()
    # col_widths = [145, 37, 35, 30] # Définition de la largeur des colonnes du tableau
    table_bolt_geom_data = Table(bolt_geom_data)
    table_bolt_geom_data.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
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
    
    elements.append(table_bolt_geom_data)
    legend = Paragraph("Tableau 1 : Données géométriques liées liées à l'élément de serrage", legend_style)
    elements.append(legend)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    
    # Matériau
    subsubsubtitle_3 = Paragraph("- Matériau", subtitle4_style)
    elements.append(subsubsubtitle_3)
    text = Paragraph("L'élément de serrage étudié est en " + str() + ". Les propriétés mécaniques utilisées, évaluées selon la température de calcul, sont présentées dans le Tableau 2 suivant.", normal_style)
    elements.append(text)
    bolt_material_data = [df_Bolt_Material_Data.columns.tolist()] + df_Bolt_Material_Data.values.tolist()
    table_bolt_material_data = Table(bolt_material_data)
    table_bolt_material_data.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
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
    elements.append(table_bolt_material_data)
    legend = Paragraph("Tableau 2 : Données matériau liées à l'élément de serrage", legend_style)
    elements.append(legend)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    # Acier austhénitique
    if B_acier_aust :
        text = Paragraph("Il s'agit d'un acier austhénitique", normal_style)
        elements.append(text)
    else :
        text = Paragraph("Il ne s'agit pas d'un acier austhénitique", normal_style)
        elements.append(text)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    
    
    # =============================================================================
    #     Pièces assemblées
    # =============================================================================
    
    subsubtitle_2 = Paragraph("Pièces assemblées", subtitle3_style)
    elements.append(subsubtitle_2)
    
    text = Paragraph("Les données liées aux pièces assemblées (matériaux et températures) sont présentées dans le Tableau 3 ci-dessous.", normal_style)
    elements.append(text)
    elements.append(Spacer(1, 4))  # Ajouter un espace après le sous sous titre
    
    
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
    legend = Paragraph("Tableau 3 : Données liées aux pièces assemblées", legend_style)
    elements.append(legend)
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
        text = Paragraph("  - Le coefficient de rigidité, &Lambda; : " + str(Lambda), normal_style)
        elements.append(text)
        text = Paragraph("  - Le coefficient de frottement sous tête ou sous écrou, f' : " + str(ft), normal_style)
        elements.append(text)
        text = Paragraph("  - Le coefficient de frottement enrte les filets en prise, f : " + str(fv), normal_style)
        elements.append(text)
        text = Paragraph("  - L'effort de précontrainte', F<sub>0</sub>; : " + str(F0) + " N", normal_style)
        elements.append(text)
        
        if F0_selection :
            text = Paragraph("Cet effort de précontrainte est pris en compte dans les calculs ANSYS présentés ci-dessus.", normal_style)
            elements.append(text)
        else : 
            text = Paragraph("Cet effort de précontrainte n’est pas pris en compte dans les calculs ANSYS présentés ci-dessus.", normal_style)
            elements.append(text)
        
        if adherence_selection :
            text = Paragraph("On suppose que les efforts extérieurs sont repris par adhérence.", normal_style)
            elements.append(text)
        else :
            text = Paragraph("On suppose que les efforts extérieurs ne sont pas repris par adhérence.", normal_style)
            elements.append(text)
        
        if selection1 :
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
            text = Paragraph("h >= 0,8d", normal_style)
            elements.append(text)
        else :
            text = Paragraph("h < 0,8d", normal_style)
            elements.append(text)
            
        if Le >= 0.8*d :
            text = Paragraph("L<sub>e</sub> >= 0,8d", normal_style)
            elements.append(text)
        else :
            text = Paragraph("L<sub>e</sub> < 0,8d", normal_style)
            elements.append(text)
            
        if SyminP_T >= SyminB_T :
            text = Paragraph("R<sub>p0,2p</sub> >= R<sub>p0,2b</sub>", normal_style)
            elements.append(text)
        else :
            text = Paragraph("R<sub>p0,2p</sub> < R<sub>p0,2b</sub>", normal_style)
            elements.append(text)
            
    
        elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    
    
    # Cas B2
    if 'B2' in Study_Case :
        text = Paragraph("La liaison boulonnée est précontrainte mais n’assure pas une fonction d’étanchéité. Elle entre donc dans la catégorie B2 et le dimensionnement se fait conformément au jeu de règles correspondant (RB 3281, RB 3284 et RB 3285). Le fluage ainsi que l’irradiation de la liaison sont négligés.", normal_style)
        elements.append(text)
        text = Paragraph("Les données complémentaires permettant de calculer les contraintes à vérifier sont :", normal_style)
        elements.append(text)
        text = Paragraph("  - Le coefficient de rigidité, &Lambda; : " + str(Lambda), normal_style)
        elements.append(text)
        text = Paragraph("  - Le coefficient de frottement sous tête ou sous écrou, f' : " + str(ft), normal_style)
        elements.append(text)
        text = Paragraph("  - Le coefficient de frottement enrte les filets en prise, f : " + str(fv), normal_style)
        elements.append(text)
        text = Paragraph("  - L'effort de précontrainte', F<sub>0</sub>; : " + str(F0) + " N", normal_style)
        elements.append(text)
        
        if F0_selection :
            text = Paragraph("Cet effort de précontrainte est pris en compte dans les calculs ANSYS présentés ci-dessus.", normal_style)
            elements.append(text)
        else : 
            text = Paragraph("Cet effort de précontrainte n’est pas pris en compte dans les calculs ANSYS présentés ci-dessus.", normal_style)
            elements.append(text)
        
        if adherence_selection :
            text = Paragraph("On suppose que les efforts extérieurs sont repris par adhérence.", normal_style)
            elements.append(text)
        else :
            text = Paragraph("On suppose que les efforts extérieurs ne sont pas repris par adhérence.", normal_style)
            elements.append(text)
        
        if selection1 :
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
        text = Paragraph("  - L’entraxe ou la distance de l’axe des éléments de serrage au bord de la pièce assemblée dans la direction de l’effort, L : " + str(L) + " mm", normal_style)
        elements.append(text)
        text = Paragraph("  - L’épaisseur de la pièce assemblée, e : " + str(e) + " mm", normal_style)
        elements.append(text)

        if selection2 :
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

    Entete_T_Results_Ansys_Bilan = ["Numéro Boulon", "NbPL", "NbAL", "TbPL", "TbAL", "MbPL", "MbAL", "Cr", "Ct", "F0"]
    T_Results_Ansys_Bilan.insert(0, Entete_T_Results_Ansys_Bilan)
    table_results_ansys_bilan = Table(T_Results_Ansys_Bilan)
    table_results_ansys_bilan.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
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
    elements.append(table_results_ansys_bilan)
    legend = Paragraph("Tableau 4 : Résultats des calculs ANSYS utilisés pour le dimensionnement de la boulonnerie en fonction des hypothèses renseignées", legend_style)
    elements.append(legend)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    
    
    
    
    
    
# =============================================================================
#     Critères à vérifier
# =============================================================================
    subtitle_2 = Paragraph("CRITERES A VERIFIER", subtitle2_style)
    elements.append(subtitle_2)
    elements.append(Spacer(1, 8))  # Ajouter un espace après le texte
        
    text = Paragraph("Les critères à vérifier dans cette étude sont de niveau "+ str(critere_selection) + ". Les hypothèses posées au paragraphe 1.2.3 permettent de définir les critères dont la vérification est nécessaire. Ces critères sont les suivants.", normal_style)
    elements.append(text)
    
    text = Paragraph("A compléter", normal_style)
    elements.append(text)
    
    
    
    
        
        
    """        
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
    
    tableau_bilan_marge = Table(L_marge_full)
    tableau_bilan_marge.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
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
    elements.append(tableau_bilan_marge)
    legend = Paragraph("Tableau 5 : Bilan des critères et marges associées pour les liaisons boulonnées étudiées", legend_style)
    elements.append(legend)
    elements.append(Spacer(1, 12))  # Ajouter un espace après le texte
    
    
    
    """

    # Génération du PDF
    doc.build(elements)
    
    
    buffer.seek(0)
                                  
    return buffer
