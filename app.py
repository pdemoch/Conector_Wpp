from flask import Flask, request
from responder import responder_ia
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@app.route('/')
def home():
    return "Webhook ativo", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == os.getenv("VERIFY_TOKEN"):
            return challenge, 200
        return 'Token inválido', 403

    if request.method == 'POST':
        data = request.json
        try:
            mensagem = data['entry'][0]['changes'][0]['value']['messages'][0]
            numero = mensagem['from']
            texto = mensagem['text']['body']
            print(f"Mensagem de {numero}: {texto}")
            responder_ia(numero, texto)
        except Exception as e:
            print("Erro ao processar:", e)
        return "OK", 200

if __name__ == '__main__':
    app.run()