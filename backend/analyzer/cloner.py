import subprocess
import shutil
import re
import uuid
from pathlib import Path
from backend.config import settings

class ClonerError(Exception):
    pass

def validate_github_url(url: str) -> str:
    pattern = r'^https://github\.com/[\w\-\.]+/[\w\-\.]+(?:\.git)?$'
    if not re.match(pattern, url):
        raise ClonerError(f"Ungültige oder unsichere GitHub URL: {url}")
    return url.rstrip('/')

def clone_repo(url: str, job_id: str | None = None) -> Path:
    url = validate_github_url(url)
    job_id = job_id or str(uuid.uuid4())[:8]
    target = settings.work_dir / job_id
    settings.work_dir.mkdir(parents=True, exist_ok=True)
    if target.exists():
        shutil.rmtree(target)
    result = subprocess.run(['git', 'clone', '--depth=50', url, str(target)], capture_output=True, text=True)
    if result.returncode != 0:
        raise ClonerError(f'git clone fehlgeschlagen: {result.stderr}')
    return target

def cleanup_repo(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
