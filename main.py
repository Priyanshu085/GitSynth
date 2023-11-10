from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel

app = FastAPI()

# For simplicity, hardcoding GitHub OAuth credentials for testing.
# In a real application, use environment variables and a secure method to manage credentials.
GITHUB_CLIENT_ID = "your_client_id"
GITHUB_CLIENT_SECRET = "your_client_secret"
GITHUB_REDIRECT_URI = "login/callback"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_REDIRECT_URI}",
    tokenUrl="https://github.com/login/oauth/access_token",
    scopes={"read:user", "repo"},
    flow="authorizationCode"
    # redirectUri=GITHUB_REDIRECT_URI,
)

@app.get("/login/github")
async def github_login(authorize_url: str = Depends(oauth2_scheme)):
    return {"message": "Redirecting to GitHub for authentication", "authorize_url": authorize_url}

@app.get("/login/callback")
async def github_callback(code: str = Depends(oauth2_scheme)):
    # In a real application, handle GitHub OAuth callback and retrieve access token.
    return {"code": code}
# conn = MongoClient('mongodb+srv://abpriyanshu007:R94Z3mJXsl5Q94E8@cluster0.tjmjpcd.mongodb.net/')

# @app.get("/", response_class=HTMLResponse)
# async def read_item(request: Request):
#     docs = conn.my.test.find_one({})
#     print(docs)
#     return templates.TemplateResponse("index.html", {"request": request})

# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Hello, World!"}

# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000)
