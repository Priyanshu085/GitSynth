import os
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from dotenv import load_dotenv

import os
import sys

# Get the path to the directory containing test_main.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Append the project directory to the Python path
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)

# from main import router
load_dotenv()

# app = FastAPI()

# # Set the environment variables for testing
# os.environ["TESTING"] = "True"
# os.environ["GITHUB_CLIENT_ID"] = "Iv1.10d5ad807d29af56"
# os.environ["GITHUB_CLIENT_SECRET"] = "a828464cd093b5a0940f1fc6700d4904c19ff1ec"
# os.environ["GITHUB_REDIRECT_URI"] = "http://127.0.0.1:8000/login/callback"

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

@pytest.mark.parametrize("endpoint", ["/login/github", "/login/callback"])
def test_endpoints_status_code(endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200

def test_github_login_response():
    response = client.get("/login/github")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Redirecting to GitHub for authentication" in response.json()["message"]

def test_github_callback_response():
    response = client.get("/login/callback")
    assert response.status_code == 200
    assert "code" in response.json()