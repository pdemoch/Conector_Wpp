from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Webhook ativo", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == 'EAAIZBEkh9ymIBO26zUZAFG4jsrtQNmI6OTdZBuBJVA1AmoTWd9ZBhZAsSAwm6vc6YIkh7zauOgNRw8TDiBjLsSHIygrsG3vFjb1ZAqzhMM8EfKUyGCKs5Ik9Coj17L0eGZCVxIZAQe2elFPmk3Jkt6GjJjuozQJFlsX6ZA4BwLDjYCpYivgPELZApAo6LMCHdktPeGgkrbf8OZCW1aFajBdvIPeSigZD':
            return challenge, 200
        return 'Token inválido', 403

    if request.method == 'POST':
        data = request.json
        print("Mensagem recebida:", data)
        return "OK", 200

if __name__ == '__main__':
    app.run()