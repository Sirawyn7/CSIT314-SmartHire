
# Synonym groups for fuzzy query expansion.
# Every term in a group maps to all other terms in that group — bidirectional by construction.

_GROUPS = [
    # Roles
    ["software engineer", "programmer", "coder", "developer", "software developer"],
    ["data scientist", "data analyst", "ml engineer", "machine learning engineer"],
    ["devops", "devops engineer", "site reliability engineer", "sre", "infrastructure engineer"],
    ["designer", "ux designer", "ui designer", "ux/ui designer", "product designer"],
    ["project manager", "pm", "program manager", "delivery manager", "scrum master"],
    ["qa engineer", "tester", "quality assurance", "test engineer"],
    ["systems administrator", "sysadmin", "it administrator"],
    ["business analyst", "ba", "systems analyst"],
    ["frontend developer", "front end developer", "front-end developer", "ui developer"],
    ["backend developer", "back end developer", "back-end developer", "server side developer"],
    ["fullstack developer", "full stack developer", "full-stack developer"],

    # Languages and technologies
    ["javascript", "js"],
    ["typescript", "ts"],
    ["python", "py"],
    ["golang", "go"],
    ["kotlin", "android development"],
    ["swift", "ios development"],
    ["c#", "csharp", "dotnet", ".net"],
    ["postgresql", "postgres"],
    ["mongodb", "mongo"],

    # Concepts
    ["machine learning", "ml", "artificial intelligence", "ai"],
    ["natural language processing", "nlp"],
    ["cloud", "cloud computing", "aws", "azure", "gcp", "google cloud"],
    ["agile", "scrum", "kanban", "sprint"],
    ["ci/cd", "continuous integration", "continuous deployment", "devops pipeline"],
    ["rest", "rest api", "restful", "api development"],
    ["docker", "containerisation", "containerization"],
    ["kubernetes", "k8s", "container orchestration"],
]


def _build_synonym_map(groups):
    """Builds a flat bidirectional dict from synonym groups."""
    synonym_map = {}
    for group in groups:
        for term in group:
            related = [t for t in group if t != term]
            synonym_map[term.lower()] = [r.lower() for r in related]
    return synonym_map


SYNONYMS = _build_synonym_map(_GROUPS)