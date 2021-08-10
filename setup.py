from setuptools import setup

with open("./README.md", "r") as f:
    readme = f.read()

setup(
    name="create-a-cli",
    version="0.0.1",
    description="Create command line interfaces using Python",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Dorukyum",
    url="https://github.com/Dorukyum/create-a-cli",
    packages=["cli"],
    keywords="cli",
    project_urls={"Source": "https://github.com/Dorukyum/create-a-cli"},
    python_requires=">=3",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
)
