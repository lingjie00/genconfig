"""Test the parser."""
import unittest
import tempfile  # create temp config files
from contextlib import contextmanager
import os
from typing import Tuple

from configen import Parser, JsonParser, YamlParser


class TestParser(unittest.TestCase):
    """Perform unit test for the parsers."""

    parsers: Tuple[Parser] = (JsonParser, YamlParser)
    """The parsers to test."""

    # ground truth
    config_truth = {
        "name": "config-01",
        "training": True,
        "parameters": {
            "num_nodes": 200,
            "num_samples": 100,
            "max_time": 40
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
        ],
        "function": {
            "function1": {
                "name": "transform",
                "param": "col1"
            },
            "function2": {
                "name": "load",
                "param": "col2"
            }
        }
    }
    new_config = {"name": "new"}

    # parser configs
    dir_path = "sample-config"
    config_path = {
        "json": f"{dir_path}/sample.json",
        "yml": f"{dir_path}/sample.yml"
    }
    config_folder = {
        "json": f"{dir_path}/config-json",
        "yml": f"{dir_path}/config-yml"
    }
    config_dict_raw = {}

    for ext, path in config_path.items():
        with open(path) as file:
            config_raw = file.read()
        config_dict_raw[ext] = config_raw

    @contextmanager
    def write_tempfile(self, filename: str, config: str):
        """Writes a given config to a filename under a tempdir, yield the filename."""
        tempdir = tempfile.TemporaryDirectory()
        tempdirname = tempdir.name
        filepath = os.path.join(tempdirname, filename)
        with open(filepath, "w") as file:
            file.write(str(config))
        try:
            yield filepath
        finally:
            tempdir.cleanup()

    def test_write_tempfile(self):
        """Function should write a config to a specific filename."""
        config = {"name": "config1"}
        with self.write_tempfile(
                filename="config.json",
                config=config) as filepath:
            print(filepath)
            with open(filepath) as file:
                self.assertEqual(file.read(), str(config), file.read())

    def test_append_extension(self):
        """Function should append appropriate file extensions."""

        for parser in self.parsers:
            parser = parser()
            ext = parser.extension
            # without a given file extension, function will append extension
            self.assertEqual(
                f"config.{ext}", parser._append_extension("config"))
            # with given file extension, function does not append extension
            self.assertEqual(
                f"config.{ext}", parser._append_extension(f"config.{ext}"))
            # given a extension that is not the parser extension, parser will
            # still append the extension
            self.assertEqual(
                f"config.tmp.{ext}", parser._append_extension(f"config.tmp.{ext}"))
            # raises assertion error when give non string input
            self.assertRaises(AssertionError, parser._append_extension, 123)

    def test_load_method(self):
        """Function should load different kind of config files."""

        for parser in self.parsers:
            parser = parser()
            ext = parser.extension
            # write a sample config
            sample_config = self.config_dict_raw[ext]
            with self.write_tempfile(
                    filename="config." + ext,
                    config=sample_config) as filename:
                # load the config
                config_loaded = parser._load_method(filename)
                # yaml will load the config as ordered dictionary
                config_loaded = dict(config_loaded)
                self.assertEqual(config_loaded, self.config_truth, parser)

    def test_write_method(self):
        """Function should be able to write different kind of config files."""

        for parser in self.parsers:
            # load sample config
            ext = parser.extension
            parser = parser(self.config_truth)
            # write
            with self.write_tempfile(
                    filename="config." + ext,
                    config="") as filename:
                # write the config
                parser._write_method(filename)
                # rely on the implemented load method
                loaded_config = parser._load_method(filename)
                self.assertIsInstance(loaded_config, dict)
                print(type(loaded_config))
                self.assertEqual(loaded_config, self.config_truth, parser)

    def test_load(self):
        """Function should be able to load single config, a folder of configs
        and a dictionary containing the config itself."""
        for parser in self.parsers:
            parser = parser()
            ext = parser.extension
            # single config
            config_path = self.config_path[ext]
            loaded_config = parser.load(config_path).config
            self.assertEqual(loaded_config, self.config_truth, parser)

            # folder of config
            config_folder = self.config_folder[ext]
            loaded_config = parser.load(config_folder).config
            self.assertEqual(loaded_config, self.config_truth, parser)

            # dictionary containing the config
            loaded_config = parser.load(self.config_truth).config
            self.assertEqual(loaded_config, self.config_truth, parser)

    def test_write(self):
        """Function should be able to write stored config to file, or a new
        config to file."""
        for parser in self.parsers:
            parser = parser(self.config_truth)
            ext = parser.extension
            # write stored config
            with self.write_tempfile(
                    filename="config." + ext,
                    config="") as filename:
                parser.write(filename)
                loaded_config = parser._load_method(filename)
                self.assertEqual(loaded_config, self.config_truth, parser)

            # write new config
            with self.write_tempfile(
                    filename="config." + ext,
                    config="") as filename:
                parser.write(filename, self.new_config)
                loaded_config = parser._load_method(filename)
                self.assertEqual(loaded_config, self.new_config, parser)

    def test_search_method(self):
        """Function return True if regex match, else False."""
        parser = Parser()
        ignored = ("pipeline.*",)
        self.assertTrue(parser._search_match("pipeline.json", ignored=ignored))
        self.assertFalse(parser._search_match("nihao.yml", ignored=ignored))

        ignored = ("^pipeline.*",)
        self.assertTrue(parser._search_match("pipeline.json", ignored=ignored))
        self.assertFalse(parser._search_match("nihao.yml", ignored=ignored))

        ignored = (".*json",)
        self.assertTrue(parser._search_match("pipeline.json", ignored=ignored))
        self.assertFalse(parser._search_match("nihao.yml", ignored=ignored))

    def test_ignore(self):
        """Function should be able to ignore some config files."""
        config_truth = self.config_truth.copy()
        config_truth.pop("pipeline")
        for parser in self.parsers:
            parser = parser()
            ext = parser.extension
            parser.load(config=self.config_folder[ext], ignored="pipeline.*")
            loaded_config = dict(parser.config)
            self.assertEqual(loaded_config, config_truth, parser)

    def test_convert(self):
        """Function should be able to convert from one config file to
        another."""

        # test saving config from one parser against all the other parsers
        for parser in self.parsers:
            other_parsers = list(filter(lambda x: x != parser, self.parsers))
            parser = parser(self.new_config)
            ext = parser.extension
            for other_parser in other_parsers:
                other_parser = other_parser()
                other_ext = parser.extension
                # save the stored config
                with self.write_tempfile(
                        filename="config." + other_ext,
                        config="") as filename:
                    parser.convert(filename=filename, parser=other_parser)
                    loaded_config = other_parser._load_method(filename)
                    self.assertEqual(loaded_config, self.new_config, f"{parser}, {other_parser}")

                # save the config path
                with self.write_tempfile(
                        filename="config." + other_ext,
                        config="") as filename:
                    config_path = self.config_path[ext]
                    parser.convert(
                            filename=filename, parser=other_parser, config_path=config_path)
                    loaded_config = other_parser._load_method(filename)
                    # yaml load config as ordered dict
                    # we convert it back to dict for comparison
                    loaded_config = dict(loaded_config)
                    self.assertEqual(loaded_config, self.config_truth, f"{parser}, {other_parser}")


if __name__ == "__main__":
    unittest.main()
