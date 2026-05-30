"""
Skill name normalizer.

Maps raw text (course titles, descriptions) to canonical skill names
used across Kaix's knowledge base.
"""

import re

# Canonical skill name → patterns to match (case-insensitive)
SKILL_PATTERNS: dict[str, list[str]] = {
    # Backend
    "Python": [r"\bpython\b", r"\bpemrograman python\b"],
    "FastAPI": [r"\bfastapi\b", r"\bfast api\b"],
    "Django": [r"\bdjango\b"],
    "Flask": [r"\bflask\b"],
    "Node.js": [r"\bnode\.?js\b", r"\bnodejs\b"],
    "Express": [r"\bexpress\.?js\b", r"\bexpress\b"],
    "PostgreSQL": [r"\bpostgres(?:ql)?\b", r"\bpgsql\b"],
    "MySQL": [r"\bmysql\b"],
    "MongoDB": [r"\bmongo(?:db)?\b"],
    "Redis": [r"\bredis\b"],
    "REST API": [r"\brest\s*api\b", r"\brestful\b", r"\bback-?end\b"],
    "GraphQL": [r"\bgraphql\b"],
    "SQL": [r"\bsql\b", r"\bdatabase\b", r"\bbasis data\b"],
    "System Design": [r"\bsystem design\b", r"\barsitektur\b", r"\bscalability\b"],

    # Frontend
    "JavaScript": [r"\bjavascript\b", r"\bjs\b"],
    "TypeScript": [r"\btypescript\b", r"\bts\b"],
    "React": [r"\breact(?:\.?js)?\b"],
    "Vue.js": [r"\bvue(?:\.?js)?\b"],
    "Next.js": [r"\bnext\.?js\b"],
    "HTML/CSS": [r"\bhtml\b", r"\bcss\b", r"\bweb dasar\b"],
    "Tailwind": [r"\btailwind\b"],
    "Angular": [r"\bangular\b"],

    # Mobile
    "Android": [r"\bandroid\b"],
    "Kotlin": [r"\bkotlin\b"],
    "Flutter": [r"\bflutter\b"],
    "Dart": [r"\bdart\b"],
    "Swift": [r"\bswift\b"],

    # DevOps
    "Docker": [r"\bdocker\b", r"\bcontainer\b"],
    "Kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
    "AWS": [r"\baws\b", r"\bamazon web services\b"],
    "Google Cloud": [r"\bgcp\b", r"\bgoogle cloud\b"],
    "Azure": [r"\bazure\b"],
    "Terraform": [r"\bterraform\b"],
    "CI/CD": [r"\bci/?cd\b", r"\bcontinuous integration\b", r"\bgithub actions\b"],
    "Linux": [r"\blinux\b", r"\bubuntu\b", r"\bdebian\b"],
    "Nginx": [r"\bnginx\b"],
    "Git": [r"\bgit(?:hub|lab)?\b", r"\bversion control\b"],

    # ML/AI
    "TensorFlow": [r"\btensorflow\b", r"\btf\b"],
    "PyTorch": [r"\bpytorch\b"],
    "Scikit-learn": [r"\bscikit[\s-]?learn\b", r"\bsklearn\b"],
    "Pandas": [r"\bpandas\b"],
    "NumPy": [r"\bnumpy\b"],
    "Machine Learning": [r"\bmachine learning\b", r"\bml\b", r"\bpembelajaran mesin\b"],
    "Deep Learning": [r"\bdeep learning\b"],
    "NLP": [r"\bnlp\b", r"\bnatural language processing\b"],
    "Computer Vision": [r"\bcomputer vision\b", r"\bimage classification\b", r"\bobject detection\b"],
    "LangChain": [r"\blangchain\b", r"\bllm\b"],

    # Data
    "Power BI": [r"\bpower bi\b"],
    "Tableau": [r"\btableau\b"],
    "Excel": [r"\bexcel\b"],
    "Data Visualization": [r"\bdata vis(?:uali[sz]ation)?\b", r"\bvisualisasi data\b"],

    # Design
    "Figma": [r"\bfigma\b"],
    "UI/UX": [r"\bui/?ux\b", r"\buser interface\b", r"\buser experience\b"],
    "Design System": [r"\bdesign system\b", r"\bdesign token\b"],

    # Marketing
    "Google Analytics": [r"\bgoogle analytics\b", r"\bga4\b"],
    "SEO": [r"\bseo\b", r"\bsearch engine\b"],
    "Meta Ads": [r"\bmeta ads\b", r"\bfacebook ads\b", r"\biklan facebook\b"],
    "Google Ads": [r"\bgoogle ads\b", r"\badwords\b"],
    "Content Marketing": [r"\bcontent marketing\b", r"\bcopywriting\b"],

    # Security
    "Penetration Testing": [r"\bpenetration testing\b", r"\bethical hacking\b", r"\bpentest\b"],
    "OWASP": [r"\bowasp\b"],
    "Network Security": [r"\bnetwork security\b", r"\bfirewall\b", r"\bids\b"],
    "Cryptography": [r"\bcryptography\b", r"\benkripsi\b"],
}

# Pre-compile patterns for performance
_COMPILED_PATTERNS: dict[str, list[re.Pattern]] = {
    skill: [re.compile(p, re.IGNORECASE) for p in patterns]
    for skill, patterns in SKILL_PATTERNS.items()
}


def infer_skills_from_text(text: str) -> list[str]:
    """
    Extract canonical skill names from free text (title, description, etc.).

    Returns deduplicated list of matched canonical skill names.
    """
    if not text:
        return []

    matched = []
    for skill, patterns in _COMPILED_PATTERNS.items():
        for pattern in patterns:
            if pattern.search(text):
                matched.append(skill)
                break  # one match per skill is enough

    return matched


def normalize_skills_list(raw_skills: list[str]) -> list[str]:
    """
    Normalize a list of raw skill strings to canonical names.

    For each raw string, tries to match against known patterns.
    Returns deduplicated list.
    """
    if not raw_skills:
        return []

    canonical = set()
    for raw in raw_skills:
        found = infer_skills_from_text(raw)
        if found:
            canonical.update(found)
        else:
            # Keep the original if no match (might be valid but unlisted)
            canonical.add(raw.strip())

    return sorted(canonical)


def infer_level_from_text(text: str) -> str:
    """Infer course level from text."""
    text_lower = text.lower()
    if any(x in text_lower for x in ["dasar", "pemula", "beginner", "basic", "introduct", "pengantar", "fundamental"]):
        return "beginner"
    if any(x in text_lower for x in ["menengah", "intermediate", "lanjut"]):
        return "intermediate"
    if any(x in text_lower for x in ["mahir", "advanced", "expert", "profesional"]):
        return "advanced"
    return "beginner"  # default
