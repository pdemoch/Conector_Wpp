import requests
import os
from dotenv import load_dotenv
import openai

load_dotenv()

TOKEN_WPP = os.getenv("WHATSAPP_TOKEN")
ID_TELEFONE = os.getenv("WHATSAPP_ID")
openai.api_key = os.getenv("OPENAI_API_KEY")

def responder_ia(telefone, pergunta):
    resposta = gerar_resposta(pergunta)
    url = f"https://graph.facebook.com/v18.0/{ID_TELEFONE}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN_WPP}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": telefone,
        "type": "text",
        "text": {"body": resposta}
    }
    r = requests.post(url, headers=headers, json=payload)
    print("Enviado:", r.status_code, r.text)

def gerar_resposta(pergunta):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": pergunta}]
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        print("Erro com OpenAI:", e)
        return "Desculpe, houve um erro na IA."