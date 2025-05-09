from flask import Flask, request, jsonify
import requests
import os
import json
from openai import OpenAI

app = Flask(__name__)

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_ID = os.getenv("WHATSAPP_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["GET"])
def verificar_webhook():
    verify_token = "meu_token_seguro"  # Troque se for diferente no painel do Meta
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == verify_token:
        return str(challenge)
    return "Token inválido", 403

@app.route("/webhook", methods=["POST"])
def receber_mensagem():
    data = request.get_json()
    print("🔹 JSON RECEBIDO:")
    print(json.dumps(data, indent=2))

    try:
        value = data["entry"][0]["changes"][0]["value"]

        if "messages" in value:
            for msg in value["messages"]:
                numero = msg.get("from")
                texto = msg.get("text", {}).get("body")

                if numero and texto:
                    print(f"📩 Mensagem recebida de {numero}: {texto}")
                    responder_ia(numero, texto)
                else:
                    print("⚠️ Mensagem recebida sem texto.")
        else:
            print("ℹ️ Webhook sem mensagens. Provavelmente é status de entrega/leitura.")
    except Exception as e:
        print(f"❌ Erro ao processar evento do webhook: {e}")

    return "OK", 200

def responder_ia(numero, mensagem_usuario):
    prompt = f"O cliente disse: {mensagem_usuario}. Responda de forma educada e amigável como se fosse de um estúdio de tatuagem moderno."
    resposta = gerar_resposta_openai(prompt)
    enviar_mensagem(numero, resposta)

def gerar_resposta_openai(prompt):
    try:
        openai = OpenAI(api_key=OPENAI_API_KEY)
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Erro ao gerar resposta da OpenAI: {e}")
        return "Desculpe, não consegui entender sua mensagem agora."

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
    response = requests.post(url, headers=headers, json=payload)
    print(f"📤 Enviando mensagem para {numero}: {texto}")
    print(f"🔁 Status envio: {response.status_code}")
    print(f"🔁 Resposta: {response.text}")

if __name__ == "__main__":
    app.run(debug=True, port=5002)