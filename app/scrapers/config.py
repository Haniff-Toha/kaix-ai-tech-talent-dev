"""
Scraper configuration — source mappings, search terms, and static data.

Contains:
    - Dicoding learning path → Kaix track mapping
    - YouTube search terms per skill
    - rubythalib.ai curated course data
    - Curated books and GitHub repos
    - Rate limiting and user agent config
"""

import random

# ──────────────────────────────────────────────
# Rate Limiting & HTTP Config
# ──────────────────────────────────────────────
RATE_LIMIT_DELAY_SECONDS = (1.0, 3.0)  # random delay between requests

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
]


def random_user_agent() -> str:
    return random.choice(USER_AGENTS)


# ──────────────────────────────────────────────
# Dicoding Learning Path → Kaix Track Mapping
# ──────────────────────────────────────────────
DICODING_LEARNING_PATHS = {
    65: {"name": "AI Engineer", "kaix_track": "ml_ai_engineer", "url": "https://www.dicoding.com/learningpaths/65"},
    68: {"name": "Gen AI Engineer", "kaix_track": "ml_ai_engineer", "url": "https://www.dicoding.com/learningpaths/68"},
    30: {"name": "MLOps Engineer", "kaix_track": "devops_engineer", "url": "https://www.dicoding.com/learningpaths/30"},
    60: {"name": "Data Scientist", "kaix_track": "data_analyst", "url": "https://www.dicoding.com/learningpaths/60"},
    22: {"name": "Front-End Web", "kaix_track": "frontend_engineer", "url": "https://www.dicoding.com/learningpaths/22"},
    58: {"name": "React", "kaix_track": "frontend_engineer", "url": "https://www.dicoding.com/learningpaths/58"},
    62: {"name": "Back-End Python", "kaix_track": "backend_engineer", "url": "https://www.dicoding.com/learningpaths/62"},
    41: {"name": "Back-End JavaScript", "kaix_track": "backend_engineer", "url": "https://www.dicoding.com/learningpaths/41"},
    53: {"name": "DevOps Engineer", "kaix_track": "devops_engineer", "url": "https://www.dicoding.com/learningpaths/53"},
    7:  {"name": "Android", "kaix_track": "frontend_engineer", "url": "https://www.dicoding.com/learningpaths/7"},
    21: {"name": "Multi-Platform App", "kaix_track": "frontend_engineer", "url": "https://www.dicoding.com/learningpaths/21"},
    52: {"name": "Google Cloud Professional", "kaix_track": "devops_engineer", "url": "https://www.dicoding.com/learningpaths/52"},
}

DICODING_CATALOG_URL = "https://www.dicoding.com/academies/list"


# ──────────────────────────────────────────────
# YouTube Search Terms per Skill
# ──────────────────────────────────────────────
YOUTUBE_SEARCH_TERMS = {
    # Backend
    "Python": ["python tutorial indonesia", "belajar python pemula", "CS50P"],
    "FastAPI": ["fastapi tutorial", "fastapi python indonesia"],
    "PostgreSQL": ["postgresql tutorial", "belajar sql indonesia"],
    "Django": ["django tutorial", "django indonesia"],
    "Docker": ["docker tutorial indonesia", "belajar docker"],
    "Kubernetes": ["kubernetes tutorial", "k8s untuk pemula"],
    "REST API": ["rest api tutorial", "belajar rest api"],
    "System Design": ["system design primer", "bytebytego", "system design indonesia"],
    "Git": ["git tutorial bahasa indonesia", "github tutorial pemula"],
    # Frontend
    "React": ["react tutorial indonesia", "belajar react js"],
    "Vue.js": ["vue js tutorial indonesia", "belajar vue"],
    "Next.js": ["nextjs tutorial", "next js indonesia"],
    "TypeScript": ["typescript tutorial", "belajar typescript"],
    "JavaScript": ["javascript tutorial indonesia", "belajar javascript pemula"],
    # DevOps
    "AWS": ["aws tutorial indonesia", "belajar aws"],
    "Terraform": ["terraform tutorial", "terraform indonesia"],
    "Linux": ["linux tutorial bahasa indonesia", "belajar linux"],
    # ML/AI
    "PyTorch": ["pytorch tutorial", "deep learning indonesia"],
    "Scikit-learn": ["machine learning indonesia", "scikit learn tutorial"],
    "Pandas": ["pandas tutorial indonesia", "belajar pandas python"],
    "LangChain": ["langchain tutorial", "build llm app python"],
    # Design
    "Figma": ["figma tutorial indonesia", "belajar figma pemula"],
    # Marketing
    "Google Analytics": ["google analytics indonesia", "belajar google analytics"],
    "SEO": ["seo tutorial indonesia", "belajar seo untuk pemula"],
    "Meta Ads": ["facebook ads indonesia", "iklan facebook untuk pemula"],
    # Security
    "Penetration Testing": ["ethical hacking indonesia", "belajar cyber security"],
    "OWASP": ["owasp top 10 tutorial", "web security indonesia"],
}

