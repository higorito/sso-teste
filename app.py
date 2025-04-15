from flask import Flask, request, redirect, jsonify
import jwt
import datetime
from urllib.parse import urlencode, urlparse, parse_qs
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes

app = Flask(__name__)

PRIVATE_KEY = """
-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----
"""

FRESHDESK_URL = "https://rmview-org.myfreshworks.com/sp/OIDC/832315941349708585/implicit"


def load_private_key():
    """Carrega a chave privada para assinar o JWT."""
    return serialization.load_pem_private_key(
        PRIVATE_KEY.encode(),
        password=None,
    )


def generate_jwt(state, nonce):
    private_key = load_private_key()
    now = datetime.datetime.utcnow()

    payload = {
        "sub": "1234567890",
        "email": "higor.pereira@dacta.tec.br",
        "nonce": nonce,
        "state": state,
        "iat": int(now.timestamp()),
        "exp": int((now + datetime.timedelta(minutes=5)).timestamp()),
        "given_name": "Higor",
        "family_name": "Silva",
    }

    return jwt.encode(payload, private_key, algorithm="RS256")



@app.route("/login", methods=["GET"])
def login():
    """Endpoint de login que recebe os parâmetros de Freshdesk e gera o JWT."""
    uri_from_freshdesk_request = request.url
    query = parse_qs(urlparse(uri_from_freshdesk_request).query)

    if "state" not in query or "nonce" not in query:
        return jsonify({"error": "Missing 'state' or 'nonce' parameter"}), 400

    state = query["state"][0]
    nonce = query["nonce"][0]

    # Gerar o JWT
    id_token = generate_jwt(state, nonce)

    print(jwt.decode(id_token, options={"verify_signature": False}))

    redirect_url = f"{FRESHDESK_URL}?state={state}&id_token={id_token}"

    return redirect(redirect_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
