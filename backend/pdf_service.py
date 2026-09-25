from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def create_hr_pdf(form_data, output_path):
    pdf = canvas.Canvas(output_path, pagesize=A4)

    width, height = A4
    y = height - 50

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "HireFlow AI - Candidate Evaluation")

    y -= 40

    pdf.setFont("Helvetica", 11)

    pdf.drawString(50, y, f"Candidate: {form_data.get('candidate_name', '')}")
    y -= 20

    pdf.drawString(50, y, f"Email: {form_data.get('email', '')}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Education")
    y -= 20

    pdf.setFont("Helvetica", 10)

    for item in form_data.get("education", []):
        pdf.drawString(60, y, str(item))
        y -= 15

    y -= 15

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Experience")
    y -= 20

    pdf.setFont("Helvetica", 10)

    for item in form_data.get("experience", []):
        pdf.drawString(60, y, str(item))
        y -= 15

    y -= 15

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Technical Skills")
    y -= 20

    pdf.setFont("Helvetica", 10)
    pdf.drawString(60, y, ", ".join(form_data.get("skills", [])))
    y -= 30

    evaluation = form_data.get("ai_evaluation", {})

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "AI Evaluation")
    y -= 20

    pdf.setFont("Helvetica", 10)

    summary = evaluation.get("overall_summary", "")

    # Keep the PDF simple and readable
    for line in [summary]:
        pdf.drawString(60, y, line[:110])
        y -= 15

    pdf.save()