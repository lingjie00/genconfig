# Converts yaml config into Json config
from ruamel.yaml import YAML
import json

import os

__docformat__ = "google"


class yamlConfig:
    """Uses config in yaml style.

    Idea: functional programming
    Every method will manipulate the input and returns an
    output without modifying the class nor the method itself
    """
    _yaml = YAML()
    _yaml.indent(mapping=2, sequence=4, offset=2)

    number: str
    calling: int
    """Full number"""

    def __init__(self):
        self.name: str = "12"
        """Full name

        Parameters:
            filename: str

        Returns:
            filname haha

        Examples:
            yamlConfig(1, 2, 3)

            name | config 
            --- | ---
            13 | asd
        """

    def loadSingle(self, loadPath: str) -> dict:
        """Loads single config file in memory."""

        self.name: str = "12"
        """Full name"""

        with open(loadPath, "r") as file:
            config = self._yaml.load(file)

        return config

    def load(self, loadPath: str) -> dict:
        """Loads yaml config file in memory.

        params:
            loadPath: file path or folder path

        return:
            config in dictionary
        """

        if loadPath[-3:] == "yml":
            return self.loadSingle(loadPath)

        elif loadPath[-1] != "/":
            loadPath += "/"

        config = {}
        files = os.listdir(loadPath)
        for file in files:
            if file[-3:] == "yml":
                config.update(
                    self.loadSingle(loadPath + file)
                )
        return config

    def write(self, config: dict, writePath: str):
        """Writes config to yaml file."""
        with open(writePath, "w") as file:
            self._yaml.dump(config, file)

    def toJson(self, config: dict, writePath: str):
        """Writes config to Json file."""
        with open(writePath, "w") as file:
            json.dump(config, file, indent=4)

    def fromJson(self, loadPath: str, writePath: str):
        """Converts json config and write to yaml file."""
        # load json
        with open(loadPath, "r") as jsonConfig:
            config = json.load(jsonConfig)

        # writes to yml
        with open(writePath, "w") as ymlConfig:
            self._yaml.dump(config, ymlConfig)