# Map skill → career tracks (for YouTube results tagging)
SKILL_TRACK_MAP = {
    "Python": ["backend_engineer", "data_analyst", "ml_ai_engineer"],
    "FastAPI": ["backend_engineer"],
    "PostgreSQL": ["backend_engineer", "data_analyst"],
    "Django": ["backend_engineer"],
    "Docker": ["backend_engineer", "devops_engineer"],
    "Kubernetes": ["devops_engineer"],
    "REST API": ["backend_engineer"],
    "System Design": ["backend_engineer", "devops_engineer"],
    "Git": ["backend_engineer", "frontend_engineer", "devops_engineer"],
    "React": ["frontend_engineer"],
    "Vue.js": ["frontend_engineer"],
    "Next.js": ["frontend_engineer"],
    "TypeScript": ["frontend_engineer", "backend_engineer"],
    "JavaScript": ["frontend_engineer", "backend_engineer"],
    "AWS": ["devops_engineer"],
    "Terraform": ["devops_engineer"],
    "Linux": ["devops_engineer", "backend_engineer"],
    "PyTorch": ["ml_ai_engineer"],
    "Scikit-learn": ["ml_ai_engineer", "data_analyst"],
    "Pandas": ["data_analyst", "ml_ai_engineer"],
    "LangChain": ["ml_ai_engineer", "backend_engineer"],
    "Figma": ["ui_ux_designer"],
    "Google Analytics": ["digital_marketer"],
    "SEO": ["digital_marketer"],
    "Meta Ads": ["digital_marketer"],
    "Penetration Testing": ["cybersecurity_analyst"],
    "OWASP": ["cybersecurity_analyst"],
}


