from setuptools import setup, find_packages
setup(
    name="deeprobot",
    version="0.1a",
    packages=find_packages(),
    scripts=["main.py"],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=["docutils>=0.3"],

    # package_data={
    #     # If any package contains *.txt or *.rst files, include them:
    #     "": ["*.txt", "*.rst"],
    #     # And include any *.msg files found in the "hello" package, too:
    #     "hello": ["*.msg"],
    # },

    # metadata to display on PyPI
    author="dkluffy",
    author_email="dkluffy@gmail.com",
    description="This is an deeprobot Package",
    keywords="hello world example examples",
    url="https://github.com/dkluffy/Gamescripts",   # project home page, if any
    project_urls={
        "Bug Tracker": "https://github.com/dkluffy/Gamescripts",
        "Documentation": "https://github.com/dkluffy/Gamescripts",
        "Source Code": "https://github.com/dkluffy/Gamescripts",
    },
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ]

    # could also include long_description, download_url, etc.
)