"""
Setup script for the Automated Daily Poster Bot package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "docs" / "README.md"
long_description = ""
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="autopost",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Automated Daily Poster Bot with intelligent scheduling and multiple content sources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/autopost",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "autopost=autopost.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "autopost": ["*.txt", "*.md"],
    },
    keywords="automation, social-media, posting, bot, scheduling",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/autopost/issues",
        "Source": "https://github.com/yourusername/autopost",
        "Documentation": "https://github.com/yourusername/autopost/blob/main/docs/README.md",
    },
) 