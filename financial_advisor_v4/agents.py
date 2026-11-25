import requests

def call(provider, model, key, prompt):
    if not key: raise ValueError(f'{provider} API key missing')
    url = 'https://api.groq.com/openai/v1/chat/completions' if provider=='Groq' else 'https://api.cohere.com/v2/chat'
    response=requests.post(url,headers={'Authorization':f'Bearer {key}','Content-Type':'application/json'},json={'model':model,'messages':[{'role':'user','content':prompt}],'max_tokens':900},timeout=45)
    if not response.ok: raise RuntimeError(f'{provider} API HTTP {response.status_code}; check key, model and quota')
    data=response.json()
    if provider=='Groq': return data['choices'][0]['message']['content']
    return '\n'.join(x['text'] for x in data['message']['content'] if x.get('type')=='text')
