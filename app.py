from flask import Flask, request, redirect
import jwt
import time
from pathlib import Path
from urllib.parse import urlencode

app = Flask(__name__)

FRESHDESK_DOMAIN = "rmview-org.myfreshworks.com"

CLIENT_ID = "832352753658967768"
PRIVATE_KEY = """
-----BEGIN RSA PRIVATE KEY-----
MIICWgIBAAKBgH2EM6SEnkf85RJLpTi6qKcehrGOh0a+l8VHv5shsrwcMJxHRHsi
0DMpYDyuQSWSlhPi+AQwphJk6G0P3/chv911yxG1IGDgsaAKs6OYT+K4qga7sw8m
JWfXEQhXlURWpisrE1C8wWBxpA80JMStPilyREG0YrWSEO51cfcaUiCrAgMBAAEC
gYBiuoBcoixWd6g/0dyuWLScb7iHJZNmpDiBZ0Rh5AnRSWM7KhvFt8aI17zpPi/k
O/9suRVZRmL7CQCB+QC0RYnCpS02f4x5deOY9378l1MQ4CaI1rXeWXB77kcN206q
ha0eMScniE6OGHgMC6w55Pw30noPKjz7m16DGEbc6ztLsQJBAO9YKnABciKthUCj
z+fh2UGT9IFxmSRptMfvOfzON2amrijlhQpniVYxpgopsHObGMSyVAQ0tkR8OA3L
bFx1MacCQQCGQDs9/qNnykkd/QPbvEqBJn52IgK6b7jTbN9MBpjUWUuJDNj1bpOV
bCGTI/tHlMJHy909OYoF4/BJB7OpVRFdAkBTrA/R7j93bg/6hAoHt4XbDh1ZL1xp
RWcEylYMUg8+HKEf/PUgqQdzEZJJVT+xepQTF4CVo9PgZ0i1UdtFC1dbAkAX2CCt
iiSLsqn54Y5l4LN67NNZOAE0C9PP+W5PmnxaeuGnndiK/vDHgUUVVTa0J/+5sMPC
tA2HrkxnLC8EzE8hAkAC20Es+ZvIJbQgY15xr0NHc1Y+cMIWug+yet7VxrjF063H
tutEByCRKIRQZPNfH5BQedKojmZfrjKlE5Rokntp
-----END RSA PRIVATE KEY-----
"""

@app.route("/login")
def sso():
    state = request.args.get("state")
    nonce = request.args.get("nonce")

    if not state or not nonce:
        return "Missing state or nonce", 400

    payload = {
        "sub": "121213",
        "email": "uiz.thiago@dacta.tec.br",
        "given_name": "Luiz",
        "family_name": "Thiago",
        "iat": int(time.time()),
        "nonce": nonce,
        "company": "rmview"
    }

    token = jwt.encode(
        payload,
        PRIVATE_KEY,
        algorithm="RS256"
    )

    redirect_url = f"https://{FRESHDESK_DOMAIN}/sp/OIDC/{CLIENT_ID}/implicit?" + urlencode({
        "state": state,
        "id_token": token
    })
    
    print(f"Redirecting to: {redirect_url}")

    return redirect(redirect_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
