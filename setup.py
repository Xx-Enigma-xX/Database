import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EDMC-hillcrestpaul0719",
    version="0.2",
    author="Kyunghan (Paul) Lee",
    author_email="enigma@enigmatic.network",
    description="Enigma Database Managing Class",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/enigmatic-network/Database",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Database"
    ],
)
