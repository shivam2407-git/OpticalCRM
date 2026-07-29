from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(data):

    filename = f"{data[1]}_prescription.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph("GOSWAMI OPTICAL", styles["Title"])
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(f"Customer Name: {data[1]}", styles["Normal"])
    )

    content.append(
        Paragraph(f"Mobile: {data[2]}", styles["Normal"])
    )

    content.append(
        Paragraph(f"Date Of Birth: {data[5]}", styles["Normal"])
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph("<b>RIGHT EYE</b>", styles["Heading2"])
    )

    content.append(
        Paragraph(f"SPH: {data[6]}", styles["Normal"])
    )

    content.append(
        Paragraph(f"CYL: {data[7]}", styles["Normal"])
    )

    content.append(
        Paragraph(f"AXIS: {data[8]}", styles["Normal"])
    )

    content.append(Spacer(1, 10))

    content.append(
        Paragraph("<b>LEFT EYE</b>", styles["Heading2"])
    )

    content.append(
        Paragraph(f"SPH: {data[9]}", styles["Normal"])
    )

    content.append(
        Paragraph(f"CYL: {data[10]}", styles["Normal"])
    )

    content.append(
        Paragraph(f"AXIS: {data[11]}", styles["Normal"])
    )

    content.append(Spacer(1, 10))

    content.append(
        Paragraph(f"PD: {data[12]}", styles["Normal"])
    )

    content.append(
        Paragraph(f"Notes: {data[13]}", styles["Normal"])
    )

    doc.build(content)

    return filename