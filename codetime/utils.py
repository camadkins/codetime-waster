import yaml
import os

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

def generate_config_file(user, repo, mode="fun", use_all=False):
    config = {
        "user": user,
        "repo": repo,
        "mode": mode,
        "all": use_all
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
