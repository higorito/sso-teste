import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
REALM_NAME = os.getenv("REALM_NAME")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

app = FastAPI(title="Keycloak User Creator", description="Cria usuários no Keycloak via API", version="1.0.0")

class User(BaseModel):
    username: str
    email: str
    firstName: str
    lastName: str
    password: str

def get_keycloak_access_token():
    url = f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise HTTPException(status_code=500, detail=f"Erro ao obter o token: {response.text}")

@app.post("/create-user", summary="Cria um usuário no Keycloak")
def create_user_in_keycloak(user: User):
    token = get_keycloak_access_token()

    user_data = {
        "username": user.username,
        "email": user.email,
        "enabled": True,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "credentials": [{
            "type": "password",
            "value": user.password,
            "temporary": False
        }]
    }

    url = f"{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/users"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(url, json=user_data, headers=headers)

    if response.status_code == 201:
        return {"message": "Usuário criado com sucesso!"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
