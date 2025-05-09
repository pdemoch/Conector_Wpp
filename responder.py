import requests
import os
from openai import OpenAI

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_ID = os.getenv("WHATSAPP_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def responder_ia(numero, mensagem_usuario):
    prompt = f"Usuário disse: {mensagem_usuario}. Responda de forma educada e útil."
    
    # Consulta à OpenAI
    resposta = gerar_resposta_openai(prompt)

    # Envia para o WhatsApp
    enviar_mensagem(numero, resposta)

def gerar_resposta_openai(prompt):
    openai = OpenAI(api_key=OPENAI_API_KEY)
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def enviar_mensagem(numero, texto):
    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": texto}
    }
    requests.post(url, headers=headers, json=payload)