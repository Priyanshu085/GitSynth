from fastapi import FastAPI
# from pymongo import MongoClient
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
import httpx
import os
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

load_dotenv()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

app = FastAPI()

User = {
    "name": "",
    "username": "",
    "email": "",
    "repo": "",
    "bio": "",
    "followers": "",
    "following": "",
}

RepoName = []

RepoData = {}

access_token = ""
@app.get("/")
def Home():
    return {"message": "Hello, Welcome to My GitSynth App"}    

def Welcome(User):
    # text = "Welcome to My GitSynth App "+User["name"]
    print("Username: ", User["username"])
    print("Email: ", User["email"])
    print("Bio: ", User["bio"])
    print("Followers: ", User["followers"])
    print("Following: ", User["following"])
    print("Repositories: ", User["repo"])

    get_user_repositories(User["username"])

    return User
@app.get("/user")
def get_commit_history():
    commits_url = f'https://api.github.com/repos/{Priyanshu085}/{Priyanshu085}/commits'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    response = httpx.get(commits_url, headers=headers)
    response.raise_for_status()
    return response.json()

# # Create a directed graph
# commits_graph = nx.DiGraph()

# # Add nodes (commits)
# for repo_name, repo_info in RepoData.items():
#     commit_history = get_commit_history(repo_info["owner"]["login"], repo_name, 'YOUR-GITHUB-TOKEN')
#     for commit in commit_history:
#         commit_sha = commit["sha"]
#         commits_graph.add_node(commit_sha, data=commit)

# # Add edges (chronological order of commits)
# for repo_name, repo_info in RepoData.items():
#     commit_history = get_commit_history(repo_info["owner"]["login"], repo_name, 'YOUR-GITHUB-TOKEN')
#     for i in range(1, len(commit_history)):
#         previous_commit = commit_history[i - 1]["sha"]
#         current_commit = commit_history[i]["sha"]
#         commits_graph.add_edge(previous_commit, current_commit)

# print(commits_graph)


def get_user_repositories(repo):
    return repo

GITHUB_TOKEN = ""
GITHUB_API_VERSION = '2022-11-28'    

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
    
    headers = {"Accept": "application/vnd.github+json"}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url="https://github.com/login/oauth/access_token",
                params=params,
                headers=headers,
            )
            response = response.json()
            GITHUB_TOKEN = response["access_token"]

        async with httpx.AsyncClient() as client:
            headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'X-GitHub-Api-Version': GITHUB_API_VERSION,
            }
            # headers = {"Authorization": f"token {access_token}"}
            response = await client.get(
                url="https://api.github.com/user",
                headers=headers,
            )
            user_data = response.json()
            User["username"] = user_data["login"]

            User["name"] = user_data["name"]

            User["email"] = user_data["email"]

            User["bio"] = user_data["bio"]
            User["followers"] = user_data["followers"]
            User["following"] = user_data["following"]

            User["repo"] = user_data["repos_url"]

            df = pd.DataFrame(user_data, index=[0])
            # df["topics"].dropna(inplace=True)
            df.to_csv('test/data.csv', index=False)

        # Set up the GitHub API base URL
        GITHUB_API_BASE_URL = 'https://api.github.com'

        # Specify the username for which you want to get repositories
        username = User["username"]

        # Set up headers including the GitHub API version and authorization token
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'X-GitHub-Api-Version': GITHUB_API_VERSION,
        }

            # Make the request to get repositories for the specified username
        url = f'{GITHUB_API_BASE_URL}/users/{username}/repos'

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                repositories = response.json()

                for repo in repositories:
                    RepoData[RepoName["name"]] = repositories["name"]
                    RepoName.append(RepoName["name"])
                     # print(repo["name"])

                Repo = repositories

                # get_user_repositories(repositories)
        except httpx.HTTPError as e:
            print(f'GitHub API Error: {str(e)}')
        except Exception as e:
            print(f'Unexpected error: {str(e)}')

        for repo_name in RepoName:
            commits_url = f'https://api.github.com/repos/{username}/{repo_name}/commits'
            response = httpx.get(commits_url, headers=headers)
            response.raise_for_status()

        df = pd.DataFrame(response.json())

        df.to_csv('test/repo.csv', index=False)
        return get_user_repositories(repositories)

            # return Welcome(User)
                # return user
                # return redirect(url_for('Welcome', name=name))

            # user_collection = db["my"]
            # result = await user_collection.insert_one(user_data)
            # user_id = result.inserted_id

            # return user_id

    except httpx.HTTPError as e:
        return {"error": f'GitHubb API Error {str(e)}'}

    except Exception as e:
        return {"error": f'Unexpected error {str(e)}'}
    
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

