# configen

[![package](https://github.com/lingjie00/configen/actions/workflows/project-actions.yml/badge.svg)](https://github.com/lingjie00/configen/actions/workflows/project-actions.yml)

Manage Json and Yaml config using folder structure.


<!-- vim-markdown-toc GFM -->

* [Project overview](#project-overview)
* [Using the library](#using-the-library)
    * [Usage](#usage)
    * [Parameters](#parameters)
    * [Installation](#installation)

<!-- vim-markdown-toc -->

# Project overview

The dream of a mature project is to cover most of the essential functions, and
the interactions users would require is to modify the configuration files
based on specific needs. For example, a user running model training for a new
region A does not need to write any new codes, instead simply modifying the
configuration files.

However, as the project grows, so do the configuration file. There are various
settings region A would require but not all of them need constant updates.
Therefore, having a programmatic way to update the configuration files and to
display them in an easy-to-understand format is crucial.

I propose to present the configuration files in a folder structure. The root
folder represents the first level keys in the configs, and the subfolders
represent nested keys.

Furthermore, we should allow both json and yaml config files. Json is easy to
create while yaml allows comments and variables creation. Both Json and yaml
have their advantages.

The API documentation is available at
[https://lingjie00.github.io/configen/](https://lingjie00.github.io/configen/)

# Using the library

## Usage

1. Convert a folder structure into a single json config file
    ```bash
    configen --path=folder_path
    ```
2. Convert a config (json or yaml) into a folder structure
    ```bash
    configen --config-path=config_path
    ```

## Parameters

- Ignore
    - User can choose to ignore some keys and not expand into sub-folders
    ```bash
    # supports regex matching
    configen --config-path=config_path --ignore=""
    ```

## Installation

```bash
# install essential packages and this repo package
pip install .
```
