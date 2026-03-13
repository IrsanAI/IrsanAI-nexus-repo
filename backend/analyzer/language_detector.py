from pathlib import Path
from collections import Counter

EXTENSION_MAP = {'.py':'Python','.js':'JavaScript','.ts':'TypeScript','.java':'Java','.go':'Go','.rs':'Rust','.cpp':'C++','.c':'C','.cs':'C#','.rb':'Ruby','.php':'PHP','.swift':'Swift','.kt':'Kotlin','.r':'R','.scala':'Scala','.sh':'Shell','.html':'HTML','.css':'CSS','.sql':'SQL','.md':'Markdown','.yml':'YAML','.yaml':'YAML','.json':'JSON','.toml':'TOML','.dockerfile':'Docker'}
IGNORE_DIRS = {'.git','node_modules','__pycache__','.venv','venv','dist','build'}

def detect_languages(repo_path: Path) -> dict:
    counts = Counter()
    total = 0
    for f in repo_path.rglob('*'):
        if f.is_file() and not any(ig in f.parts for ig in IGNORE_DIRS):
            lang = EXTENSION_MAP.get(f.suffix.lower())
            if lang:
                counts[lang] += 1
                total += 1
    if total == 0:
        return {}
    return {lang:{'count':c,'percent':round(c/total*100,1)} for lang,c in counts.most_common()}
