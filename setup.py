from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="uipath-community-sdk",
    version="1.1.0",
    author="Christian Blandford",
    author_email="christianblandford@me.com",
    description="A community-maintained Python SDK for UiPath",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/christianblandford/uipath-community-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=[
        "uipath",
        "uipath-community-sdk",
        "rpa",
        "robotic process automation",
        "automation",
        "robotics",
        "orchestrator",
        "process-automation",
        "api-client",
        "api-wrapper",
        "uipath-api",
        "uipath-orchestrator",
        "workflow-automation",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "mkdocs-material",
            "mkdocs-autorefs",
            "mkdocstrings[python]",
        ],
    },
)
