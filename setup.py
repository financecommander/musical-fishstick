"""
EdgeForge: Production-Grade Edge Deployment DSL for ML Models
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="edgeforge",
    version="0.1.0",
    author="Calculus Holdings LLC",
    author_email="sean@calculusholdings.com",
    description="Python-embedded DSL for ultra-efficient edge deployment of ML models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/financecommander/musical-fishstick",
    packages=find_packages(exclude=["tests", "examples", "docs"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "torch>=2.1.0",
        "onnx>=1.15.0",
        "onnxruntime>=1.16.0",
        "numpy>=1.24.0",
        "tqdm>=4.65.0",
        "pyyaml>=6.0",
        "click>=8.1.0",
        "psutil>=5.9.0",
        "py-cpuinfo>=9.0.0",
    ],
    extras_require={
        "gpu": [
            "onnxruntime-gpu>=1.16.0",
            "nvidia-ml-py3>=7.352.0",
        ],
        "tensorrt": [
            "tensorrt>=8.6.0",
        ],
        "tflite": [
            "tensorflow-lite>=2.14.0",
        ],
        "coreml": [
            "coremltools>=7.0",
        ],
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
            "flake8>=6.1.0",
        ],
        "all": [
            "onnxruntime-gpu>=1.16.0",
            "tensorrt>=8.6.0",
            "tensorflow-lite>=2.14.0",
            "coremltools>=7.0",
            "nvidia-ml-py3>=7.352.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "edgeforge=edgeforge.cli:main",
        ],
    },
)
