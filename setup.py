from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="github-growth-plotter",
    version="0.1.0",
    author="Open Source Maintainers",
    description="A tool to fetch GitHub stargazers and plot growth over time.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "requests",
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
            "github-growth-plot=github_growth_plotter.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
