from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="football-prediction-system",
    version="0.1.0",
    author="Ming Chen",
    author_email="ming-chen4697@github.com",
    description="A comprehensive football match data analysis and prediction system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ming-chen4697/football-match-prediction",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
        "plotly>=5.0.0",
        "requests>=2.26.0",
    ],
)
