<div align="center">
  <img src="./assets/banner.svg" alt="GitHub Stargazers Growth Plotter Banner" width="100%">
</div>

# 📈 GitHub Stargazers Growth Plotter

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![GitHub CLI](https://img.shields.io/badge/GitHub%20CLI-Required-black?style=for-the-badge&logo=github&logoColor=white)](https://cli.github.com/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Supported-orange?style=for-the-badge)](https://matplotlib.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

> **Note:** As the stargazers API for 3rd party repos gets deprecated or restricted, repository owners can use this tool to easily fetch and publish their own repository's growth charts!

🚀 **GitHub Stargazers Growth Plotter** is an automated tool that fetches the stargazers history of any GitHub repository, caches it locally, and generates a stunning SVG growth plot. Designed for repository owners, this script can auto-publish charts directly to your `README.md` for maximum visibility and better SEO indexing of project metrics.

## ✨ Features

- 🔐 **Automated Authentication**: Seamlessly integrates with your active GitHub CLI (`gh`) token. Zero manual token configuration required!
- 🎯 **Zero-Config Context**: Automatically detects your current repository from your git config if run without arguments.
- 🗄️ **Local Caching**: Caches historical stargazer data in a CSV file and dynamically appends it to your `.gitignore` to prevent accidental commits.
- 📊 **High-Quality Plotting**: Renders beautiful, scalable vector `.svg` plots optimized for web display, saving them cleanly in an `assets/` directory.
- 📝 **Auto-Publishing**: With a simple flag, automatically inject your latest growth chart into your `README.md` within a perfectly centered HTML block.

## 🛠️ Prerequisites

1. **Python 3.x**: Ensure Python is installed on your system.
2. **GitHub CLI (`gh`)**: You must have the GitHub CLI installed and authenticated.
   ```bash
   gh auth login
   ```
3. **Installation**:
   Install the tool via PyPI:
   ```bash
   pip install github-growth-plotter
   ```
   *(To install from source locally, clone the repo and run `pip install .`)*

## 🚀 Usage Guide

### 1️⃣ Run for the current repository
If you are already inside a Git repository folder, you can simply run:
```bash
github-growth-plot
```
This detects the repository, downloads the stargazers to a CSV, and outputs the SVG plot in the `assets/` directory.

### 2️⃣ Run for a specific repository
You can specify any repository using the standard `owner/repo` format:
```bash
github-growth-plot "google/jax"
```

### 3️⃣ Auto-publish to README
Want to display the chart on your project's main page? Pass the `--publish` flag:
```bash
github-growth-plot --publish
```
This automatically appends the following HTML snippet to the bottom of your `README.md`:
```html
<p align="center">
  <img src="./assets/<username>_<reponame>_growth.svg" alt="<owner>/<repo>" width="100%" />
</p>
```

## 📂 Generated Files

When executed, the script generates and manages the following files:
- 🖼️ **`assets/<username>_<reponame>_growth.svg`**: The generated vector graph showing star growth over time.
- 📄 **`<username>_<reponame>_stargazers.csv`**: Raw historical star data (automatically ignored via `.gitignore`).
- 🙈 **`.gitignore`**: Updated automatically to ignore the generated CSV file.

---
*Made with ❤️ for Open Source Maintainers.*

