from pathlib import Path

WEIGHTS = {'engineering_quality':0.30,'innovation_score':0.25,'security_posture':0.20,'documentation':0.15,'community_signals':0.10}

def score_engineering_quality(metrics: dict) -> float:
    score = 50.0
    if metrics.get('avg_complexity',10) < 5:
        score += 20
    elif metrics.get('avg_complexity',10) > 15:
        score -= 20
    if metrics.get('has_tests', False):
        score += 20
    if metrics.get('lint_score',5) > 7:
        score += 10
    return max(0,min(100,score))

def score_innovation(metrics: dict) -> float:
    score = 40.0
    lang_count = metrics.get('language_count',1)
    score += min(lang_count*5,25)
    modern_techs = {'rust','go','typescript','webassembly','llm','ai','ml'}
    techs = {t.lower() for t in metrics.get('detected_techs',[])}
    score += len(techs & modern_techs) * 5
    return max(0,min(100,score))

def score_security_posture(metrics: dict) -> float:
    score = 80.0
    score -= metrics.get('critical_issues',0) * 15
    score -= metrics.get('high_issues',0) * 7
    return max(0,min(100,score))

def score_documentation(repo_path: Path) -> float:
    score = 0.0
    checks = {'README.md':30,'CHANGELOG.md':15,'CONTRIBUTING.md':15,'LICENSE':20,'docs/':20}
    for name,pts in checks.items():
        if (repo_path / name).exists():
            score += pts
    return min(100,score)

def calculate_repo_iq(metrics: dict, repo_path: Path) -> dict:
    scores = {'engineering_quality':score_engineering_quality(metrics),'innovation_score':score_innovation(metrics),'security_posture':score_security_posture(metrics),'documentation':score_documentation(repo_path),'community_signals':min(100,metrics.get('commit_count',0)*2)}
    total = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
    return {'dimensions':scores,'weights':WEIGHTS,'repo_iq':round(total,1)}

def hidden_unicorn_probability(metrics: dict) -> float:
    score = 0.0
    score += min(metrics.get('stars_proxy',0)/1000,0.3)
    score += min(metrics.get('commit_count',0)/500,0.25)
    score += 0.2 if metrics.get('has_tests',False) else 0.0
    lang_bonus = min(metrics.get('language_count',1)/5,0.15)
    score += lang_bonus
    score += 0.1 if metrics.get('has_ci',False) else 0.0
    return round(min(score,1.0),3)
