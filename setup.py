try:
    from setuptools import setup;
except ImportError:
    from distutils.core import setup;

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read();

setup(
    name="ventoy_updater",
    version="0.2",
    author="Marcel-Brian Wilkowsky",
    author_email="marcel.wilkowsky@hotmail.de",
    description="Manage and update ISO files on Ventoy devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mawigh/ventoy_updater",
    project_urls={
        "Bug Tracker": "https://github.com/mawigh/ventoy_updater/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0",
        "Operating System :: Linux",
    ],
    scripts=["bin/ventoyu"],
)
