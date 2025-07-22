from setuptools import setup, find_packages

setup(
    name="common",
    version="0.1.0",
    description="Common library for AI agent frameworks testing",
    author="Robert Tartarotti",
    author_email="robert.tartarotti@gmail.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "datetime",
        "pymongo",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "ruff",
            "mypy",
            "pre-commit",
            "sphinx",
            "sphinx-rtd-theme",
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