# ──────────────────────────────────────────────
# rubythalib.ai — Manually Curated Courses
# ──────────────────────────────────────────────
RUBYTHALIB_CURATED_COURSES = [
    {
        "source": "rubythalib",
        "title": "Deep Learning Computer Vision dengan TensorFlow",
        "url": "https://academy.rubythalib.ai/",
        "instructor": "Ruby Abdullah",
        "platform_display": "rubythalib.ai Academy",
        "language": "id",
        "level": "intermediate",
        "is_free": False,
        "has_certificate": True,
        "skills_covered": ["TensorFlow", "Python", "Scikit-learn"],
        "career_tracks": ["ml_ai_engineer"],
        "is_indonesia_specific": True,
        "is_bahasa_indonesia": True,
        "description_short": (
            "Kelas praktis membangun model Deep Learning untuk Computer Vision "
            "menggunakan TensorFlow. Cocok untuk yang sudah memahami Python dan "
            "konsep dasar machine learning."
        ),
        "topics_covered": ["computer vision", "convolutional neural network", "tensorflow", "image classification"],
    },
    {
        "source": "rubythalib",
        "title": "NLP Deep Learning dengan TensorFlow",
        "url": "https://academy.rubythalib.ai/",
        "instructor": "Ruby Abdullah",
        "platform_display": "rubythalib.ai Academy",
        "language": "id",
        "level": "intermediate",
        "is_free": False,
        "has_certificate": True,
        "skills_covered": ["TensorFlow", "Python"],
        "career_tracks": ["ml_ai_engineer"],
        "is_indonesia_specific": True,
        "is_bahasa_indonesia": True,
        "description_short": (
            "Kelas NLP (Natural Language Processing) berbasis Deep Learning "
            "menggunakan TensorFlow. Mencakup text classification, sentiment analysis, "
            "dan sequence models."
        ),
        "topics_covered": ["nlp", "natural language processing", "text classification", "tensorflow", "lstm"],
    },
    {
        "source": "rubythalib",
        "title": "Object Detection dengan PyTorch",
        "url": "https://academy.rubythalib.ai/",
        "instructor": "Ruby Abdullah",
        "platform_display": "rubythalib.ai Academy",
        "language": "id",
        "level": "advanced",
        "is_free": False,
        "has_certificate": True,
        "skills_covered": ["PyTorch", "Python"],
        "career_tracks": ["ml_ai_engineer"],
        "is_indonesia_specific": True,
        "is_bahasa_indonesia": True,
        "description_short": (
            "Kelas lanjutan Computer Vision dengan PyTorch, fokus pada object detection. "
            "Membahas arsitektur YOLO, training custom dataset, dan deployment model."
        ),
        "topics_covered": ["object detection", "yolo", "pytorch", "computer vision", "custom dataset"],
    },
    {
        "source": "rubythalib",
        "title": "NLP Deep Learning dengan PyTorch",
        "url": "https://academy.rubythalib.ai/",
        "instructor": "Ruby Abdullah",
        "platform_display": "rubythalib.ai Academy",
        "language": "id",
        "level": "advanced",
        "is_free": False,
        "has_certificate": True,
        "skills_covered": ["PyTorch", "Python"],
        "career_tracks": ["ml_ai_engineer"],
        "is_indonesia_specific": True,
        "is_bahasa_indonesia": True,
        "description_short": (
            "Kelas NLP advanced menggunakan PyTorch. Membahas transformer architecture, "
            "attention mechanism, dan fine-tuning pre-trained language models."
        ),
        "topics_covered": ["nlp", "transformer", "attention", "pytorch", "bert", "fine-tuning"],
    },
    {
        "source": "rubythalib",
        "title": "Introduction to Machine Learning",
        "url": "https://goakal.com/rubythalib/course-intro-ml",
        "instructor": "Ruby Abdullah",
        "platform_display": "rubythalib.ai Academy",
        "language": "id",
        "level": "beginner",
        "is_free": True,
        "has_certificate": False,
        "skills_covered": ["Scikit-learn", "Python", "Pandas"],
        "career_tracks": ["ml_ai_engineer", "data_analyst"],
        "is_indonesia_specific": True,
        "is_bahasa_indonesia": True,
        "description_short": (
            "Kelas gratis pengantar Machine Learning dari dasar. "
            "Mencakup konsep ML, pemrosesan data, model prediksi, "
            "klasifikasi, dan pengelompokan data."
        ),
        "topics_covered": ["machine learning", "supervised learning", "classification", "clustering", "data processing"],
    },
    {
        "source": "rubythalib",
        "title": "Sistem Rekomendasi dengan AI",
        "url": "https://academy.rubythalib.ai/",
        "instructor": "Ruby Abdullah",
        "platform_display": "rubythalib.ai Academy",
        "language": "id",
        "level": "intermediate",
        "is_free": False,
        "has_certificate": True,
        "skills_covered": ["Python", "Scikit-learn", "TensorFlow"],
        "career_tracks": ["ml_ai_engineer", "data_analyst"],
        "is_indonesia_specific": True,
        "is_bahasa_indonesia": True,
        "description_short": (
            "Kelas praktis membangun sistem rekomendasi menggunakan berbagai "
            "pendekatan: collaborative filtering, content-based filtering, "
            "dan hybrid methods."
        ),
        "topics_covered": ["recommendation system", "collaborative filtering", "content-based filtering", "matrix factorization"],
    },
    {
        "source": "rubythalib",
        "title": "Face Recognition App - Fullstack AI",
        "url": "https://academy.rubythalib.ai/",
        "instructor": "Ruby Abdullah",
        "platform_display": "rubythalib.ai Academy",
        "language": "id",
        "level": "advanced",
        "is_free": False,
        "has_certificate": True,
        "skills_covered": ["Python", "PyTorch", "FastAPI"],
        "career_tracks": ["ml_ai_engineer"],
        "is_indonesia_specific": True,
        "is_bahasa_indonesia": True,
        "description_short": (
            "Kelas end-to-end membangun aplikasi Face Recognition fullstack. "
            "Mencakup model training, REST API backend dengan FastAPI, "
            "dan deployment ke production."
        ),
        "topics_covered": ["face recognition", "computer vision", "fastapi", "deployment", "fullstack ai"],
    },
]


