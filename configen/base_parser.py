"""Defines the base parser requirements."""
from __future__ import annotations

import abc
import os
import re
from collections import deque
from typing import Tuple, Union


class Parser:
    """The base Parser."""

    extension: str = ""
    """The parser file extension."""
    config: dict = {}
    """The loaded config."""

    def __init__(self, config: Union[dict, None] = None):
        """Initiate object with optional initial config."""
        if config is not None:
            assert isinstance(
                config, dict
            ), f"Expected config to be dict get {type(config)}"
        self.config = config

    def __eq__(self, parser: object) -> bool:
        """Compares if given parser is same as self."""
        if isinstance(parser, Parser):
            return parser.extension == self.extension
        return False

    def __str__(self):
        """Returns the print value."""
        return self.extension

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
        assert isinstance(input_path, str), f"expected type str got {type(input_path)}"

        filename, file_extension = os.path.splitext(input_path)
        if file_extension != "." + self.extension:
            input_path += "." + self.extension
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

    @staticmethod
    def _search_match(name: str, ignored: Tuple[str]) -> bool:
        """Checks if the name is present in the ignored list."""
        assert isinstance(name, str), f"Expected name as str, get {type(name)}"
        assert isinstance(
            ignored, tuple
        ), f"Expected ignored as tuple, get {type(name)}"

        for ignore in ignored:
            # if there is a regex match, return true
            result = re.search(ignore, name)
            if isinstance(result, re.Match):
                return True
        return False

    def load(self, config: Union[str, dict, None], ignored: Tuple[str] = ()) -> Parser:
        """Loads the config (single, or multiple files, or dict).

        Params:
            config: either

            1. single config
            2. filepath for a folder of configs
            3. dictionary containing the config itself

            ignored: list of regex match strings to ignore in file names

        Returns:
            self with the config loaded in memory

        Example:
            single file: `load("config.json")`

            multiple files: `load("config_folder")`

            dictionary: `load({"name": "config"})
        """
        if config is not None:
            assert isinstance(
                config, (str, dict)
            ), f"expected (str, dict) got {type(config)}"

        if isinstance(ignored, str):
            ignored = (ignored,)

        assert isinstance(ignored, tuple), "expected ignored as tuple, got {type(ignored)}"

        # if config is None, then remove the stored config
        if config is None:
            self.config = None
            return self

        # if given dictionary then stores it and end
        if isinstance(config, dict):
            self.config = config
            return self

        filename, file_extension = os.path.splitext(config)
        # if the config is a single config
        if file_extension == "." + self.extension:
            self.config = self._load_method(config)
            return self

        # idea: iterate through the root folder, parse all configs
        # stores the folder into a queue, then literately retrieve queue to
        # maintain folder hierarchy
        files = os.listdir(config)
        queue: deque[str] = deque()

        if self.config is None:
            self.config = {}

        # first iteration to get the depth 1 keys and folders
        for file in files:
            # skip those in the ignored
            if self._search_match(file, ignored):
                continue
            filename, file_extension = os.path.splitext(file)
            filepath = os.path.join(config, file)
            if file_extension == "." + self.extension:
                self.config.update(self._load_method(filepath))
            elif os.path.isdir(filepath):
                queue.append(filepath)

        # while queue is not empty, repeat the procedure
        while queue:
            folder = queue.pop()
            files = os.listdir(folder)
            for file in files:
                # skip those in the ignored
                if self._search_match(file, ignored):
                    continue
                filename, file_extension = os.path.splitext(file)
                filepath = os.path.join(folder, file)
                base_folder = os.path.basename(folder)
                if base_folder not in self.config:
                    self.config[base_folder] = {}
                if file_extension == "." + self.extension:
                    self.config[base_folder].update(self._load_method(filepath))
                elif os.path.isdir(filepath):
                    queue.append(filepath)

        return self

    def write(self, filename: str, config: Union[str, dict, None] = None) -> Parser:
        """Writs the config to file.

        Parms:
            filename: the file to be output as

            config: the config file, if not provided use config stored in object

            depth: how deep should we go, if -1 then every config file does not
            contain sub-keys else the max folder layer is the depth parameter.

        Returns:
            self with config written to file

        Example:
            `write("config.json")`

            `write("config.json", {"name": "config1"})`
        """
        if config is not None:
            assert isinstance(
                config, (str, dict)
            ), f"expected str, dict, None got {type(config)}"

        # if given config, need to store the old config and restore later
        if config is None:
            # if no config is given just replace back the old config
            self_config, self.config = self.config, self.config

        else:
            # if given config
            self_config, self.config = self.config, config

        self._write_method(filename)

        # restore config
        self = self.load(self_config)

        return self

    def convert(
        self, filename: str, parser: type[Parser], config_path: Union[str, None] = None
    ) -> Parser:
        """Converts the config file into another file extension.

        Params:
            filename: the file path to be written as

            parser: the parser to be used for conversion

            config_path: file path to the config file, if no path is given then
            use the config stored in self

        Returns:
            self

        Example:
            `convert("config.json", "config.yml", YamlPaser)`
        """
        if config_path is not None:
            assert isinstance(
                config_path, str
            ), f"expected str or None got {type(config_path)}"
        assert isinstance(filename, str), f"expected str got {type(filename)}"
        assert isinstance(parser, Parser), f"expected ktr got {type(parser)}"

        # ensure the file extension are correct
        if config_path is not None:
            config_path = self._append_extension(config_path)
        filename = parser._append_extension(filename)

        # load the config from given path
        if config_path is not None:
            config = self.load(config_path).config
        else:
            config = self.config

        # writes config based on the given parser
        parser.write(filename=filename, config=config)

        return self
