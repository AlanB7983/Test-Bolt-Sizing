# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 11:03:09 2024

@author: admin
"""



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




def create_pdf_eurocode(bolt_type, bolt_diameter, bolt_classe, tete_fraisee_check, resine_check, df_bolt_data, df_assembly_data, recouvrement_une_rangee, plan_cisaill, df_loads_data, L_cat, tp , Lj, Result_Cat_A, Result_Cat_B, Result_Cat_C, Result_Cat_D, Result_Cat_E, Result_Cat_Combine, marge_min_A, marge_min_B, marge_min_C, marge_min_D, marge_min_E, marge_min_combine):
    buffer = BytesIO()
    
    #Configuration du document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    page_width = letter[0] # Largeur de la page

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    # Styles de texte
    subtitle_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading2'],
        fontName='Times-Bold',  # Police pour Heading1
        fontSize=16,
        spaceAfter=12,
        firstLineIndent=0  # Indentation de la première ligne (en points)
    )
    subsubtitle_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading3'],
        fontName='Times-Bold',  # Police pour Heading2
        fontSize=14,
        spaceAfter=10,
        spaceBefore=10,
        firstLineIndent=10  # Indentation de la première ligne (en points)
    )
    subsubsubtitle_style = ParagraphStyle(
        'Heading3Custom',
        parent=styles['Heading4'],
        fontName='Times-Italic',  # Police pour Heading3
        fontSize=12,
        spaceAfter=8,
        spaceBefore=20,
        firstLineIndent=20  # Indentation de la première ligne (en points)
    )
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
    
    # Saut de ligne
    espace = Spacer(1, 12)
    
    #Ajout du titre
    title = Paragraph("ANNEXE : DIMENSIONNEMENT DE LA BOULONNERIE", title_style)
    elements.append(title)
    elements.append(espace) #Ajouter un espace après le titre
    
    
    
    
    # =============================================================================
    #     1. CODE DE DIMENSIONNEMENT
    # =============================================================================
        
    subtitle_1 = Paragraph("Code de dimensionnement", subtitle_style)
    elements.append(subtitle_1)

    text_1 = Paragraph("Pour cette étude, la boulonnerie est dimensionnée selon la norme NF EN 1993-1-8 (Eurocode 3 pour le calcul des assemblages). Les paragraphes correspondant aux équations utilisées seront précisés entre parenthèses. Il conviendra de s'y référer pour plus de détails.", normal_style)
    elements.append(text_1)
    elements.append(espace)
    
    
    
    # =============================================================================
    #     2. DONNEES D'ENTREE
    # =============================================================================
    
    # Saut de page
    elements.append(PageBreak())
    
    subtitle_2 = Paragraph("Données d'entrée", subtitle_style)
    elements.append(subtitle_2)
    
    
        # =============================================================================
        #     2.1 Elément de serrage
        # =============================================================================
    
    subsubtitle_2_1 = Paragraph("Elément de serrage", subsubtitle_style)
    elements.append(subsubtitle_2_1)
    
    
            # =============================================================================
            #     2.1.1 Type d'élément de serrage
            # =============================================================================

    subsubsubtitle_2_1_1 = Paragraph("Type d'élément de serrage", subsubsubtitle_style)
    elements.append(subsubsubtitle_2_1_1)
    
    if not tete_fraisee_check :
        text_2_1_1 = "L'élément de serrage étudié est un " + str(bolt_type) + " M" + str(bolt_diameter) + " de classe " + str(bolt_classe) + ", à tête non fraisée et supposé normalisé."
    else :
        text_2_1_1 = "L'élément de serrage étudié est un " + str(bolt_type) + " M" + str(bolt_diameter) + " de classe " + str(bolt_classe) + ", à tête fraisée et supposé normalisé."
    
    if resine_check :
        text_2_1_1 = text_2_1_1 + " Il est injecté."
    else :
        text_2_1_1 = text_2_1_1 + " Il n'est pas injecté."
        
    if bolt_classe == "8.8" or bolt_classe == "10.9" :
        text_2_1_1 = text_2_1_1 + " Il s'agit d'un élément de serrage haute résistance."
    else : 
        text_2_1_1 = text_2_1_1 + " Il s'agit d'un élément de serrage normal."
   
    text_2_1_1 = Paragraph(text_2_1_1, normal_style)
    elements.append(text_2_1_1)
    elements.append(espace)
    
    
            # =============================================================================
            #     2.1.2 Données
            # =============================================================================
            
    subsubsubtitle_2_1_2 = Paragraph("Données", subsubsubtitle_style)
    elements.append(subsubsubtitle_2_1_2)

    text_2_1_2 = Paragraph("Les données liées à cet élément de serrage, utilisées pour les calculs de dimensionnement, sont résumées dans le Tableau 1 ci-dessous.", normal_style)
    elements.append(text_2_1_2)
    elements.append(espace)
    
    bolt_data = [df_bolt_data.columns.tolist()] + df_bolt_data.values.tolist()    
    table_bolt_data = Table(bolt_data)
    table_bolt_data.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
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
    elements.append(table_bolt_data)
    legend = Paragraph("Tableau 1 : Données liées à l'élément de serrage", legend_style)
    elements.append(legend)
    elements.append(espace)  # Ajouter un espace après le texte
    
    
        # =============================================================================
        #     2.2 Assemblage
        # =============================================================================
  
    # Saut de page
    elements.append(PageBreak())
  
    subsubtitle_2_2 = Paragraph("Assemblage", subsubtitle_style)
    elements.append(subsubtitle_2_2)

    subsubsubtitle_2_2_1 = Paragraph("Données", subsubsubtitle_style)
    elements.append(subsubsubtitle_2_2_1)

    text_2_2_1 = Paragraph("Les données liées aux pièces assemblées et à la disposition des liaisons boulonnées sont présentées dans le Tableau 2 ci-dessous.", normal_style)
    elements.append(text_2_2_1)
    elements.append(espace)
    
    assembly_data = [df_assembly_data.columns.tolist()] + df_assembly_data.values.tolist()    
    table_assembly_data = Table(assembly_data)
    table_assembly_data.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
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
    elements.append(table_assembly_data)
    legend = Paragraph("Tableau 2 : Données liées aux pièces assemblées et à l'assemblage", legend_style)
    elements.append(legend)
    elements.append(espace)  # Ajouter un espace après le texte

    if recouvrement_une_rangee :
        text_2_2_1bis = "Cet assemblage est à simple recouvrement à une rangée de boulons."
    else :
        text_2_2_1bis = ""

    if plan_cisaill == "filets" :
        text_2_2_1bis = text_2_2_1bis + " De plus, le plan de cisaillement se situe dans les filets de l'élément de serrage."
    else :
        text_2_2_1bis = text_2_2_1bis + " De plus, le plan de cisaillement se situe dans le fût lisse de l'élément de serrage."
    
    text_2_2_1bis = Paragraph(text_2_2_1bis, normal_style)
    elements.append(text_2_2_1bis)
    elements.append(espace)
    
    
        # =============================================================================
        #     2.3 Bilan des efforts
        # =============================================================================
  
    # Saut de page
    elements.append(PageBreak())
  
    subsubtitle_2_3 = Paragraph("Bilan des efforts sollicitant", subsubtitle_style)
    elements.append(subsubtitle_2_3)
    
    text_2_3_1 = Paragraph("Les efforts qui s'appliquent à l'élément de serrage sont les suivants.", normal_style)
    elements.append(text_2_3_1)
    elements.append(espace)

    loads_data = [df_loads_data.columns.tolist()] + df_loads_data.values.tolist()    
    table_loads_data = Table(loads_data)
    table_loads_data.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
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
    elements.append(table_loads_data)
    legend = Paragraph("Tableau 3 : Résultats des calculs ANSYS utilisés pour le dimensionnement de la boulonnerie en fonction des hypothèses renseignées", legend_style)
    elements.append(legend)
    elements.append(espace)  # Ajouter un espace après le texte
    
    text_2_3_1bis = Paragraph("Avec :", normal_style)
    elements.append(text_2_3_1bis)
    text_2_3_1bis = Paragraph("- Fv,x,Ed la composante sur X de l'effort de cisaillement à l'état limite ultime, rapporté à l'axe de la liaison boulonnée", normal_style)
    elements.append(text_2_3_1bis)
    text_2_3_1bis = Paragraph("- Fv,y,Ed la composante sur Y de l'effort de cisaillement à l'état limite ultime, rapporté à l'axe de la liaison boulonnée", normal_style)
    elements.append(text_2_3_1bis)
    text_2_3_1bis = Paragraph("- Fv,x,Ed,ser la composante sur X de l'effort de cisaillement à l'état limite de service, rapporté à l'axe de la liaison boulonnée", normal_style)
    elements.append(text_2_3_1bis)
    text_2_3_1bis = Paragraph("- Fv,y,Ed,ser la composante sur Y de l'effort de cisaillement à l'état limite de service, rapporté à l'axe de la liaison boulonnée", normal_style)
    elements.append(text_2_3_1bis)
    text_2_3_1bis = Paragraph("- Ft,Ed l'effort de cisaillement à l'état limite ultime, rapporté à l'axe de la liaison boulonnée", normal_style)
    elements.append(text_2_3_1bis)
    text_2_3_1bis = Paragraph("- Ft,Ed,ser l'effort de traction à l'état limite de service, rapporté à l'axe de la liaison boulonnée", normal_style)
    elements.append(text_2_3_1bis)
    text_2_3_1bis = Paragraph("- F0 l'effort de préserrage", normal_style)
    elements.append(text_2_3_1bis)

    elements.append(espace)
    
    
        # =============================================================================
        #      3 Criteres
        # =============================================================================
   
    # Saut de page
    elements.append(PageBreak())
  
    subtitle_3 = Paragraph("Critères à vérifier", subtitle_style)
    elements.append(subtitle_3)
    
    text_3 = "Les efforts sollicitant mentionnés précédemment permettent d'établir la ou les catégories de dimensionnement de l'élément de serrage."
    
    if L_cat[0] : # Catégorie A - texte
        text_3 = text_3 + " Ici, il appartient à la catégorie A. D'après le Tableau 3.2 de la norme NF EN 1998-8-1, les critères à vérifier sont les suivants."
        
    if L_cat[1] : # Catégorie B - texte
        text_3 = text_3 + " Ici, il appartient à la catégorie B. D'après le Tableau 3.2 de la norme NF EN 1998-8-1, les critères à vérifier sont les suivants."
    
    if L_cat[2] : # Catégorie C - texte
        text_3 = text_3 + " Ici, il appartient à la catégorie C. D'après le Tableau 3.2 de la norme NF EN 1998-8-1, les critères à vérifier sont les suivants."
        
    if L_cat[3] : # Catégorie D - texte
        text_3 = text_3 + " Ici, il appartient à la catégorie D. D'après le Tableau 3.2 de la norme NF EN 1998-8-1, les critères à vérifier sont les suivants."

    if L_cat[4] : # Catégorie E - texte
        text_3 = text_3 + " Ici, il appartient à la catégorie E. D'après le Tableau 3.2 de la norme NF EN 1998-8-1, les critères à vérifier sont les suivants."
        
    if L_cat[0] and L_cat[3] :
        text_3 = text_3 + " Ici, il appartient aux catégories A et D. D'après le Tableau 3.2 de la norme NF EN 1998-8-1, les critères à vérifier sont les suivants."
        
    if L_cat[1] and L_cat[4] :
        text_3 = text_3 + " Ici, il appartient aux catégories B et E. D'après le Tableau 3.2 de la norme NF EN 1998-8-1, les critères à vérifier sont les suivants."

    if L_cat[3] and L_cat[4] :
        text_3 = text_3 + " Ici, il appartient aux catégories C et E. D'après le Tableau 3.2 de la norme NF EN 1998-8-1, les critères à vérifier sont les suivants."

    text_3 = Paragraph(text_3, normal_style)
    elements.append(text_3)
    elements.append(espace)
    
   
    if L_cat[0] : # Catégorie A - criteres 
        # traceurA = Paragraph("CatA")
        # elements.append(traceurA)
        if resine_check :
            # traceurA = Paragraph("CatAi")
            # elements.append(traceurA)
            image_A_general_path = "Pictures/EUROCODE_Criteres_Formules/eurocode_critere_CatA-injecte.png"
            image_width = page_width - 2.16*inch
            image_A_general = Image(image_A_general_path)
            image_A_general.drawHeight = image_width * image_A_general.drawHeight / image_A_general.drawWidth
            image_A_general.drawWidth = image_width
            elements.append(image_A_general)
        else :
            # traceurA = Paragraph("CatAg")
            # elements.append(traceurA)
            image_A_general_path = "Pictures/EUROCODE_Criteres_Formules/eurocode_critere_CatA.png"
            image_width = page_width - 2.16*inch
            image_A_general = Image(image_A_general_path)
            image_A_general.drawHeight = image_width * image_A_general.drawHeight / image_A_general.drawWidth
            image_A_general.drawWidth = image_width
            elements.append(image_A_general)
    
    if L_cat[1] : # Catégorie B - criteres
        traceurB = Paragraph("CatB")
        elements.append(traceurB)        
        if resine_check :
            traceurB = Paragraph("CatBi")
            elements.append(traceurB)  
            image_B_general_path = "Pictures/EUROCODE_Criteres_Formules/eurocode_critere_CatB-injecte.png"
            image_width = page_width - 2.16*inch
            image_B_general = Image(image_B_general_path)
            image_B_general.drawHeight = image_width * image_B_general.drawHeight / image_B_general.drawWidth
            image_B_general.drawWidth = image_width
            elements.append(image_B_general)
        else :
            traceurB = Paragraph("CatBg")
            elements.append(traceurB)  
            image_B_general_path = "Pictures/EUROCODE_Criteres_Formules/eurocode_critere_CatB.png"
            image_width = page_width - 2.16*inch
            image_B_general = Image(image_B_general_path)
            image_B_general.drawHeight = image_width * image_B_general.drawHeight / image_B_general.drawWidth
            image_B_general.drawWidth = image_width
            elements.append(image_B_general)
    
    if L_cat[2] : # Catégorie C - criteres
        traceurC = Paragraph("CatC")
        elements.append(traceurC)         
        if resine_check :
            traceurC = Paragraph("CatCi")
            elements.append(traceurC)
            image_C_general_path = "Pictures/EUROCODE_Criteres_Formules/eurocode_critere_CatC-injecte.png"
            image_width = page_width - 2.16*inch
            image_C_general = Image(image_C_general_path)
            image_C_general.drawHeight = image_width * image_C_general.drawHeight / image_C_general.drawWidth
            image_C_general.drawWidth = image_width
            elements.append(image_C_general)
        else :
            traceurC = Paragraph("CatCg")
            elements.append(traceurC)
            image_C_general_path = "Pictures/EUROCODE_Criteres_Formules/eurocode_critere_CatC.png"
            image_width = page_width - 2.16*inch
            image_C_general = Image(image_C_general_path)
            image_C_general.drawHeight = image_width * image_C_general.drawHeight / image_C_general.drawWidth
            image_C_general.drawWidth = image_width
            elements.append(image_C_general)
    
    if L_cat[3] or L_cat[4] : # Catégorie D ou E - criteres
        traceurDE = Paragraph("CatDE")
        elements.append(traceurDE)      
        image_DE_general_path = "Pictures/EUROCODE_Criteres_Formules/eurocode_critere_CatDE.png"
        image_width = page_width - 2.16*inch
        image_DE_general = Image(image_DE_general_path)
        image_DE_general.drawHeight = image_width * image_DE_general.drawHeight / image_DE_general.drawWidth
        image_DE_general.drawWidth = image_width
        elements.append(Spacer(1, 10))
        elements.append(image_DE_general)
              
    if L_cat[5] : # Efforts combinés
        traceurComb = Paragraph("CatComb")
        elements.append(traceurComb)
        image_comb_general_path = "Pictures/EUROCODE_Criteres_Formules/eurocode_critere_combines.png"
        image_width = page_width - 2.16*inch
        image_comb_general = Image(image_comb_general_path)
        image_comb_general.drawHeight = image_width * image_comb_general.drawHeight / image_comb_general.drawWidth
        image_comb_general.drawWidth = image_width
        elements.append(Spacer(1, 10))
        elements.append(image_comb_general)
    
    
        # =============================================================================
        #      4 Résultats
        # =============================================================================
   
    # Saut de page
    elements.append(PageBreak())
  
    subtitle_4 = Paragraph("Résultats", subtitle_style)
    elements.append(subtitle_4)
    
    text_4 = Paragraph("L'évaluation des efforts limites présentés ci-dessus permet d'obtenir, par liaison boulonnée, les valeurs et les marges suivantes.", normal_style)
    elements.append(text_4)
    elements.append(espace)
    
    #tableaux
    num_tabeau = 4
    if L_cat[0] :
        Table_Result_Cat_A = Table(Result_Cat_A)
        Table_Result_Cat_A.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
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
        elements.append(Table_Result_Cat_A)
        legend = Paragraph("Tableau " + str(num_tabeau) + " : Résultats du dimensionnement pour les critères de catégorie A", legend_style)
        elements.append(legend)
        elements.append(espace)  # Ajouter un espace après le texte
        num_tabeau += 1 # On met à jour le numéro du tableau

        # On ajoute une phrase de conclusion
        if marge_min_A >= 0 :
            text = Paragraph("Le dimensionnement en catégorie A est validé avec une marge minimale de " + str(marge_min_A) + " %.", conclusion_style)
        else :
            text = Paragraph("Le dimensionnement en catégorie A n'est pas validé avec une marge minimale de " + str(marge_min_A) + " %.", conclusion_style)
        elements.append(text)  
        elements.append(espace)  # Ajouter un espace après le texte

    if L_cat[1] :
        Table_Result_Cat_B = Table(Result_Cat_B)
        Table_Result_Cat_B.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
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
        elements.append(Table_Result_Cat_B)
        legend = Paragraph("Tableau " + str(num_tabeau) + " : Résultats du dimensionnement pour les critères de catégorie B", legend_style)
        elements.append(legend)
        elements.append(espace)  # Ajouter un espace après le texte
        num_tabeau += 1 # On met à jour le numéro du tableau

        # On ajoute une phrase de conclusion
        if marge_min_B >= 0 :
            text = Paragraph("Le dimensionnement en catégorie B est validé avec une marge minimale de " + str(marge_min_B) + " %.", conclusion_style)
        else :
            text = Paragraph("Le dimensionnement en catégorie B n'est pas validé avec une marge minimale de " + str(marge_min_B) + " %.", conclusion_style)
        elements.append(text)  
        elements.append(espace)  # Ajouter un espace après le texte

    if L_cat[2] :
        Table_Result_Cat_C = Table(Result_Cat_C)
        Table_Result_Cat_C.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
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
        elements.append(Table_Result_Cat_C)
        legend = Paragraph("Tableau " + str(num_tabeau) + " : Résultats du dimensionnement pour les critères de catégorie C", legend_style)
        elements.append(legend)
        elements.append(espace)  # Ajouter un espace après le texte
        num_tabeau += 1 # On met à jour le numéro du tableau

        # On ajoute une phrase de conclusion
        if marge_min_C >= 0 :
            text = Paragraph("Le dimensionnement en catégorie C est validé avec une marge minimale de " + str(marge_min_C) + " %.", conclusion_style)
        else :
            text = Paragraph("Le dimensionnement en catégorie C n'est pas validé avec une marge minimale de " + str(marge_min_C) + " %.", conclusion_style)
        elements.append(text)  
        elements.append(espace)  # Ajouter un espace après le texte

    if L_cat[3] :
        Table_Result_Cat_D = Table(Result_Cat_D)
        Table_Result_Cat_D.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
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
        elements.append(Table_Result_Cat_D)
        legend = Paragraph("Tableau " + str(num_tabeau) + " : Résultats du dimensionnement pour les critères de catégorie D", legend_style)
        elements.append(legend)
        elements.append(espace)  # Ajouter un espace après le texte
        num_tabeau += 1 # On met à jour le numéro du tableau

        # On ajoute une phrase de conclusion
        if marge_min_D >= 0 :
            text = Paragraph("Le dimensionnement en catégorie D est validé avec une marge minimale de " + str(marge_min_D) + " %.", conclusion_style)
        else :
            text = Paragraph("Le dimensionnement en catégorie D n'est pas validé avec une marge minimale de " + str(marge_min_D) + " %.", conclusion_style)
        elements.append(text)  
        elements.append(espace)  # Ajouter un espace après le texte

    if L_cat[4] :
        Table_Result_Cat_E = Table(Result_Cat_E)
        Table_Result_Cat_E.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
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
        elements.append(Table_Result_Cat_E)
        legend = Paragraph("Tableau " + str(num_tabeau) + " : Résultats du dimensionnement pour les critères de catégorie E", legend_style)
        elements.append(legend)
        elements.append(espace)  # Ajouter un espace après le texte
        num_tabeau += 1 # On met à jour le numéro du tableau

        # On ajoute une phrase de conclusion
        if marge_min_E >= 0 :
            text = Paragraph("Le dimensionnement en catégorie E est validé avec une marge minimale de " + str(marge_min_E) + " %.", conclusion_style)
        else :
            text = Paragraph("Le dimensionnement en catégorie E n'est pas validé avec une marge minimale de " + str(marge_min_E) + " %.", conclusion_style)
        elements.append(text)  
        elements.append(espace)  # Ajouter un espace après le texte

    if L_cat[5] :
        Table_Result_Cat_Combine = Table(Result_Cat_Combine)
        Table_Result_Cat_Combine.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
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
        elements.append(Table_Result_Cat_Combine)
        legend = Paragraph("Tableau " + str(num_tabeau) + " : Résultats du dimensionnement pour les critères de cisaillement et traction combinés", legend_style)
        elements.append(legend)
        elements.append(espace)  # Ajouter un espace après le texte
        num_tabeau += 1 # On met à jour le numéro du tableau

        # On ajoute une phrase de conclusion
        if marge_min_combine >= 0 :
            text = Paragraph("Le dimensionnement en cisaillement et traction combinés est validé avec une marge minimale de " + str(marge_min_combine) + " %.", conclusion_style)
        else :
            text = Paragraph("Le dimensionnement en cisaillement et traction combinés n'est pas validé avec une marge minimale de " + str(marge_min_combine) + " %.", conclusion_style)
        elements.append(text)  
        elements.append(espace)  # Ajouter un espace après le texte

    




    
    
        # =============================================================================
        #      5 Détails
        # =============================================================================
   
    # Saut de page
    elements.append(PageBreak())
  
    subtitle_4 = Paragraph("Détails des formules utilisées", subtitle_style)
    elements.append(subtitle_4)


            # =============================================================================
            #      Catégorie A
            # =============================================================================
         
    if L_cat[0] :
        
        # Résistance au cisaillement FvRd
        if tp > bolt_diameter/3 :
            image_A_general_path = "Pictures/EUROCODE_Criteres_Formules/eurocode_formules_CatA_FvRd-tp.png"
            image_width = page_width - 2.16*inch
            image_A_general = Image(image_A_general_path)
            image_A_general.drawHeight = image_width * image_A_general.drawHeight / image_A_general.drawWidth
            image_A_general.drawWidth = image_width
            if Lj > 15*bolt_diameter :
                image_A_general_path = "Pictures/EUROCODE_Criteres_Formules/eurocode_formules_CatA_FvRd-tp-Lj.png"
                image_width = page_width - 2.16*inch
                image_A_general = Image(image_A_general_path)
                image_A_general.drawHeight = image_width * image_A_general.drawHeight / image_A_general.drawWidth
                image_A_general.drawWidth = image_width
        else :
            if Lj > 15*bolt_diameter :
                image_A_general_path = "Pictures/EUROCODE_Criteres_Formules/eurocode_formules_CatA_FvRd-Lj.png"
                image_width = page_width - 2.16*inch
                image_A_general = Image(image_A_general_path)
                image_A_general.drawHeight = image_width * image_A_general.drawHeight / image_A_general.drawWidth
                image_A_general.drawWidth = image_width
            else :
                image_A_general_path = "Pictures/EUROCODE_Criteres_Formules/eurocode_formules_CatA_FvRd-general.png"
                image_width = page_width - 2.16*inch
                image_A_general = Image(image_A_general_path)
                image_A_general.drawHeight = image_width * image_A_general.drawHeight / image_A_general.drawWidth
                image_A_general.drawWidth = image_width
        
        elements.append(image_A_general)
        
        # Résistance à la pression diamétrale FbRd
        if resine_check :
            image_A_general_path = "Pictures/EUROCODE_Criteres_Formules/eurocode_formules_CatA_FbRd-injecte.png"
            image_width = page_width - 2.16*inch
            image_A_general = Image(image_A_general_path)
            image_A_general.drawHeight = image_width * image_A_general.drawHeight / image_A_general.drawWidth
            image_A_general.drawWidth = image_width
            elements.append(image_A_general)
            if recouvrement_une_rangee :
                image_A_general_path = "Pictures/EUROCODE_Criteres_Formules/eurocode_formules_CatA_FbRd-supplement simple recouvrement.png"
                image_width = page_width - 2.16*inch
                image_A_general = Image(image_A_general_path)
                image_A_general.drawHeight = image_width * image_A_general.drawHeight / image_A_general.drawWidth
                image_A_general.drawWidth = image_width
                elements.append(image_A_general)
        else :
            image_A_general_path = "Pictures/EUROCODE_Criteres_Formules/eurocode_formules_CatA_FbRd-general.png"
            image_width = page_width - 2.16*inch
            image_A_general = Image(image_A_general_path)
            image_A_general.drawHeight = image_width * image_A_general.drawHeight / image_A_general.drawWidth
            image_A_general.drawWidth = image_width
            elements.append(image_A_general)
            if recouvrement_une_rangee :
                image_A_general_path = "Pictures/EUROCODE_Criteres_Formules/eurocode_formules_CatA_FbRd-supplement simple recouvrement.png"
                image_width = page_width - 2.16*inch
                image_A_general = Image(image_A_general_path)
                image_A_general.drawHeight = image_width * image_A_general.drawHeight / image_A_general.drawWidth
                image_A_general.drawWidth = image_width
                elements.append(image_A_general)
                
    
            # =============================================================================
            #      Catégorie B
            # =============================================================================
         
    # if cat_bolt == "B" :

    
    
    
    #Génération du PDF
    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
    buffer.seek(0)
    
    return buffer





