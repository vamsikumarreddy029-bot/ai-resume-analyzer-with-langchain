def json_to_text(data):
    text = f"Name: {data.get('name','')}\n\n"

    text += "Skills:\n"
    for s in data.get("skills", []):
        text += f"- {s}\n"

    text += "\nProjects:\n"
    for p in data.get("projects", []):
        text += f"- {p}\n"

    text += "\nExperience:\n"
    for e in data.get("experience", []):
        text += f"- {e}\n"

    text += "\nEducation:\n"
    for ed in data.get("education", []):
        text += f"- {ed}\n"

    return text