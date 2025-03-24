import requests
from datetime import datetime

GITHUB_API_URL = "https://api.github.com"

def fetch_commits(user, repo, per_page=100, headers=None):
    """
    Fetches commits from a GitHub repo with hardcoded limits.
    Returns a list of commit timestamps.
    """
    commits = []
    page = 1
    max_pages = 20
    max_commits = 2000

    while True:
        if page > max_pages:
            print(f"Reached page limit ({max_pages}).")
            break
        if len(commits) >= max_commits:
            print(f"Reached commit limit ({max_commits}).")
            break

        url = f"{GITHUB_API_URL}/repos/{user}/{repo}/commits"
        params = {"per_page": per_page, "page": page}
        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch page {page} - Status code: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        for commit in data:
            try:
                timestamp = commit['commit']['committer']['date']
                commits.append(datetime.fromisoformat(timestamp.replace("Z", "+00:00")))
                if len(commits) >= max_commits:
                    print(f"Hit max_commits ({max_commits}).")
                    return commits
            except KeyError:
                continue

        print(f"Fetched page {page} ({len(data)} commits)")
        page += 1

    return commits
