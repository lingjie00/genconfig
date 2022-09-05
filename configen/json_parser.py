import json
from ruamel.yaml import YAML
from configen.base_parser import Parser

_yaml = YAML()
_yaml.indent(mapping=2, sequence=4, offset=2)


class JsonParser(Parser):
    """Json parser."""
    extension = "json"

    def _write_method(self, filename: str) -> Parser:
        filename = self.check_extension(filename)

        with open(filename, "w") as file:
            json.dump(self.config, file, indent=4)

        return self

    def _load_method(self, filename: str) -> dict:
        filename = self.check_extension(filename)

        with open(filename, "r") as json_config:
            config = json.load(json_config)

        return config
