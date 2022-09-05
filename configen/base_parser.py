"""Defines the base parser requirements."""
from __future__ import annotations
from typing import Union

import abc


class Parser(abc.ABC):
    """The base Parser."""
    extension: str
    """The parser file extension."""
    config: dict
    """The loaded config."""

    def _append_extension(self, input_path: str) -> str:
        """Output the input_path with the file extension.

        Params:
            input_path: the path to be checked

        Returns:
            the input_path with file extension

        Example:
            `_check_extension("config")` -> config.json

            `_check_extension("config.json")` -> config.json
        """
        # TODO: implement better extension checks
        if input_path.split(".")[-1] != self.extension:
            input_path += f".{self.extension}"
        return input_path

    @abc.abstractmethod
    def _load_method(self, filename: str) -> dict:
        """Implement the load method for different parser.

        Params:
            filename: the config filename

        Returns:
            the loaded config as a dictionary

        Example:
            `_load_method("config.json")`
        """
        pass

    @abc.abstractmethod
    def _write_method(self, filename: str) -> Parser:
        """Implement the write method for different parser.

        The config content is retrieved from the object itself.

        Params:
            filename: the config file to write to

        Returns:
            does not return anything

        Example:
            `_write_method("config.json")`
        """
        pass

    def load(self, config: Union[str, dict]) -> Parser:
        """Loads the config (single, or multiple files, or dict).

        Params:
            config: either

            1. single config
            2. filepath for a folder of configs
            3. dictionary containing the config itself

        Returns:
            self with the config loaded in memory

        Example:
            single file: `load("config.json")`

            multiple files: `load("config_folder")`

            dictionary: `load({"name": "config"})
        """
        pass

    def write(self, filename: str, config: Union[str, dict, None]) -> Parser:
        """Writs the config to file.

        Parms:
            filename: the file to be output as

            config: the config file, if not provided use config stored in object

        Returns:
            self with config written to file

        Example:
            `write("config.json")`

            `write("config.json", {"name": "config1"})`
        """
        pass

    def convert(self, config_path: str, filename: str, parser: type(Parser)) -> Parser:
        """Converts the config file into another file extension.

        Params:
            config_path: file path to the config file

            filename: the file path to be written as

            parser: the parser to be used for conversion

        Returns:
            self

        Example:
            `convert("config.json", "config.yml", YamlPaser)`
        """
        # ensure the file extension are correct
        config_path = self._append_extension(config_path)
        filename = parser.append_extension(filename)

        # load the config from given path
        config = self.load(config_path)

        # writes config based on the given parser
        parser.write(filename=filename, config=config)

        return self
