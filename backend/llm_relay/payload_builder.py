import json
from .model_adapters import get_adapter

ROLE_PERSPECTIVES = ['CEO','Investor','Dev','Security','Marketer','UX','Lawyer','AI_Researcher']

def build_payload(analysis: dict, model: str = 'openai', round_num: int = 1) -> dict:
    adapter = get_adapter(model)
    payload = {'analysis_version':analysis.get('analysis_version','1.0.0'),'repo_meta':analysis.get('repo_meta',{}),'metrics':analysis.get('metrics',{}),'languages':analysis.get('languages',{}),'repo_iq':analysis.get('repo_iq',{}),'hidden_unicorn_probability':analysis.get('hidden_unicorn_probability',0),'role_perspectives':ROLE_PERSPECTIVES,'opportunity_map':_build_opportunity_map(analysis),'requested_task':_get_task_for_round(round_num),'attachments':{'top_n_files':_trim_files(analysis.get('top_n_files',[]),adapter.max_input_tokens),'dependency_list':analysis.get('metrics',{}).get('detected_techs',[]),}}
    return _wrap_for_model(payload, adapter, model)

def _build_opportunity_map(analysis: dict) -> dict:
    iq = analysis.get('repo_iq',{}).get('repo_iq',0)
    unicorn = analysis.get('hidden_unicorn_probability',0)
    return {'saas_potential':'HIGH' if iq>70 else 'MEDIUM' if iq>50 else 'LOW','open_source_community':'HIGH' if analysis.get('metrics',{}).get('commit_count',0)>100 else 'MEDIUM','hidden_unicorn_probability':unicorn,'monetization_hints':_monetization_hints(analysis)}

def _monetization_hints(analysis: dict) -> list:
    hints=[]
    langs=analysis.get('languages',{})
    if 'Python' in langs:
        hints.append('PyPI-Paket mit Premium-Tier möglich')
    if 'TypeScript' in langs or 'JavaScript' in langs:
        hints.append('SaaS-Frontend oder npm-Plugin möglich')
    if analysis.get('metrics',{}).get('has_tests',False):
        hints.append('Enterprise-Support Offering (hohe Code-Qualität)')
    return hints or ['Weitere Analyse empfohlen']

def _get_task_for_round(round_num: int) -> str:
    if round_num == 1:
        return 'Analyze this repository comprehensively. For each role in role_perspectives, provide a 3-5 sentence assessment. Include top 3 risks and top 5 opportunities. Return valid JSON only.'
    return 'Based on the Round 1 analysis provided, deepen the product strategy. Identify hidden use cases, suggest 3 SaaS product ideas with pricing tiers, and estimate 12-month market potential. Return valid JSON only.'

def _trim_files(files: list, max_tokens: int) -> list:
    snippet_limit = 200 if max_tokens < 50000 else 500
    return [{**f, 'snippet': f.get('snippet','')[:snippet_limit]} for f in files]

def _wrap_for_model(payload: dict, adapter, model: str) -> dict:
    content = json.dumps(payload, ensure_ascii=False, indent=2)
    messages = [{'role':'system','content':adapter.system_prompt_prefix},{'role':'user','content':f'Repository Analysis Data:\n\n{content}'}]
    return {'model':_default_model_name(model),'messages':messages,'max_tokens':4096,'response_format':{'type':'json_object'}}

def _default_model_name(model: str) -> str:
    return {'openai':'gpt-4o'}.get(model,'gpt-4o')
