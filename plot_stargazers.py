import argparse
import subprocess
import requests
import csv
import os
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_github_token():
    try:
        result = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("Error: Could not retrieve GitHub token. Ensure you are logged in using 'gh auth login'.")
        sys.exit(1)
    except FileNotFoundError:
         # Fallback to env var if gh not found
         token = os.environ.get("GITHUB_TOKEN")
         if not token:
             print("Error: 'gh' CLI not found and GITHUB_TOKEN environment variable not set.")
             sys.exit(1)
         return token

def get_current_repo():
    try:
        # First try using gh CLI
        result = subprocess.run(['gh', 'repo', 'view', '--json', 'nameWithOwner', '--jq', '.nameWithOwner'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        try:
             # Fallback to git remote parsing
             result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True, check=True)
             url = result.stdout.strip()
             # Extract owner/repo from url
             if url.startswith("git@github.com:"):
                 return url[15:].replace('.git', '')
             elif url.startswith("https://github.com/"):
                 return url[19:].replace('.git', '')
             else:
                 print("Error: Could not determine current repository from git remote.")
                 sys.exit(1)
        except Exception as e:
             print("Error: Could not determine current repository. Are you in a git repository?")
             sys.exit(1)
    except FileNotFoundError:
        print("Error: Required command line tool 'gh' or 'git' not found.")
        sys.exit(1)

def fetch_stargazers(repo, token):
    url = f"https://api.github.com/repos/{repo}/stargazers"
    headers = {
        "Accept": "application/vnd.github.v3.star+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    stargazers = []
    page = 1
    per_page = 100
    
    print(f"Fetching stargazers for {repo}...")
    while True:
        params = {"page": page, "per_page": per_page}
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching stargazers: {response.status_code} {response.text}")
            sys.exit(1)
            
        data = response.json()
        if not data:
            break
            
        for item in data:
            stargazers.append({
                "user": item["user"]["login"],
                "starred_at": item["starred_at"]
            })
            
        if "next" not in response.links:
            break
        page += 1
        
    return stargazers

def save_to_csv(stargazers, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["user", "starred_at"])
        writer.writeheader()
        for stargazer in stargazers:
            writer.writerow(stargazer)
    print(f"Saved {len(stargazers)} stargazers to {filename}")

def plot_growth(stargazers, filename, repo):
    dates = [datetime.strptime(s["starred_at"], "%Y-%m-%dT%H:%M:%SZ") for s in stargazers]
    dates.sort()
    
    counts = list(range(1, len(dates) + 1))
    
    plt.figure(figsize=(10, 6))
    plt.plot(dates, counts, marker='', linestyle='-', color='b')
    
    plt.title(f"Stargazers Growth for {repo}")
    plt.xlabel("Date")
    plt.ylabel("Number of Stargazers")
    
    # Format the x-axis to show dates nicely
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()
    
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    print(f"Saved growth plot to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Fetch stargazers and plot growth.")
    parser.add_argument("repo", nargs="?", help="GitHub repository in owner/repo format. If not provided, uses the current repository.")
    args = parser.parse_args()
    
    repo = args.repo
    if not repo:
        repo = get_current_repo()
        
    token = get_github_token()
    
    stargazers = fetch_stargazers(repo, token)
    
    if not stargazers:
        print("No stargazers found or repository does not exist.")
        sys.exit(0)
        
    safe_repo_name = repo.replace('/', '_')
    csv_filename = f"{safe_repo_name}_stargazers.csv"
    plot_filename = f"{safe_repo_name}_growth.png"
    
    save_to_csv(stargazers, csv_filename)
    plot_growth(stargazers, plot_filename, repo)

if __name__ == "__main__":
    main()
