# GitHub Stargazers Growth Plotter

> **Note:** As the stargazers API for 3rd party repos gets deprecated or restricted, repository owners can use this tool to easily fetch and publish their own repository's growth charts!

This tool automatically fetches the stargazers history of a GitHub repository using your active GitHub token, caches it locally as a CSV, and generates a clean SVG growth plot over time. It can even automatically append and publish the chart directly to your repository's `README.md`.

## Features

- **Automated Authentication**: Seamlessly uses your active GitHub CLI (`gh`) token. No manual token configuration required!
- **Zero-Config Context**: Automatically detects your current repository from your git config if run without arguments.
- **Local Caching**: Saves historical stargazer data to a CSV and automatically appends that filename to your `.gitignore` to prevent accidental commits.
- **High-Quality Plotting**: Generates a scalable vector `.svg` plot and saves it cleanly in a local `assets/` directory.
- **Auto-Publishing**: Optionally append the newly generated plot directly to your `README.md` within a centered HTML block.

## Prerequisites

1. **Python 3.x**
2. **GitHub CLI (`gh`)**: You must have the GitHub CLI installed and authenticated.
   ```bash
   gh auth login
   ```
3. **Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(This will install `requests` and `matplotlib`)*

## Usage

### 1. Run for the current repository
If you are already inside a Git repository folder, you can simply run:
```bash
python plot_stargazers.py
```
This will detect the repository, download the stargazers to a CSV, and output the SVG plot in the `assets/` directory.

### 2. Run for a specific repository
You can optionally specify any repository using the standard `owner/repo` format:
```bash
python plot_stargazers.py "google/jax"
```

### 3. Auto-publish to README
Want to display the chart on your project's main page? Pass the `--publish` flag:
```bash
python plot_stargazers.py --publish
```
This will append the following HTML snippet to the bottom of your `README.md`:
```html
<p align="center">
  <img src="./assets/<username>_<reponame>_growth.svg" alt="<owner>/<repo>" width="100%" />
</p>
```

## Generated Files

When executed, the script generates and manages the following files:
- **`assets/<username>_<reponame>_growth.svg`**: The generated vector graph showing star growth over time.
- **`<username>_<reponame>_stargazers.csv`**: Raw historical star data (automatically ignored via `.gitignore`).
- **`.gitignore`**: Updated automatically to ignore the generated CSV file.
