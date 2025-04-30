#!/usr/bin/env python3

import argparse
import json
import os
import random
import sys
import requests
import yaml
from datetime import datetime, timedelta

# ========== GitHub API ==========

def get_user_repos(user):
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
        repos.extend([repo["name"] for repo in data])
        if len(data) < per_page:
            break
        page += 1
    return repos

def fetch_commits(user, repo, per_page=100):
    commits = []
    page = 1
    max_pages = 20
    max_commits = 2000

    while True:
        if page > max_pages or len(commits) >= max_commits:
            break

        url = f"https://api.github.com/repos/{user}/{repo}/commits"
        response = requests.get(url, params={"per_page": per_page, "page": page})

        if response.status_code != 200:
            print(f"Failed to fetch page {page} - Status code: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        for commit in data:
            try:
                timestamp = commit["commit"]["committer"]["date"]
                commits.append(datetime.fromisoformat(timestamp.replace("Z", "+00:00")))
            except KeyError:
                continue

            if len(commits) >= max_commits:
                break

        page += 1

    return commits

# ========== Time Estimator ==========

def group_commits_into_sessions(timestamps, session_gap_minutes=60):
    if not timestamps:
        return 0

    timestamps.sort()
    session_count = 1
    last_time = timestamps[0]

    for current_time in timestamps[1:]:
        gap = current_time - last_time
        if gap > timedelta(minutes=session_gap_minutes):
            session_count += 1
        last_time = current_time

    return session_count

def estimate_total_time(session_count, avg_minutes_per_session=30):
    total_minutes = session_count * avg_minutes_per_session
    return round(total_minutes / 60, 2)

# ========== Fun Converter ==========

def load_activities(mode="fun"):
    path = f"data/activities_{mode}.json"
    if not os.path.exists(path):
        print(f"⚠️ Activity file not found for mode: {mode}")
        return []
    with open(path, "r") as f:
        return json.load(f)

def convert_time_to_activities(total_hours, activity_count=10, mode="fun"):
    activities = load_activities(mode)
    random.shuffle(activities)
    results = []
    used_activities = set()

    for item in activities:
        if item["activity"] in used_activities:
            continue

        units = int(total_hours // item["hours"])
        if units > 0:
            results.append(f"- {item['activity'].capitalize()} {units} times")
            used_activities.add(item["activity"])

        if len(results) >= activity_count:
            break

    return results

# ========== Config Helpers ==========

def generate_config_file(user, repo, mode="fun", use_all=False):
    config = {"user": user, "repo": repo, "mode": mode, "all": use_all}
    with open("codetime.config.yml", "w") as f:
        yaml.dump(config, f)
    print("✅ Config file saved to codetime.config.yml")

def load_config():
    try:
        with open("codetime.config.yml", "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}

# ========== Markdown Writer ==========

def generate_stats_md(username, repos, session_count, total_hours, alt_activities):
    with open("STATS.md", "w") as f:
        f.write("# 📊 CodeTime Waster Report\n\n")
        f.write(f"**User**: `{username}`  ")
        f.write(f"Repos analyzed: {', '.join(repos) if repos else 'N/A'}\n\n")
        f.write(f"**Estimated coding sessions**: `{session_count}`  ")
        f.write(f"Total time wasted: `{total_hours} hours` 😅\n\n")
        f.write("## 🌀 Instead, you could have:\n\n")
        for item in alt_activities:
            f.write(f"{item}\n")

# ========== CLI ==========

def parse_args():
    parser = argparse.ArgumentParser(description="CodeTime Waster - Estimate your wasted GitHub time")
    parser.add_argument("--user", help="GitHub username (fallbacks to config file)")
    parser.add_argument("--repo", help="GitHub repo name (required unless --all is used)")
    parser.add_argument("--all", action="store_true", help="Analyze all public repos")
    parser.add_argument("--mode", choices=["fun", "guilty", "inspirational", "corporate"], default="fun",
                        help="Output tone (default: fun)")
    parser.add_argument("--init", action="store_true", help="Create a codetime.config.yml from CLI args")

    try:
        return parser.parse_args()
    except SystemExit:
        print("\nInvalid arguments. Use '--help' for usage information.")
        sys.exit(0)

def main():
    args = parse_args()

    if args.init:
        if not args.user or (not args.repo and not args.all):
            print("❌ Error: --init requires at least --user and --repo or --all.")
            return
        generate_config_file(args.user, args.repo, args.mode or "fun", args.all)
        return

    config = load_config()
    user = args.user or config.get("user")
    repo = args.repo or config.get("repo")
    mode = args.mode or config.get("mode", "fun")
    use_all = args.all or (config.get("all", False) if not repo else False)

    if not user or (not repo and not use_all):
        print("❌ Error: Missing required user/repo. Use CLI args or generate with --init.")
        return

    if repo and use_all:
        print("⚠️ Warning: `repo` is specified — ignoring `all: true` and using only that repo.")

    repos = [repo] if repo else get_user_repos(user)

    all_commits = []

    for repo in repos:
        commits = fetch_commits(user, repo)
        all_commits.extend(commits)
        print(f"Fetched {len(commits)} commits from {repo}.")

    if not all_commits:
        print("⚠️ No commits found. Skipping analysis.")
        return

    sessions = group_commits_into_sessions(all_commits)
    hours_wasted = estimate_total_time(sessions)

    print(f"\nEstimated coding sessions: {sessions}")
    print(f"Total time wasted: {hours_wasted} hours 😅\n")

    activity_output = convert_time_to_activities(hours_wasted, mode=mode)
    print("Instead, you could have:")
    for line in activity_output:
        print(line)

    generate_stats_md(user, repos, sessions, hours_wasted, activity_output)

if __name__ == "__main__":
    main()
