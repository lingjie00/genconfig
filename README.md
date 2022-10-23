# GenConfig

[![package](https://github.com/lingjie00/genconfig/actions/workflows/project-actions.yml/badge.svg)](https://github.com/lingjie00/genconfig/actions/workflows/project-actions.yml)

Manage config using folder structure, currently support Json and Yaml.


<!-- vim-markdown-toc GFM -->

* [Installation](#installation)
* [Example usage](#example-usage)
* [Project overview](#project-overview)
* [Usage](#usage)
    * [Parameters](#parameters)

<!-- vim-markdown-toc -->

# Installation

```bash
pip install genconfig
```

# Example usage

1. Arrange the config files into folders, sub-folders, and files.

    ```
    sample-config/config-mix/
    ├── basic.yml
    ├── function
    │   ├── function1.json
    │   └── function2.yml
    ├── param.yml
    └── pipeline.json

    1 directory, 5 files
    ```

2. Run the `genconfig`

    ```bash
    genconfig sample-config/config-mix -o config.json
    ```

3. Retrieve a single merged config

    ```
    {
        "name": "config-01",
        "training": true,
        "parameters": {
            "num_nodes": 200,
            "num_samples": 100,
            "max_time": 40
        },
        "function": {
            "function1": {
                "name": "transform",
                "param": "col1"
            },
            "function2": {
                "name": "load",
                "param": "col"
            }
        },
        "pipeline": [
            {
                "name": "extraction",
                "function": "etl.extraction"
            },
            {
                "name": "training",
                "function": "model.training"
            },
            {
                "name": "evaluation",
                "function": "model.evaluation"
            },
            {
                "name": "deployment",
                "function": "cloud.deploy"
            }
        ]
    }
    ```

# Project overview

The dream of a mature project is to cover most of the essential functions, and
the interactions users would require is to modify the configuration files
based on specific needs. For example, a user running model training for a new
region A does not need to write any new codes, instead simply modifying the
configuration files.

However, as the project grows, so does the configuration file. There are various
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
[https://lingjie00.github.io/genconfig/](https://lingjie00.github.io/genconfig/)

The GitHub repo is at [https://github.com/lingjie00/genconfig](https://github.com/lingjie00/genconfig)

# Usage

1. Convert a folder structure into a single json config file
    ```bash
    genconfig --path=folder_path --output="config.json"
    ```

## Parameters

- ignored
    - User can choose to ignore some keys and not expand into sub-folders
    ```bash
    # supports regex matching
    genconfig config_path -o config.json --ignore "config1.json" "config2.yaml" "debug.*json"
    ```
- keep
    - Different from ignored, instead read only files with matching file name
    ```bash
    # supports regex matching
    genconfig config_path -o config.json --keep "only_this_config.yaml"
    ```
- verbose
    - the level of logging to display
    ```bash
    # refer to python logging for acceptable levels
    genconfig config_path -o config.json --verbose "DEBUG"
    ```
- append
    - useful for manual replace/update values
    ```bash
    # input has to be in json format
    genconfig config_path -o config.json --append "{'name': 'updated_name'}"
    ```
- read
    - Useful when there is a mixture of config file types but only want to read
      a specific file type
    ```bash
    genconfig config_path -o config.json --read "json"
    ```
- folder
    - useful to ignore folder names as key, then user can arrange config files
      in any subfolders without worrying about nested keys
    ```bash
    genconfig config_path -o config.json --folder False
    ```
