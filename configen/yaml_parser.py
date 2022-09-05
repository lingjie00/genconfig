import os
from ruamel.yaml import YAML
from configen.base_parser import Parser

_yaml = YAML()
_yaml.indent(mapping=2, sequence=4, offset=2)


class YamlParser(Parser):
    """Yaml parser."""
    extension = "yml"

    def _load_method(self, filename: str) -> dict:
        filename = self.check_extension(filename)

        with open(filename, "r") as file:
            config = _yaml.load(file.read())

        return config

    def _write_method(self, filename: str) -> Parser:
        # check if the given path ends with a yaml file extension
        filename = self.check_extension(filename)

        with open(filename, "w") as file:
            _yaml.dump(self.config, file)

        return self
