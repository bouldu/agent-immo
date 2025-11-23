"""PDF generation utilities using ReportLab."""

import os
from typing import Any

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def generate_pdf_report(indicators: dict[str, Any], images: dict[str, Any]) -> str:
    """
    Generate a PDF report from indicators and images.

    Args:
        indicators: Dictionary containing analysis indicators
        images: Dictionary containing visualization images

    Returns:
        Path to the generated PDF file
    """
    # Create output directory if it doesn't exist
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)

    # Generate PDF filename
    pdf_path = os.path.join(output_dir, "rapport_analyse.pdf")

    # Create PDF document
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph("Rapport d'Analyse Immobilière", styles["Title"])
    story.append(title)
    story.append(Spacer(1, 0.2 * inch))

    # Introduction
    intro = Paragraph(
        "Ce rapport présente l'analyse de pertinence d'un emplacement pour un projet immobilier.",
        styles["Normal"],
    )
    story.append(intro)
    story.append(Spacer(1, 0.2 * inch))

    # Indicators section
    story.append(Paragraph("Indicateurs", styles["Heading1"]))
    story.append(Spacer(1, 0.1 * inch))

    # TODO: Add actual indicator data to PDF
    if indicators:
        for key, value in indicators.items():
            if value is not None:
                text = f"<b>{key}:</b> {value}"
                story.append(Paragraph(text, styles["Normal"]))
                story.append(Spacer(1, 0.05 * inch))

    # Images section
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Visualisations", styles["Heading1"]))
    story.append(Spacer(1, 0.1 * inch))

    # TODO: Add actual images to PDF
    # For now, just add placeholder text
    story.append(
        Paragraph("Les visualisations seront ajoutées dans une version future.", styles["Normal"])
    )

    # Build PDF
    doc.build(story)

    return pdf_path






