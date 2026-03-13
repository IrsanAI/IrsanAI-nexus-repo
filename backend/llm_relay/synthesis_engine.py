import json
from datetime import datetime, timezone

class SynthesisEngine:
    def __init__(self, analysis: dict):
        self.analysis = analysis
        self.rounds = []
    def ingest_response(self, raw_response: str, model: str, round_num: int) -> dict:
        try:
            clean = raw_response.strip()
            if clean.startswith('```'):
                clean = clean.split('```')[1]
                if clean.startswith('json'):
                    clean = clean[4:]
            parsed = json.loads(clean)
        except Exception:
            parsed = {'raw_text': raw_response, 'parse_error': True}
        entry = {'round': round_num,'model': model,'timestamp': datetime.now(timezone.utc).isoformat(),'data': parsed}
        self.rounds.append(entry)
        return entry
    def synthesize(self) -> dict:
        return {'title':'IRSAN-AI Command Center Report','version':'1.0','generated_at': datetime.now(timezone.utc).isoformat(),'repo_meta': self.analysis.get('repo_meta',{}),'repo_iq': self.analysis.get('repo_iq',{}),'hidden_unicorn_probability': self.analysis.get('hidden_unicorn_probability',0),'static_analysis':{'languages': self.analysis.get('languages',{}),'security': self.analysis.get('security',{}),'metrics': self.analysis.get('metrics',{})},'llm_rounds': self.rounds,'synthesized_insights': self._extract_insights(),'export_ready': True}
    def _extract_insights(self) -> dict:
        all_opportunities=[]
        all_risks=[]
        for r in self.rounds:
            data = r.get('data',{})
            all_opportunities += data.get('opportunities',[])
            all_risks += data.get('risks',[]) + data.get('risk_matrix',[])
        return {'top_opportunities': all_opportunities[:5],'top_risks': all_risks[:3],'round_count': len(self.rounds)}
