# ⏳ CodeTime Waster

**Estimate how much time you've "wasted" writing code on GitHub — and what else you could have done with that time.** Automatically generates a fun (or guilty!) `STATS.md` report based on your commit activity.

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/camadkins/codetime-waster/generate-stats.yml?label=GitHub%20Actions&style=flat-square)

---

## Features

-  Smart session estimation from GitHub commit history
-  Weekly GitHub Action that updates `STATS.md`
-  Modes: `fun`, `guilty`, `inspirational`, and `corporate`
-  CLI version available for local use
-  GitHub template — easily clone and personalize

---

##  Quick Start

You have **three options** to get started depending on your preference:

---

###  Option 1: Run Locally via CLI

Clone your version of the template:

```bash
git clone https://github.com/camadkins/codetime-waster.git
cd codetime-waster
```

Run the CLI tool:

```bash
python cli/codetime_waster.py --user yourgithub --repo yourrepo --mode fun
```

---

###  Option 2: Local Config + GitHub Actions

1. Generate a config file:

   ```bash
   python cli/codetime_waster.py --init --user yourgithub --repo yourrepo --mode guilty
   ```

2. Commit it:

   ```bash
   git add codetime.config.yml
   git commit -m "Add my config"
   git push
   ```

3. Go to GitHub → Actions → Manually run the job

---

###  Option 3: GitHub-Only Setup (No Download)

1. Click **"Use this template"** (top of the repo)
2. In your new repo:
   - Add or edit `codetime.config.yml` in the GitHub UI:

     ```yaml
     user: yourgithub
     repo: yourrepo
     mode: fun
     all: false
     ```

3. Commit the change to `main`
4. Go to **Actions** → Run the job
5. `STATS.md` will be generated and pushed automatically every Sunday 🎉

---

##  How GitHub Action Works

This repo includes a pre-configured GitHub Action that:

- Runs every **Sunday at midnight UTC**
- Executes the `main.py` script
- Reads `codetime.config.yml`
- Regenerates and commits your personalized `STATS.md`

No maintenance needed.

---

##  Sample Output

Here’s what your `STATS.md` might look like:

```markdown
# 📊 CodeTime Waster Report

**User**: `camadkins`  
**Repos analyzed**: `codetime-waster`

**Estimated coding sessions**: `42`  
**Total time wasted**: `21.0 hours` 😅

## 🌀 Instead, you could have:

- Cooked 42 healthy meals
- Hit the gym 21 times
- Watched 10 full baseball games
```

---

##  Download CLI Version

Want to run it without cloning the whole repo? [Download codetime_waster.py](cli/codetime_waster.py)  
Just run:

```bash
python codetime_waster.py --user yourname --repo yourrepo
```

---

###  CLI Usage

```bash
python cli/codetime_waster.py --user yourgithub --repo yourrepo --mode fun
```

#### Arguments

- `--user`: **Required**: Your GitHub username.
- `--repo`: **Optional**: The specific GitHub repo to analyze. If not provided, and `--all` is not used, the program will not know which repo to analyze.
- `--all`: **Optional**: If this flag is used, the program will analyze **all public repositories** of the specified user.
- `--mode`: **Optional**: Choose the tone of the output. Available options:
  - `fun`: Default, provides lighthearted alternatives for your wasted time.
  - `guilty`: Gives you a more guilty perspective of how you could have used that time.
  - `inspirational`: Offers motivational alternatives to your wasted time.
  - `corporate`: Provides a corporate-like perspective (e.g., meetings, emails).
- `--init`: **Optional**: Creates a `codetime.config.yml` file based on your input.
- `--token`: **Optional**: (Future feature) GitHub Personal Access Token (PAT) to increase the API rate limit (not implemented yet).
  
---

### **Example Commands**

```bash
# Analyze one specific repo (default mode is 'fun')
python cli/codetime_waster.py --user yourgithub --repo yourrepo

# Analyze all repos for the user
python cli/codetime_waster.py --user yourgithub --all

# Use the 'guilty' mode
python cli/codetime_waster.py --user yourgithub --repo yourrepo --mode guilty
```

---

##  How It Works

- Fetches your commit timestamps via GitHub's API
- Groups them into "sessions" based on gaps
- Multiplies session count by average time (30 minutes)
- Shows you what else you could’ve done in that time 😅

---

##  API Rate Limits

GitHub's API has a **rate limit** that restricts the number of requests you can make:

- **Unauthenticated users**: 60 requests per hour
- **Authenticated users**: 5000 requests per hour (using a Personal Access Token)

### What this means for you

- If you're only analyzing a few repos at a time, the limit will likely not be an issue.
- If you're analyzing **many repos** (especially in the `--all` mode), you may hit the rate limit after several requests.

You can always wait for the limit to reset, or consider **reducing the number of repos** you're analyzing to avoid hitting the limit.

---

##  Requirements

- Python 3.9+
- `requests`, `pyyaml`

Install with:

```bash
pip install -r requirements.txt
```

---

##  Contributing & License

Contributions welcome! Fork it, build your twist, and tag me.

MIT License • Made with 💻 by [camadkins](https://github.com/camadkins)

##  Support the Project

If you enjoyed this project and want me to keep making more programs, consider buying me a coffee! ☕️

[Buy me a coffee on Ko-Fi](https://ko-fi.com/camadkins)

Every little bit helps, and I really appreciate it! 🙏
