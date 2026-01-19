from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import black, grey
from reportlab.lib.units import inch

def generate_resume_pdf(filename, data):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=30,
        bottomMargin=30
    )

    story = []

    # ---------- STYLES ----------
    name_style = ParagraphStyle(
        "Name", fontSize=22, fontName="Helvetica-Bold", spaceAfter=4
    )
    role_style = ParagraphStyle(
        "Role", fontSize=11, textColor=grey, spaceAfter=6
    )
    contact_style = ParagraphStyle(
        "Contact", fontSize=9, textColor=grey, spaceAfter=10
    )

    header_style = ParagraphStyle(
        "Header", fontSize=11, fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=4
    )

    body_style = ParagraphStyle(
        "Body", fontSize=10, leading=14, spaceAfter=4
    )

    # ---------- HEADER ----------
    story.append(Paragraph(data["name"], name_style))
    story.append(Paragraph(data["role"], role_style))
    story.append(Paragraph(data["contact"], contact_style))
    story.append(Spacer(1, 6))

    # ---------- SUMMARY ----------
    story.append(Paragraph("SUMMARY", header_style))
    story.append(Paragraph(data["summary"], body_style))

    # ---------- SKILLS (2 COLUMNS) ----------
    story.append(Paragraph("SKILLS", header_style))

    skills_table = Table(
        [[Paragraph(s, body_style)] for s in data["skills"]],
        colWidths=[6.5 * inch]
    )
    story.append(skills_table)

    # ---------- PROJECTS ----------
    story.append(Paragraph("PROJECTS", header_style))
    for p in data["projects"]:
        row = Table(
            [[
                Paragraph(p["title"], body_style),
                Paragraph(p["date"], body_style)
            ]],
            colWidths=[4.8 * inch, 1.7 * inch]
        )
        story.append(row)

        for b in p["bullets"]:
            story.append(Paragraph(f"• {b}", body_style))

    # ---------- EDUCATION ----------
    story.append(Paragraph("EDUCATION", header_style))
    edu = Table(
        [[
            Paragraph(data["education"]["degree"], body_style),
            Paragraph(data["education"]["year"], body_style)
        ]],
        colWidths=[4.8 * inch, 1.7 * inch]
    )
    story.append(edu)

    # ---------- CERTIFICATIONS ----------
    if data["certifications"]:
        story.append(Paragraph("CERTIFICATIONS", header_style))
        for c in data["certifications"]:
            story.append(Paragraph(f"{c}", body_style))

    doc.build(story)
