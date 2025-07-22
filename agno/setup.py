from setuptools import setup, find_packages

setup(
    name="test_agno",
    version="0.1.0",
    description="Test library for Agno framework",
    author="Robert Tartarotti",
    author_email="robert.tartarotti@gmail.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "agno",
        "openai",
        "common",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "ruff",
            "mypy",
            "pre-commit",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 