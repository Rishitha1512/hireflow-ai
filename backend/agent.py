def create_hr_form(candidate, evaluation):
    return {
        "candidate_name": candidate.get("name", ""),
        "email": candidate.get("email", ""),
        "education": candidate.get("education", []),
        "experience": candidate.get("experience", []),
        "skills": candidate.get("skills", []),
        "projects": candidate.get("projects", []),
        "certifications": candidate.get("certifications", []),
        "ai_evaluation": evaluation
    }