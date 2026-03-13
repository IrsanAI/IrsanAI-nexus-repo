from fastapi import FastAPI
from backend.config import settings

app = FastAPI(title=settings.app_name)

@app.get('/health')
def health():
    return {'status': 'ok', 'version': settings.app_version}
