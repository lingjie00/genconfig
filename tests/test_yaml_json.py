import unittest
import os
from configen.utils import yamlConfig
import json


class TestYamlJson(unittest.TestCase):
    """Test yaml json converter."""

    # the current file path
    # useful for retriving test files
    basePath = os.path.dirname(__file__) + "/"
    configFilePath = basePath + "testYaml/"
    configObj = yamlConfig()

    def test_load(self):
        """Function loads yaml config in memory"""
        config = self.configObj.load(self.configFilePath)
        self.assertEqual(
            config.get("name"), "JP ltvo test config",
            msg=config.get("name", config)
        )
        self.assertEqual(
            config.get("content"), [1, 2],
            msg=config.get("content", config)
        )

    def test_write(self):
        """Function writes yaml config as file."""
        content = "write yaml config"
        path = self.basePath + "write.yml"

        # writes to path
        config = {"name": content}
        self.configObj.write(config, path)

        # load from path
        loadConfig = self.configObj.load(path)

        # write and load should be the same content
        assert loadConfig.get("name") == content

        # remove the file
        os.remove(path)

    def test_toJson(self):
        """Function writes yaml config into Json
        config file with identical content."""
        # loads from yml
        config = self.configObj.load(self.configFilePath)
        path = self.basePath + "write.json"

        # writes to Json
        self.configObj.toJson(config, path)

        # reads json from file
        with open(path, "r") as file:
            loadConfig = json.load(file)

        assert loadConfig["name"] == config["name"]

        # remove the file
        os.remove(path)

    def test_fromJson(self):
        """Function writes Json config file into yaml config
        with identical content."""
        # writes a json config
        content = "test from json"
        config = {"name": content}
        jsonPath = self.basePath + "from.json"

        with open(jsonPath, "w") as jsonConfig:
            json.dump(config, jsonConfig)

        # converts json file to yaml file
        ymlPath = self.basePath + "from.yml"
        self.configObj.fromJson(jsonPath, ymlPath)

        # load written yaml file
        loadConfig = self.configObj.load(ymlPath)

        assert loadConfig["name"] == config["name"]

        # remove the files
        os.remove(jsonPath)
        os.remove(ymlPath)

    def test_ltvoConfig(self):
        """Check the LTVO conversion is correct."""
        jsonPath = self.configFilePath + "ltvoConfig.json"
        ymlPath = self.configFilePath + "ltvoConfig.yml"

        # convert ltvo json to yaml
        self.configObj.fromJson(jsonPath, ymlPath)

        # load the yaml config file
        configYml = self.configObj.load(ymlPath)

        # load the json config file
        with open(jsonPath, "r") as file:
            configJson = json.load(file)

        self.assertEqual(configYml, configJson)

        # remove the converted yaml config file
        os.remove(ymlPath)
