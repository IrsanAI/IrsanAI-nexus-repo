from fastapi import APIRouter, HTTPException
from pathlib import Path
from backend.analyzer.unified_analyzer import analyze
from backend.analyzer.cloner import clone_repo, cleanup_repo

router = APIRouter()

@router.post('/analyze')
def analyze_repo(repo_url: str):
    try:
        path = clone_repo(repo_url)
        result = analyze(Path(path), repo_url)
        cleanup_repo(path)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
