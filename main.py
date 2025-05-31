import argparse
import sys
from codetime.github_api import fetch_commits
from codetime.time_estimator import group_commits_into_sessions, estimate_total_time
from codetime.fun_converter import convert_time_to_activities
from codetime.utils import generate_stats_md, generate_config_file, load_config
from codetime.utils import get_user_repos

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

    # Handle --init mode
    if args.init:
        if not args.user or (not args.repo and not args.all):
            print("❌ Error: --init requires at least --user and --repo or --all.")
            return
        generate_config_file(args.user, args.repo, args.mode or "fun", args.all)
        return

    # Load config from file
    config = load_config()
    user = args.user or config.get("user")
    repo = args.repo or config.get("repo")
    mode = args.mode or config.get("mode", "fun")
    
    # Fix: Properly handle the 'all' setting from config
    # CLI --all flag takes precedence, otherwise use config value
    use_all = args.all or config.get("all", False)

    if not user or (not repo and not use_all):
        print("❌ Error: Missing required user/repo. Use CLI args or generate with --init.")
        return

    # Fix: Only show warning and override if both repo AND all are explicitly set via CLI
    if args.repo and args.all:
        print("⚠️ Warning: Both --repo and --all specified via CLI — using --all.")
        use_all = True

    # Determine which repos to analyze
    if use_all:
        repos = get_user_repos(user)
        print(f"Analyzing all {len(repos)} repositories for user {user}")
    else:
        repos = [repo]
        print(f"Analyzing single repository: {repo}")

    all_commits = []

    for repo_name in repos:
        commits = fetch_commits(user, repo_name)
        all_commits.extend(commits)
        print(f"Fetched {len(commits)} commits from {repo_name}.")

    if not all_commits:
        print("⚠️ No commits found. Skipping analysis.")
        return

    sessions = group_commits_into_sessions(all_commits)
    hours_wasted = estimate_total_time(sessions)

    print(f"\nEstimated coding sessions: {sessions}")
    print(f"Total time wasted: {hours_wasted} hours 😅")

    activity_output = convert_time_to_activities(hours_wasted, mode=mode)

    print(f"\nInstead, you could have:")
    for line in activity_output:
        print(line)

    generate_stats_md(user, repos, sessions, hours_wasted, activity_output)

if __name__ == "__main__":
    main()
