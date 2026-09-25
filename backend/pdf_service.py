from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def create_hr_pdf(form_data, output_path):

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()

    # ---------- HIREFLOW COLORS ----------

    AMBER = colors.HexColor("#E9A642")
    LIGHT_AMBER = colors.HexColor("#FFF7E6")
    DARK_TEXT = colors.HexColor("#25272B")
    SECONDARY_TEXT = colors.HexColor("#6B7280")
    LIGHT_BACKGROUND = colors.HexColor("#F8F7F3")
    BORDER = colors.HexColor("#D9D9D9")
    WHITE = colors.white

    # ---------- STYLES ----------

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        textColor=DARK_TEXT,
        spaceAfter=5,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=SECONDARY_TEXT,
        spaceAfter=18,
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=AMBER,
        spaceBefore=12,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=DARK_TEXT,
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=SECONDARY_TEXT,
    )

    bullet_style = ParagraphStyle(
        "Bullet",
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=5,
    )

    skill_style = ParagraphStyle(
        "Skill",
        parent=body_style,
        fontSize=8.5,
        alignment=TA_CENTER,
        textColor=DARK_TEXT,
    )

    # ---------- HELPERS ----------

    def make_bullets(items):
        result = []

        for item in items:
            result.append(
                Paragraph(
                    f"• {str(item)}",
                    bullet_style,
                )
            )

        return result

    def make_skill_chips(skills):

        if not skills:
            return Paragraph(
                "Not provided",
                body_style,
            )

        # Put skills into rows of 4
        rows = []
        current_row = []

        for skill in skills:
            current_row.append(
                Paragraph(
                    str(skill),
                    skill_style,
                )
            )

            if len(current_row) == 4:
                rows.append(current_row)
                current_row = []

        if current_row:
            while len(current_row) < 4:
                current_row.append("")

            rows.append(current_row)

        table = Table(
            rows,
            colWidths=[
                43.5 * mm,
                43.5 * mm,
                43.5 * mm,
                43.5 * mm,
            ],
            hAlign="LEFT",
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        LIGHT_AMBER,
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor("#E7C98D"),
                    ),
                    (
                        "INNERGRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        WHITE,
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        return table

    # ---------- DATA ----------

    candidate_name = form_data.get(
        "candidate_name",
        "Not provided",
    )

    email = form_data.get(
        "email",
        "Not provided",
    )

    phone = form_data.get(
        "phone",
        "Not provided",
    )

    education = form_data.get(
        "education",
        [],
    )

    experience = form_data.get(
        "experience",
        [],
    )

    skills = form_data.get(
        "skills",
        [],
    )

    projects = form_data.get(
        "projects",
        [],
    )

    certifications = form_data.get(
        "certifications",
        [],
    )

    evaluation = form_data.get(
        "ai_evaluation",
        {},
    )

    if not isinstance(evaluation, dict):
        evaluation = {}

    experience_summary = evaluation.get(
        "experience_summary",
        "Not available",
    )

    strengths = evaluation.get(
        "strengths",
        [],
    )

    missing_information = evaluation.get(
        "missing_information",
        [],
    )

    overall_summary = evaluation.get(
        "overall_summary",
        "Not available",
    )

    # ---------- DOCUMENT ----------

    story = []

    # ---------- TOP ACCENT LINE ----------

    accent_line = Table(
        [[""]],
        colWidths=[174 * mm],
        rowHeights=[3 * mm],
    )

    accent_line.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    AMBER,
                ),
            ]
        )
    )

    story.append(accent_line)
    story.append(Spacer(1, 12))

    # ---------- HEADER ----------

    story.append(
        Paragraph(
            "HIREFLOW",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "CANDIDATE EVALUATION REPORT",
            subtitle_style,
        )
    )

    # ---------- CANDIDATE PROFILE ----------

    profile_data = [
        [
            Paragraph(
                "<b>Candidate</b><br/>"
                + str(candidate_name),
                body_style,
            ),
            Paragraph(
                "<b>Email</b><br/>"
                + str(email),
                body_style,
            ),
            Paragraph(
                "<b>Phone</b><br/>"
                + str(phone),
                body_style,
            ),
        ]
    ]

    profile_table = Table(
        profile_data,
        colWidths=[
            58 * mm,
            58 * mm,
            58 * mm,
        ],
    )

    profile_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    LIGHT_BACKGROUND,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    BORDER,
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    BORDER,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
            ]
        )
    )

    story.append(profile_table)

    # ---------- EDUCATION ----------

    story.append(
        Paragraph(
            "EDUCATION",
            section_style,
        )
    )

    if education:
        story.extend(
            make_bullets(education)
        )
    else:
        story.append(
            Paragraph(
                "Not provided",
                body_style,
            )
        )

    # ---------- EXPERIENCE ----------

    story.append(
        Paragraph(
            "EXPERIENCE",
            section_style,
        )
    )

    if experience:

        for exp in experience:

            # Structured experience returned by Gemini
            if isinstance(exp, dict):

                role = exp.get(
                    "role",
                    "",
                )

                company = exp.get(
                    "company",
                    "",
                )

                duration = exp.get(
                    "duration",
                    "",
                )

                responsibilities = exp.get(
                    "responsibilities",
                    [],
                )

                # Role + company
                if role or company:
                    story.append(
                        Paragraph(
                            f"<b>{role} — {company}</b>",
                            body_style,
                        )
                    )

                # Duration
                if duration:
                    story.append(
                        Paragraph(
                            f"<i>{duration}</i>",
                            small_style,
                        )
                    )

                # Responsibilities
                if responsibilities:
                    story.extend(
                        make_bullets(
                            responsibilities
                        )
                    )

                story.append(
                    Spacer(1, 6)
                )

            # Fallback if experience is returned as a string
            else:
                story.append(
                    Paragraph(
                        f"• {str(exp)}",
                        bullet_style,
                    )
                )

    else:
        story.append(
            Paragraph(
                "Not provided",
                body_style,
            )
        )

    # ---------- TECHNICAL SKILLS ----------

    story.append(
        Paragraph(
            "TECHNICAL SKILLS",
            section_style,
        )
    )

    story.append(
        make_skill_chips(skills)
    )

    # ---------- PROJECTS ----------

    story.append(
        Paragraph(
            "PROJECTS",
            section_style,
        )
    )

    if projects:

        for project in projects:

            # Structured project returned by Gemini
            if isinstance(project, dict):

                project_name = project.get(
                    "name",
                    "",
                )

                description = project.get(
                    "description",
                    "",
                )

                details = project.get(
                    "details",
                    [],
                )

                # Project name
                if project_name:
                    story.append(
                        Paragraph(
                            f"<b>{project_name}</b>",
                            body_style,
                        )
                    )

                # Project description
                if description:
                    story.append(
                        Paragraph(
                            description,
                            body_style,
                        )
                    )

                # Project details
                if details:
                    story.extend(
                        make_bullets(details)
                    )

                story.append(
                    Spacer(1, 6)
                )

            # Fallback if project is returned as a string
            else:
                story.append(
                    Paragraph(
                        f"• {str(project)}",
                        bullet_style,
                    )
                )

    else:
        story.append(
            Paragraph(
                "Not provided",
                body_style,
            )
        )

    # ---------- CERTIFICATIONS ----------

    story.append(
        Paragraph(
            "CERTIFICATIONS",
            section_style,
        )
    )

    if certifications:
        story.extend(
            make_bullets(certifications)
        )
    else:
        story.append(
            Paragraph(
                "No certifications listed in the resume.",
                body_style,
            )
        )

    story.append(
        Spacer(1, 8)
    )

    # ---------- AI EVALUATION HEADER ----------

    evaluation_header = Table(
        [
            [
                Paragraph(
                    "AI EVALUATION",
                    ParagraphStyle(
                        "EvaluationHeader",
                        parent=section_style,
                        textColor=WHITE,
                        fontSize=11,
                        spaceBefore=0,
                        spaceAfter=0,
                    ),
                )
            ]
        ],
        colWidths=[174 * mm],
    )

    evaluation_header.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    AMBER,
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(
        evaluation_header
    )

    story.append(
        Spacer(1, 10)
    )

    # ---------- EXPERIENCE SUMMARY ----------

    story.append(
        Paragraph(
            "<b>Experience Summary</b>",
            body_style,
        )
    )

    story.append(
        Paragraph(
            str(experience_summary),
            body_style,
        )
    )

    story.append(
        Spacer(1, 10)
    )

    # ---------- STRENGTHS ----------

    story.append(
        Paragraph(
            "<b>Strengths</b>",
            body_style,
        )
    )

    if strengths:
        story.extend(
            make_bullets(strengths)
        )
    else:
        story.append(
            Paragraph(
                "No strengths identified.",
                body_style,
            )
        )

    story.append(
        Spacer(1, 5)
    )

    # ---------- MISSING INFORMATION ----------

    story.append(
        Paragraph(
            "<b>Missing Information</b>",
            body_style,
        )
    )

    if missing_information:
        story.extend(
            make_bullets(
                missing_information
            )
        )
    else:
        story.append(
            Paragraph(
                "No missing information identified.",
                body_style,
            )
        )

    story.append(
        Spacer(1, 10)
    )

    # ---------- OVERALL SUMMARY ----------

    summary_table = Table(
        [
            [
                Paragraph(
                    "<b>Overall Summary</b><br/><br/>"
                    + str(overall_summary),
                    body_style,
                )
            ]
        ],
        colWidths=[174 * mm],
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    LIGHT_BACKGROUND,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    BORDER,
                ),
                (
                    "LINEBEFORE",
                    (0, 0),
                    (0, 0),
                    4,
                    AMBER,
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
            ]
        )
    )

    story.append(
        summary_table
    )

    story.append(
        Spacer(1, 18)
    )

    # ---------- FOOTER ----------

    story.append(
        Paragraph(
            "Generated by HireFlow • AI-generated from the submitted resume",
            small_style,
        )
    )

    # ---------- BUILD ----------

    doc.build(story)