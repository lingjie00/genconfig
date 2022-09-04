"""Setup."""
import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setuptools.setup(
    name="configen",
    user_scm_version=True,
    author="Ling",
    author_email="lingjie@u.nus.edu",
    description="Manage Json and Yaml config using folder structure",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/lingjie00/configen",
    project_urls={"Bug Tracker": "https://github.com/lingjie00/configen/issues"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "configen"},
    packages=setuptools.find_packages(where="configen"),
    python_requires=">=3.8",
    setup_requires=["setuptools_scm"],
    install_requires=required,
    license="MIT",
)
