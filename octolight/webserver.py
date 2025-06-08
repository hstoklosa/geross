import os 
from dotenv import load_dotenv; load_dotenv()

from flask import Flask, request, abort

from utils import verify_signature

app = Flask(__name__)

WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # Validate signature
    signature = request.headers.get('X-Hub-Signature-256', '')
    if not verify_signature(request.data, signature, WEBHOOK_SECRET):
        abort(400, 'Invalid signature')

    # Check event type
    event = request.headers.get('X-GitHub-Event', '')
    payload = request.json or {}
    if event == 'star' and payload.get('action') == 'created':
        user = payload['sender']['login']
        repo = payload['repository']['full_name']
        print(f":star: {user} starred {repo}")

    return '', 204


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
