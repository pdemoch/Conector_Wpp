from Flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Webhook ativo", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == 'EAAIZBEkh9ymIBOZC3PzlyTPrOZATZAUriNXK5tNMP63BBMSga51aEnTbygG87ZBNnwwx3zfAD0n60iEbUHR71F1sBOZBzjn1SsuGtuZC7aFOFPyoxxKpZC33mhXVWKOLrizCSPbcHJH6p3ybrOPMekgLLJRhlRqfSrqV5er92vL6mqqSqsbAUF30rP1SXGWA3yZBtUpgPAwdGDZB5xLmgvg8CZBiu5e':
            return challenge, 200
        return 'Token inválido', 403

    if request.method == 'POST':
        data = request.json
        print("Mensagem recebida:", data)
        return "OK", 200

if __name__ == '__main__':
    app.run()