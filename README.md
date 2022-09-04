# configen

[![package](https://github.com/lingjie00/configen/actions/workflows/project-actions.yml/badge.svg)](https://github.com/lingjie00/configen/actions/workflows/project-actions.yml)

# Project overview

Manage Json and Yaml config using folder structure.

The API documentation is available at
[https://lingjie00.github.io/configen/](https://lingjie00.github.io/configen/)

# Folder structure

- [docs](/docs): includes the methodology and documentations 
- [notebooks](/notebooks): includes sample codes in jupyter notebooks format
- [configen]: source codes

# Local development

install [miniconda](https://docs.conda.io/en/latest/miniconda.html)
and create new virtual environment

```bash
# create new environment, replace ```configen``` with the env name
conda create -n configen python==3.8

# activate the new environment
conda activate configen

# install essential packages and this repo package
pip install -r requirements.txt
```
