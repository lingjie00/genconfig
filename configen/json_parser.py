import json
from configen.base_parser import Parser


class JsonParser(Parser):
    """Json parser."""
    extension = "json"

    def _write_method(self, filename: str) -> Parser:
        filename = self._append_extension(filename)

        with open(filename, "w") as file:
            json.dump(self.config, file, indent=4)

        return self

    def _load_method(self, filename: str) -> dict:
        filename = self._append_extension(filename)

        with open(filename, "r") as json_config:
            config = json.loads(json_config.read())

        return config
