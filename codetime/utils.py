import yaml
import os
import requests

def generate_stats_md(username, repos, session_count, total_hours, alt_activities):
    with open("STATS.md", "w") as f:
        f.write("# 📊 CodeTime Waster Report\n\n")
        f.write(f"**User**: `{username}`\n")
        f.write(f"**Repos analyzed**: {', '.join(repos) if repos else 'N/A'}`\n\n")
        f.write(f"**Estimated coding sessions**: `{session_count}`\n")
        f.write(f"**Total time wasted**: `{total_hours} hours` 😅\n\n")
        f.write("## 🌀 Instead, you could have:\n\n")
        for item in alt_activities:
            f.write(f"{item}\n")

def generate_config_file(user, repo, mode="fun", use_all=False, include_forks=False):
    config = {
        "user": user,
        "repo": repo,
        "mode": mode,
        "all": use_all,
        "include_forks": include_forks
    }
    with open("codetime.config.yml", "w") as f:
        yaml.dump(config, f)
    print("✅ Config file saved to codetime.config.yml")

def load_config():
    config_path = "codetime.config.yml"
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_user_repos(user, include_forks=False):
    """Fetch all public repos for the given GitHub user."""
    repos = []
    page = 1
    per_page = 100
    while True:
        url = f"https://api.github.com/users/{user}/repos"
        params = {"per_page": per_page, "page": page}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"⚠️ Failed to fetch repos for user {user} (HTTP {response.status_code})")
            break
        data = response.json()
        if not data:
            break
        
        for repo in data:
            # Skip forks unless explicitly requested
            if repo["fork"] and not include_forks:
                continue
            repos.append(repo["name"])
            
        if len(data) < per_page:
            break
        page += 1
    
    if not include_forks:
        print(f"Found {len(repos)} non-fork repositories (forks excluded)")
    else:
        print(f"Found {len(repos)} repositories (including forks)")
    
    return repos
