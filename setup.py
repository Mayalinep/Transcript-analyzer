from setuptools import setup, find_packages

def read_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

base_requirements = [
    "openai-whisper>=20231117",
    "yt-dlp>=2023.12.30",
    "ffmpeg-python>=0.2.0",
    "typing-extensions>=4.9.0",
    "numpy>=1.26.0",
    "torch>=2.1.0",
    "tqdm>=4.66.0",
    "transformers>=4.37.0",
    "sentencepiece>=0.1.99",
    "accelerate>=0.27.0"
]

setup(
    name="transcript-analyzer",
    version="1.0.0",
    description="Analyseur de transcriptions avec génération de documentation Markdown",
    author="Maya",
    author_email="maya@example.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=base_requirements,
    extras_require={
        "openai": ["openai>=1.0.0"],
        "dev": read_requirements("requirements/dev.txt"),
        "all": read_requirements("requirements/optional.txt")
    },
    entry_points={
        "console_scripts": [
            "analyze-transcript=src.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: Free for non-commercial use",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
) 