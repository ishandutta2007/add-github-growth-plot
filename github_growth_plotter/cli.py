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
    
    vintage_fonts = 'Georgia'
    cursive_fonts = 'Segoe Script'
    
    plt.title("Star history", fontfamily=vintage_fonts, fontsize=16)
    
    if len(dates) > 1:
        time_span = dates[-1] - dates[0]
        span_days = time_span.days
    else:
        span_days = 0
        
    if span_days >= 365:
        xlabel_text = "Years"
        fmt = "%Y"
    elif span_days >= 30:
        xlabel_text = "Months"
        fmt = "%b %Y"
    elif span_days >= 7:
        xlabel_text = "Weeks"
        fmt = "Week %W, %Y"
    else:
        xlabel_text = "Day with month"
        fmt = "%b %d"
        
    plt.xlabel(xlabel_text, fontfamily=cursive_fonts, fontsize=12)
    plt.ylabel("Github Stars", fontfamily=cursive_fonts, fontsize=12)
    
    # Format the x-axis to show dates nicely
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(fmt))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()
    
    # Set font for tick labels
    for label in plt.gca().get_xticklabels() + plt.gca().get_yticklabels():
        label.set_fontfamily(cursive_fonts)
    
    # Add repo name to top left (which is usually empty in cumulative growth plots)
    plt.text(0.05, 0.95, repo, transform=plt.gca().transAxes, 
             fontsize=14, fontfamily=cursive_fonts, 
             verticalalignment='top', horizontalalignment='left',
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    print(f"Saved growth plot to {filename}")

def update_gitignore(filename):
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r', encoding='utf-8') as f:
            content = f.read()
            if filename in content.splitlines():
                return
        with open('.gitignore', 'a', encoding='utf-8') as f:
            if content and not content.endswith('\n'):
                f.write('\n')
            f.write(f"{filename}\n")
    else:
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(f"{filename}\n")
    print(f"Added {filename} to .gitignore")

def publish_to_readme(plot_filename, repo):
    readme_path = "README.md"
    basename = os.path.basename(plot_filename)
    img_path = f"./assets/{basename}"
    
    html_snippet = f'\n<p align="center">\n  <img src="{img_path}" alt="{repo}" width="100%" />\n</p>\n'
    
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if basename not in content:
            with open(readme_path, 'a', encoding='utf-8') as f:
                if content and not content.endswith('\n'):
                    f.write('\n')
                f.write(html_snippet)
            print(f"Published plot to {readme_path}")
        else:
            print(f"Plot already seems to be published in {readme_path}")
    else:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(html_snippet.lstrip())
        print(f"Created {readme_path} and published plot")

def main():
    parser = argparse.ArgumentParser(description="Fetch stargazers and plot growth.")
    parser.add_argument("repo", nargs="?", help="GitHub repository in owner/repo format. If not provided, uses the current repository.")
    parser.add_argument("--publish", action="store_true", help="Auto publish the plot to the current README.md")
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
    
    os.makedirs("assets", exist_ok=True)
    plot_filename = os.path.join("assets", f"{safe_repo_name}_growth.svg")
    
    save_to_csv(stargazers, csv_filename)
    update_gitignore(csv_filename)
    plot_growth(stargazers, plot_filename, repo)
    
    if args.publish:
        publish_to_readme(plot_filename, repo)

if __name__ == "__main__":
    main()