# ──────────────────────────────────────────────
# Curated Books (static — not scraped)
# ──────────────────────────────────────────────
CURATED_BOOKS = [
    {
        "source": "book",
        "title": "Designing Data-Intensive Applications",
        "instructor": "Martin Kleppmann",
        "platform_display": "Book",
        "language": "en",
        "level": "advanced",
        "is_free": False,
        "has_certificate": False,
        "skills_covered": ["System Design", "PostgreSQL"],
        "career_tracks": ["backend_engineer", "devops_engineer", "data_analyst"],
        "is_indonesia_specific": False,
        "is_bahasa_indonesia": False,
        "description_short": (
            "The definitive book on distributed systems and data architecture. "
            "Covers databases, replication, consistency, stream processing. "
            "Essential reading for anyone targeting senior backend or data engineering roles."
        ),
        "topics_covered": ["distributed systems", "database internals", "replication", "consistency"],
    },
    {
        "source": "book",
        "title": "Clean Code",
        "instructor": "Robert C. Martin",
        "platform_display": "Book",
        "language": "en",
        "level": "intermediate",
        "is_free": False,
        "has_certificate": False,
        "skills_covered": ["Python", "Java", "JavaScript"],
        "career_tracks": ["backend_engineer", "frontend_engineer"],
        "is_indonesia_specific": False,
        "is_bahasa_indonesia": False,
        "description_short": (
            "The standard reference for writing readable, maintainable code. "
            "Covers naming, functions, comments, error handling, and testing. "
            "Recommended reading after completing the foundations phase."
        ),
        "topics_covered": ["clean code", "refactoring", "SOLID", "testing", "code quality"],
    },
    {
        "source": "book",
        "title": "System Design Interview – An Insider's Guide",
        "instructor": "Alex Xu",
        "platform_display": "Book",
        "language": "en",
        "level": "intermediate",
        "is_free": False,
        "has_certificate": False,
        "skills_covered": ["System Design"],
        "career_tracks": ["backend_engineer", "devops_engineer"],
        "is_indonesia_specific": False,
        "is_bahasa_indonesia": False,
        "description_short": (
            "The most widely used system design interview prep book. "
            "Covers URL shortener, rate limiter, notification system, YouTube, "
            "Google Drive, and more. Practical and example-driven."
        ),
        "topics_covered": ["system design", "scalability", "load balancing", "caching", "database design"],
    },
    {
        "source": "book",
        "title": "Python Crash Course",
        "instructor": "Eric Matthes",
        "platform_display": "Book",
        "language": "en",
        "level": "beginner",
        "is_free": False,
        "has_certificate": False,
        "skills_covered": ["Python"],
        "career_tracks": ["backend_engineer", "data_analyst", "ml_ai_engineer"],
        "is_indonesia_specific": False,
        "is_bahasa_indonesia": False,
        "description_short": (
            "The most recommended Python beginner book. Structured, project-based, "
            "covers fundamentals through three real projects: a game, data visualization, "
            "and a web app."
        ),
        "topics_covered": ["python fundamentals", "projects", "web development", "data visualization"],
    },
    {
        "source": "book",
        "title": "Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow",
        "instructor": "Aurélien Géron",
        "platform_display": "Book",
        "language": "en",
        "level": "intermediate",
        "is_free": False,
        "has_certificate": False,
        "skills_covered": ["Scikit-learn", "TensorFlow", "PyTorch", "Pandas"],
        "career_tracks": ["ml_ai_engineer", "data_analyst"],
        "is_indonesia_specific": False,
        "is_bahasa_indonesia": False,
        "description_short": (
            "The standard ML practitioner book. Covers the full pipeline from "
            "data preparation through training, tuning, and deployment. "
            "Requires Python fundamentals as prerequisite."
        ),
        "topics_covered": ["machine learning", "neural networks", "deep learning", "model deployment"],
    },
]
