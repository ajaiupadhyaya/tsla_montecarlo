from setuptools import setup, find_packages

setup(
    name="quant_framework",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Core ML & Data Science
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "scipy>=1.7.0",
        
        # Deep Learning
        "torch>=1.9.0",
        "tensorflow>=2.6.0",
        "transformers>=4.11.0",
        
        # Reinforcement Learning
        "gym>=0.21.0",
        "stable-baselines3>=1.5.0",
        
        # Financial Libraries
        "yfinance>=0.1.70",
        "ta-lib>=0.4.24",
        "backtrader>=1.9.76",
        "pyfolio>=0.9.2",
        
        # Feature Engineering
        "tsfresh>=0.17.0",
        "featuretools>=1.0.0",
        "category_encoders>=2.3.0",
        
        # NLP & Text Processing
        "nltk>=3.6.0",
        "vaderSentiment>=3.3.2",
        "finbert-embedding>=0.1.5",
        
        # Data Processing
        "python-dotenv>=0.19.0",
        "pyyaml>=6.0",
        "requests>=2.26.0",
        
        # Testing & Development
        "pytest>=6.2.5",
        "black>=21.9b0",
        "flake8>=3.9.0",
        
        # Documentation
        "sphinx>=4.2.0",
        "mkdocs>=1.2.0",
        
        # Visualization
        "plotly>=5.3.0",
        "seaborn>=0.11.0",
        "matplotlib>=3.4.0",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
            "mypy",
            "pre-commit",
        ],
        "docs": [
            "sphinx",
            "mkdocs",
            "mkdocs-material",
        ],
    },
    python_requires=">=3.8",
    author="Quantitative Finance Team",
    author_email="team@example.com",
    description="A comprehensive quantitative finance framework for research and trading",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quant_framework",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
) 