from dataclasses import dataclass

@dataclass
class ModelAdapter:
    name: str
    api_url: str
    curl_example: str
    system_prompt_prefix: str
    max_input_tokens: int
    chunking_note: str

ADAPTERS: dict[str, ModelAdapter] = {
    'openai': ModelAdapter(
        name='ChatGPT (OpenAI)',
        api_url='https://api.openai.com/v1/chat/completions',
        curl_example='curl https://api.openai.com/v1/chat/completions \\  -H "Authorization: Bearer $OPENAI_API_KEY" \\  -H "Content-Type: application/json" \\  -d @payload_openai.json',
        system_prompt_prefix='You are an expert software architect and product analyst. Analyze the provided repository data and return a structured JSON response with keys: summary, strengths, risks, opportunities, recommendations.',
        max_input_tokens=128000,
        chunking_note='Bei >100k Tokens: Teile top_n_files in 2 Payloads. Sende role_perspectives in Runde 2.',
    ),
}
