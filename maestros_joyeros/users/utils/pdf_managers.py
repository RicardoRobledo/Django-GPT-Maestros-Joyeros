from django.http import HttpResponse
from django.utils import timezone

from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Image, SimpleDocTemplate
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from .graph_managers import create_radar_chart


__author__ = 'Ricardo'
__version__ = '0.1'


def create_single_report(user, total_simulations, user_simulation_evaluation, total_workshops, user_workshop_scores):

    date = timezone.now().strftime('%d-%m-%Y')

    # Create a HttpResponse object with the correct PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f"attachment; filename=Reporte_{user.middle_name}{user.last_name}{user.first_name}_{date}.pdf"

    # Create the PDF object using reportlab
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='Title',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.white,
        alignment=1,  # Center align
        spaceAfter=14,
        wordWrap='CJK'  # Ensure word wrapping
    )
    normal_style = styles['Normal']
    heading_style = ParagraphStyle(
        name='Heading', parent=styles['Heading1'], alignment=1, spaceAfter=14, fontSize=14)
    right_aligned_style = ParagraphStyle(
        name='RightAligned', parent=styles['Normal'], alignment=2, spaceAfter=14)

    info = [
        [Paragraph(
            'Evaluación para vendedores de los últimos 31 días', title_style), ''],
        ['Nombre completo',
            f'{user.first_name} {user.middle_name} {user.last_name}'],
        ['Fecha de expedición del reporte', f'{date}']
    ]

    # Añadir columnas de padding
    info_table = Table(info, colWidths=[240, 240])
    info_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),  # Span the title across the inner columns
        # Center all cells horizontally
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        # Center the title cell vertically
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        # Larger font size for the title
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        # Background color for the title
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        # Text color for the title
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        # Top padding for the title row
        ('TOPPADDING', (0, 0), (-1, -1), 12),  # Top padding for all rows
        # Bottom padding for all rows
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        # Background color for other rows
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        # Text color for other rows
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 12),  # Font size for other rows
        ('LEFTPADDING', (0, 0), (-1, -1), 12),  # Left padding for all rows
        # Right padding for all rows
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Border around the table
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))  # Additional spacer after the table

    # Add data table
    data = [["Tema", "Veces que se tomó", "Promedio"]]  # Header
    for metric in user_workshop_scores:
        data.append(
            [metric['topic_name'], metric['topic_count'], metric['topic_average']])

    # Create radar chart and get it as a buffer
    if total_simulations == 0:
        # Subtítulo
        subtitle = Paragraph(
            "El vendedor no ha tomado simulaciones", heading_style)
        elements.append(subtitle)
    else:
        radar_chart_buffer = create_radar_chart(
            user_simulation_evaluation)

        # Subtítulo
        subtitle = Paragraph(
            f"Estadísticas de simulaciones ({total_simulations} hechos)", heading_style)
        elements.append(subtitle)

        # Insert radar chart image into the PDF
        radar_chart_img = Image(radar_chart_buffer)
        radar_chart_img.drawHeight = 3 * inch
        radar_chart_img.drawWidth = 3 * inch

        elements.append(radar_chart_img)
        elements.append(Spacer(1, 36))

    if total_workshops == 0:
        # Subtítulo
        subtitle = Paragraph(
            f"El vendedor no ha tomado talleres", heading_style)
        elements.append(subtitle)
    else:
        subtitle = Paragraph(
            f"Estadísticas de talleres ({total_workshops} hechos)", heading_style)
        elements.append(subtitle)

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)

    # intro_text = Paragraph(
    #    f"<strong>Número de simulaciones hechas:</strong> {total_simulations}.",
    #    normal_style
    # )
    # elements.append(intro_text)

    # Build PDF
    doc.build(elements)

    return response


def create_branch_report(branch_name, total_simulations, user_simulation_scores, total_workshops, user_workshop_evaluations):

    date = timezone.now().strftime('%d-%m-%Y')

    # Create a HttpResponse object with the correct PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f"attachment; filename=Reporte_{branch_name}_{date}.pdf;"

    # Create the PDF object using reportlab
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='Title',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.white,
        alignment=1,  # Center align
        spaceAfter=14,
        wordWrap='CJK'  # Ensure word wrapping
    )
    normal_style = styles['Normal']
    heading_style = ParagraphStyle(
        name='Heading', parent=styles['Heading1'], alignment=1, spaceAfter=14, fontSize=14)
    right_aligned_style = ParagraphStyle(
        name='RightAligned', parent=styles['Normal'], alignment=2, spaceAfter=14)

    info = [
        [Paragraph(
            f'Evaluación general para los vendedores de la sucursal de {branch_name} en los últimos 31 días', title_style), ''],
        ['Fecha de expedición del reporte', f'{date}']
    ]

    # Añadir columnas de padding
    info_table = Table(info, colWidths=[240, 240])
    info_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),  # Span the title across the inner columns
        # Center all cells horizontally
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        # Center the title cell vertically
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        # Larger font size for the title
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        # Background color for the title
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        # Text color for the title
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        # Top padding for the title row
        ('TOPPADDING', (0, 0), (-1, -1), 12),  # Top padding for all rows
        # Bottom padding for all rows
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        # Background color for other rows
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        # Text color for other rows
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 12),  # Font size for other rows
        ('LEFTPADDING', (0, 0), (-1, -1), 12),  # Left padding for all rows
        # Right padding for all rows
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('WORDWRAP', (0, 0), (1, 0), 'CJK')  # Border around the table
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))  # Additional spacer after the table

    if total_simulations == 0:
        # Subtítulo
        subtitle = Paragraph(
            "Los vendedores no han hecho simulaciones en los últimos 31 días", heading_style)
        elements.append(subtitle)
    else:

        # Subtítulo
        subtitle = Paragraph(
            f"Estadísticas de simulaciones ({total_simulations} hechos)", heading_style)
        elements.append(subtitle)

        radar_chart_buffer = create_radar_chart(user_simulation_scores)

        radar_chart_img = Image(radar_chart_buffer)
        radar_chart_img.drawHeight = 3 * inch
        radar_chart_img.drawWidth = 3 * inch

        elements.append(radar_chart_img)
        elements.append(Spacer(1, 36))

    # Add data table
    data = [["Tema", "Veces que se tomó", "Promedio"]]  # Header
    for metric in user_workshop_evaluations:
        data.append(
            [metric['topic_name'], metric['topic_count'], metric['topic_average']])

    if total_workshops == 0:
        # Subtítulo
        subtitle = Paragraph(
            f"Los vendedores no han tomado talleres en los últimos 31 días", heading_style)
        elements.append(subtitle)
    else:
        subtitle = Paragraph(
            f"Estadísticas de talleres ({total_workshops} hechos)", heading_style)
        elements.append(subtitle)

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)

    # Build PDF
    doc.build(elements)

    return response
