from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import black, grey

def generate_resume_pdf(filename, name, content):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    story = []

    name_style = ParagraphStyle(
        "Name",
        fontSize=20,
        leading=24,
        fontName="Helvetica-Bold",
        textColor=black,
        spaceAfter=18
    )

    heading_style = ParagraphStyle(
        "Heading",
        fontSize=12,
        leading=14,
        fontName="Helvetica-Bold",
        textColor=black,
        spaceBefore=14,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "Body",
        fontSize=10,
        leading=14,
        textColor=grey,
        spaceAfter=6
    )

    story.append(Paragraph(name, name_style))
    story.append(Spacer(1, 0.2 * inch))

    for line in content.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.isupper():
            story.append(Paragraph(line, heading_style))
        else:
            story.append(Paragraph(line, body_style))

    doc.build(story)
