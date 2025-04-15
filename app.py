from flask import Flask, redirect
import jwt
import datetime

app = Flask(__name__)

@app.route("/login")
def login():
    private_key_path = "private.pem"
    with open(private_key_path, "r") as key_file:
        private_key = key_file.read()

    payload = {
        "sub": "1234567890",
        "email": "usuario@example.com",
        "nonce": "123422",
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
        "iss": "rmview",
        "aud": "freshdesk"
    }

    token = jwt.encode(payload, private_key, algorithm="RS256")

    redirect_url = f"https://rmview-org.myfreshworks.com/sp/OIDC/832315941349708585/implicit?id_token={token}&state=abc123"
    return redirect(redirect_url)
