import setuptools

setuptools.setup(
    name="sunflower",
    version="0.1.0",
    packages=setuptools.find_packages(),
    install_requires=(
        "selenium>=3.141.0",
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "peewee>=3.14.4",
        "click>=8.0.1",
    ),
    entry_points={
        "console_scripts": ["sunflower=sunflower.cli.core:main"]
    },
)
