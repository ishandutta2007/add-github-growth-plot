# Contributing to GitHub Stargazers Growth Plotter

Thank you for your interest in contributing to **GitHub Stargazers Growth Plotter**! This guide will help you understand the project structure, how to set up your development environment, and the guidelines for submitting your changes.

---

## 🛠️ Development Setup

The project is built as a standard Python package using `setuptools`.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ishandutta2007/add-github-growth-plot.git
   cd add-github-growth-plot
   ```

2. **Install locally in editable mode:**
   ```bash
   pip install -e .
   ```
   This will install the package alongside its dependencies (`requests`, `matplotlib`) and link the `github-growth-plot` command directly to your local source code. Any changes you make to `github_growth_plotter/cli.py` will be immediately reflected when you run the command.

3. **Install Build Tools (Optional, for publishing):**
   ```bash
   pip install build twine
   ```

## 📋 Contribution Guidelines

1. **Bug Reports & Feature Requests:**
   * Please check the existing issues to ensure it hasn't already been reported.
   * Clearly describe the issue or feature, and provide context or steps to reproduce if applicable.

2. **Submitting Pull Requests:**
   * Branch off from the primary branch.
   * Keep your commits focused and descriptive (e.g., `feat: add support for enterprise github`, `fix: correct svg scaling`).
   * Test your changes thoroughly by running `github-growth-plot` locally on a sample repository before submitting.
   * Push your branch and open a Pull Request!

---

## 🌐 SaaS Products Pricing Info

This project relies on the GitHub API to fetch historical stargazer data. Refer to the pricing details and free tier limits below:

| SaaS Product | Pricing Model | Free Tier Details / Limits |
| :--- | :--- | :--- |
| **GitHub API** | Freemium | Free for public/private repositories. Unauthenticated API: 60 requests/hr. Authenticated API (which this tool uses natively via the `gh` CLI): 5,000 requests/hr. |
