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
        if token == 'EAAIZBEkh9ymIBOyJGqYlP06nlOLOil5pYJkqcb0aZCKZAwzS2fSMyPdp2fM0qw9Kd4uouYUK3HGyjRZC7Ec0F4Yb0pm2lPOvFcPOawxnvYfDAvkXuVlAso4gITGYZBFjSACNbSYZB4X3yZCM2jyIhoj4ZA0z6mv8ZAZB9S6isdXXZAAGG2zrIc7v0yKBi5ZCK3e8iE564d9Id3v50mRn9tLvAW8EfqoZD':
            return challenge, 200
        return 'Token inválido', 403

    if request.method == 'POST':
        data = request.json
        print("Mensagem recebida:", data)
        return "OK", 200

if __name__ == '__main__':
    app.run()