from setuptools import setup, find_packages

setup(
    name="Wastons Products Info Scraper",
    version="0.1",
    author="Anthony Sung",
    author_email="xiaolong70701@gmail.com",
    description="A web scraper for Watsons Taiwan products",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xiaolong70701/wastons",
    packages=find_packages(),
    install_requires=[
        "selenium-wire",
        "requests",
        "tqdm"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
