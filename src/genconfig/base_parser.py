"""Defines the base parser requirements."""
from __future__ import annotations

import abc
import logging
import os
import re
from typing import Tuple, Union, Optional, Any, Dict

from genconfig.utils import merge

logger = logging.getLogger(__name__)


class Parser:
    """The base Parser."""

    extension: str = ""
    """The parser file extension."""
    config: dict = {}
    """The loaded config."""

    def __init__(self, config: Optional[dict] = None):
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
        assert isinstance(input_path, str),\
            f"expected type str got {type(input_path)}"

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
    def _search_match(name: str, check_list: Tuple[str]) -> bool:
        """Checks if the name is present in the ignored list.

        Params:
            name: name to be checked
            check_list: list to be check

        Returns:
            bool representing if name is in check list
        """
        if check_list == ("",):
            return False
        assert isinstance(name, str), f"Expected name as str, get {type(name)}"
        assert isinstance(
            check_list, tuple
        ), f"Expected check_list as tuple, get {type(check_list)}"

        for ignore in check_list:
            # if there is a regex match, return true
            result = re.search(ignore, name)
            if isinstance(result, re.Match):
                return True
        return False

    def join(
            self,
            curr_config: Dict[str, Any],
            filepath: str,
            ignore_keys: Tuple[str] = ("", ),
            ignored: Tuple[str] = ("", ),
            keep: Tuple[str] = ("", ),
            merge_conflict: bool = True,
            use_folder: bool = True):
        """Joins config.

        Params:
            curr_config: the existing loaded config
            filepath: file path to the new config to be loaded
            ignore_keys: the folders that will not be use as keys
            ignored: list of file names to be ignored
            keep: list of file names to be kept, if not empty then load only these file names
            merge_conflict: if to merge the conflicts
            use_folder: if to use folder as key

        Returns:
            updated config
        """
        # the current loaded filepath
        logger.debug(f"{curr_config=}")
        logger.debug(f"{filepath=}")
        logger.debug(f"{ignore_keys=}")
        logger.debug(f"{ignored=}")
        logger.debug(f"{keep=}")
        logger.debug(f"{merge_conflict=}")
        logger.debug(f"{use_folder=}")
        # get the current filename and extension
        base_filename = os.path.basename(filepath)
        filename, file_extension = os.path.splitext(base_filename)
        logger.debug(f"Joining {filename=} with {file_extension=}")

        assert isinstance(
            ignore_keys, tuple
        ), f"expected ignored as tuple, got {type(ignore_keys)}"
        assert isinstance(
            ignored, tuple
        ), f"expected ignored as tuple, got {type(ignored)}"
        assert isinstance(
            keep, tuple
        ), f"expected ignored as tuple, got {type(keep)}"

        if self._search_match(filename, ignored):
            # ignore the file if it's in the ignored list
            logger.debug(f"{filename} is in ignored list, ignored")
            return curr_config

        elif keep != ("",) and not self._search_match(filename, keep):
            # not in the keep list
            logger.debug(f"{filename} not in keep list, ignored")
            return curr_config

        if file_extension == "." + self.extension:
            # load the file if it's of the config format
            logger.info(f"{'='*5} Reading {filepath}")
            new_config = self._load_method(filepath)
            curr_config = merge(curr_config, new_config, merge_conflict=merge_conflict)

        elif os.path.isdir(filepath):
            # if the path is a folder, iteratively add the folder files
            files = os.listdir(filepath)
            # ensure files are in order
            files = sorted(files)
            for file in files:
                new_path = os.path.join(filepath, file)
                # base folder will be used as the key
                base_folder = os.path.basename(os.path.dirname(new_path))
                logger.debug(f"{base_folder=}")
                # decide if to use folder as key
                if use_folder and base_folder not in ignore_keys:
                    logger.debug(f"Using folder {base_folder} as key")
                    use_config = curr_config.get(base_folder, {})
                else:
                    logger.debug(f"Did not use folder {base_folder} as key")
                    use_config = curr_config

                # generate new config
                new_config = self.join(
                    curr_config=use_config,
                    ignore_keys=ignore_keys,
                    filepath=new_path,
                    ignored=ignored,
                    keep=keep,
                    merge_conflict=merge_conflict,
                    use_folder=use_folder
                )

                # add back the new config
                if use_folder:
                    curr_config[base_folder] = new_config
                else:
                    curr_config = new_config
        return curr_config

    def load(
        self, config: Union[str, dict, None],
        add_path: bool = False,
        replace: bool = False,
        ignore_keys: Tuple[str] = ("", ),
        *args, **kwargs
    ) -> Parser:
        """Loads the config (single, or multiple files, or dict).

        Params:
            config: either

            1. single config
            2. filepath for a folder of configs
            3. dictionary containing the config itself

            ignored: list of regex match strings to ignore in file names
            keep: list of regex match strings to keep (only)
            add_path: if to add the config filepath
            replace: if to replace the existing config
            other args will be passed to self.join

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

        # if config is None, then remove the stored config
        if config is None:
            self.config = {}
            return self

        # if given dictionary then stores it and end
        elif isinstance(config, dict):
            logger.info(f"{'='*5} Loading dictionary")
            self.config = config
            return self

        # if replace config, remove the stored config
        if replace:
            self.config = {}

        filename, file_extension = os.path.splitext(config)
        # if the config is a single config
        if file_extension == "." + self.extension:
            logger.info(f"{'='*5} Loading single file {config}")

        if self.config is None:
            self.config = {}

        # base folder will be used as the key
        base_folder = os.path.basename(os.path.dirname(config))
        ignore_keys = ignore_keys + (base_folder, )

        self.config = self.join(
                self.config,
                config,
                ignore_keys=ignore_keys,
                *args, **kwargs)

        # ensure base folder is not in configs
        if base_folder in self.config:
            self.config.pop(base_folder)

        if add_path:
            self.config["config_path"] = config

        logger.debug(f"Config after loading: {self.config}")

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
        self, filename: str, parser: type[Parser], config_path: Optional[str] = None
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
        assert isinstance(parser, Parser), f"expected str got {type(parser)}"

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
