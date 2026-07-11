from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from datetime import datetime
import os

def generate_pdf_report(
        filename,
        prediction,
        risk_score,
        risk_level,
        loc,
        complexity,
        mi=None):

    os.makedirs("reports", exist_ok=True)

    pdf_path = "reports/IntelliCode_Report.pdf"

    doc = SimpleDocTemplate(
        pdf_path,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.alignment = TA_CENTER

    heading = styles["Heading2"]
    normal = styles["BodyText"]

    story = []

    # =====================================================
    # TITLE
    # =====================================================

    story.append(Paragraph(
        "<font size=22><b>IntelliCode</b></font>",
        title))

    story.append(Paragraph(
        "<b>AI-Powered Software Defect Prediction Report</b>",
        styles["Heading3"]))

    story.append(Spacer(1, 20))

    # =====================================================
    # REPORT INFO
    # =====================================================

    story.append(Paragraph("<b>REPORT INFORMATION</b>", heading))

    info = [
        ["Generated On", datetime.now().strftime("%d-%m-%Y %H:%M:%S")],
        ["File Name", filename],
        ["Analysis Type", "Python Static Analysis"],
        ["Prediction Engine", "Random Forest"],
        ["Status", "Analysis Completed"]
    ]

    table = Table(info, colWidths=[170, 300])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#E3F2FD")),
        ("GRID",(0,0),(-1,-1),1,colors.grey),
        ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#F5F5F5")),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica"),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))

    story.append(table)

    story.append(Spacer(1,18))

    # =====================================================
    # PREDICTION SUMMARY
    # =====================================================

    story.append(Paragraph("<b>PREDICTION SUMMARY</b>", heading))

    summary = [
        ["Prediction", prediction],
        ["Risk Score", f"{risk_score}%"],
        ["Risk Level", risk_level]
    ]

    table = Table(summary, colWidths=[170,300])

    table.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),1,colors.grey),
        ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#F5F5F5")),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))

    story.append(table)

    story.append(Spacer(1,18))

    # =====================================================
    # METRICS
    # =====================================================

    story.append(Paragraph("<b>SOFTWARE METRICS</b>", heading))

    metrics = [
        ["Lines of Code (LOC)", str(loc)],
        ["Cyclomatic Complexity", str(complexity)],
        ["Maintainability Index", str(mi)]
    ]

    table = Table(metrics, colWidths=[220,250])

    table.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),1,colors.grey),
        ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#F5F5F5")),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))

    story.append(table)

    story.append(Spacer(1,18))

    # =====================================================
    # AI ASSESSMENT
    # =====================================================

    story.append(Paragraph("<b>AI ASSESSMENT</b>", heading))

    if risk_score >= 70:

        assessment = """
        The uploaded module exhibits high software complexity and is likely to contain defects.
        Immediate code review, refactoring, and additional testing are strongly recommended
        before deployment.
        """

    elif risk_score >= 40:

        assessment = """
        The uploaded module shows moderate software risk indicators.
        Targeted testing and focused code review are recommended to improve reliability.
        """

    else:

        assessment = """
        The uploaded module appears stable with a relatively low probability of defects.
        Standard software testing practices should be sufficient.
        """

    story.append(Paragraph(assessment, normal))

    story.append(Spacer(1,18))

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    story.append(Paragraph("<b>RECOMMENDED ACTIONS</b>", heading))

    recommendations = [
        "• Perform detailed code review",
        "• Increase unit test coverage",
        "• Reduce cyclomatic complexity",
        "• Conduct static code analysis",
        "• Execute regression testing",
        "• Monitor maintainability metrics"
    ]

    for item in recommendations:
        story.append(Paragraph(item, normal))

    story.append(Spacer(1,20))

    # =====================================================
    # FOOTER
    # =====================================================

    story.append(Paragraph(
        "<b>Generated by IntelliCode</b>",
        styles["Heading3"]))

    story.append(Paragraph(
        "AI-Powered Software Quality Assurance Platform", "© 2026 IntelliCode",
        normal))

    story.append(Paragraph(
        "© 2026 IntelliCode",
        normal))

    doc.build(story)

    return pdf_path