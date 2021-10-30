try:
    from setuptools import setup, find_packages;
except ImportError:
    from distutils.core import setup;

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read();

setup(
    name="ventoyu",
    version="0.3",
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
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Unix",
    ],
    include_package_data=True,
    scripts=["bin/ventoyu"],
    install_requires=["beautifulsoup4", "requests"],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)
