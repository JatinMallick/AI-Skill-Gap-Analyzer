import re
from typing import Dict, Iterable, List


def load_skills(file_path):
    with open(file_path, "r") as f:
        skills = [line.strip().lower() for line in f]
    return skills


def extract_skills(text, skills_list):
    """
    Extract skills from resume text using a curated dictionary.

    Notes:
    - This is dictionary-based: if a skill is not present in `skills_list`,
      it will not be extracted. Add new skills to `data/skills.txt`.
    - Matching is robust to punctuation/spacing variants (best-effort).
    """
    if not text:
        return []

    normalized_text = _normalize_text(text)
    aliases = _aliases()

    found = set()
    for raw_skill in skills_list or []:
        skill = (raw_skill or "").strip().lower()
        if not skill:
            continue

        canonical = aliases.get(skill, skill)
        if _skill_in_text(normalized_text, canonical):
            found.add(canonical)
            continue

        # Try alias variants too (e.g., "powerbi" -> "power bi")
        for variant, canon in aliases.items():
            if canon == canonical and _skill_in_text(normalized_text, variant):
                found.add(canonical)
                break

    return sorted(found)


def _normalize_text(s: str) -> str:
    s = s.lower()
    # Keep letters/numbers and a few skill-relevant symbols; normalize the rest.
    s = re.sub(r"[^\w\s+.#/\-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _aliases() -> Dict[str, str]:
    # Both keys and values should be normalized (lowercase).
    return {
        "node": "node.js",
        "nodejs": "node.js",
        "reactjs": "react",
        "nextjs": "next.js",
        "postgres": "postgresql",
        "postgre": "postgresql",
        "powerbi": "power bi",
        "ci cd": "ci/cd",
        "cicd": "ci/cd",
        "k8s": "kubernetes",
        ".net": "dotnet",
        "dot net": "dotnet",
        "ml ops": "mlops",
    }


def _skill_in_text(normalized_text: str, skill: str) -> bool:
    skill = _normalize_text(skill)
    if not skill:
        return False

    # Multi-word skills: allow flexible whitespace between words
    if " " in skill:
        parts = [re.escape(p) for p in skill.split(" ") if p]
        if not parts:
            return False
        pattern = r"(?:^|\s)" + r"\s+".join(parts) + r"(?:\s|$)"
        return re.search(pattern, normalized_text) is not None

    # Single token: require token boundaries (avoid "sql" matching "sequel")
    pattern = r"(?:^|\s)" + re.escape(skill) + r"(?:\s|$)"
    if re.search(pattern, normalized_text) is not None:
        return True

    # Handle tokens that commonly appear with separators (next.js, node.js, ci/cd)
    if any(ch in skill for ch in ".-/+#"):
        compact_text = normalized_text.replace(" ", "")
        compact_skill = skill.replace(" ", "")
        return compact_skill in compact_text

    return False


if __name__ == "__main__":

    from resume_parser import extract_resume_text

    text = extract_resume_text(r"C:\Users\jatin\Desktop\skill_gap_analyzer\data\Resume final.pdf")

    skills = load_skills(r"C:\Users\jatin\Desktop\skill_gap_analyzer\data\skills.txt")

    extracted = extract_skills(text, skills)

    print("Extracted Skills:")
    print(extracted)