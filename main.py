from fastapi import FastAPI
from pymongo import MongoClient
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
import httpx
import os
from db import db
import uvicorn

load_dotenv()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
# GITHUB_REDIRECT_URI = "http://localhost:8000/login/callback"

app = FastAPI()

def Welcome(name):
    text = "Welcome to My GitSynth App-> "+name
    return text

@app.get("/github-login")
async def github_login():
    return RedirectResponse(
        f'https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}', 
        status_code=302
    )

@app.get("/github-callback")
async def github_callback(code: str):
    if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
        return {"error": "GitHub credentials not configured properly"}

    params = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
    }

    headers = {"Accept": "application/json"}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url="https://github.com/login/oauth/access_token",
                params=params,
                headers=headers,
            )
            response = response.json()
            access_token = response["access_token"]
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"token {access_token}"}
                response = await client.get(
                    url="https://api.github.com/user",
                    headers=headers,
                )
                # response.raise_for_status() # Raises an exception if response code is 4xx or 5xx
                user_data = response.json()
                name = user_data["login"]
            
                return Welcome(name=name)

            # user_collection = db["my"]
            # result = await user_collection.insert_one(user_data)
            # user_id = result.inserted_id

            # return user_id

    except httpx.HTTPError as e:
        return {"error": f'GitHubb API Error {str(e)}'}

    except Exception as e:
        return {"error": f'Unexpected error {str(e)}'}
    

@app.get("/")
async def home():
#     # In a real application, handle GitHub OAuth callback and retrieve access token.
    return {"message": "Hello, Welcome to My GitSynth App"}

# @app.get("/user")
# async def get_users():
    
@app.get("/")
def Home():
    return {"message": "Hello, Welcome to My GitSynth App"}    

# uvicorn.run(app, host="0.0.0.0", port=8001)


