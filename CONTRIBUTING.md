# Contributing to GitHub Stargazers Growth Plotter

Thank you for your interest in contributing to **GitHub Stargazers Growth Plotter**!

This documentation is divided into distinct sections tailored to your role:
- [👤 End Users](#-end-users)
- [👩‍💻 Developers & Contributors](#-developers--contributors)
- [🚀 Package Publishers & DevOps](#-package-publishers--devops)

---

## 👤 End Users

End users can install and execute the CLI tool directly.

```bash
pip install github-growth-plotter
github-growth-plot --publish
```

For full usage commands, see the **[README.md](file:///C:/Users/ishan/Documents/Projects/add-github-growth-plot/README.md#-end-users-guide)**.

---

## 👩‍💻 Developers & Contributors

### 🛠️ Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ishandutta2007/add-github-growth-plot.git
   cd add-github-growth-plot
   ```

2. **Install in editable mode:**
   ```bash
   pip install -e .
   ```
   This links the CLI `github-growth-plot` directly to your local codebase in `github_growth_plotter/cli.py`.

3. **Install Build & Testing Tools:**
   ```bash
   pip install build twine
   ```

### 📋 Pull Request Workflow

1. Create a feature branch off `main`.
2. Follow clear commit messages (`feat: ...`, `fix: ...`).
3. If changing package metadata or adding dependencies, update both `pyproject.toml` and `setup.py`.
4. Run `github-growth-plot` locally to verify changes before submitting your PR.

---

## 🚀 Package Publishers & DevOps

### 📦 Automated PyPI Auto-Publishing

Automated publishing is powered by GitHub Actions ([`.github/workflows/publish-pypi.yml`](file:///C:/Users/ishan/Documents/Projects/add-github-growth-plot/.github/workflows/publish-pypi.yml)).

#### Triggering Auto-Publish on PyPI:
- **Version Bump in TOML / Setup**:
  Whenever you increment the version in `pyproject.toml` (or any `*.toml` / `setup.py` / `__init__.py`) and push to `main`, GitHub Actions will build the package and publish it to PyPI automatically.
- **Git Tag Push**:
  Pushing a tag such as `git push origin v0.1.2` also triggers automatic PyPI deployment.

#### Required Repository Configuration:
1. Ensure `PYPI_API_TOKEN` is present in GitHub Secrets (**Settings > Secrets and variables > Actions**).
2. If pushing workflow changes via PAT, verify your PAT has the **`workflow`** permission scope enabled.

---

## 🌐 SaaS Products & Pricing Info

| SaaS Product | Pricing Model | Free Tier Details / Limits |
| :--- | :--- | :--- |
| **GitHub API** | Freemium | Free for public/private repositories. Unauthenticated API: 60 requests/hr. Authenticated API (`gh` CLI): 5,000 requests/hr. |
| **GitHub Actions** | Freemium | 2,000 free build minutes/month for standard public/private repository accounts. |
| **PyPI (Python Package Index)** | Free | Free package hosting and distribution. |
