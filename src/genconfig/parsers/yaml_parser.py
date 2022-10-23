from ruamel.yaml import YAML
from genconfig.base_parser import Parser


class YamlParser(Parser):
    """Yaml parser."""
    extension = "yml"

    _yaml = YAML()
    _yaml.indent(mapping=2, sequence=4, offset=2)

    def _write_method(self, filename: str) -> Parser:
        # check if the given path ends with a yaml file extension
        filename = self._append_extension(filename)

        with open(filename, "w") as file:
            self._yaml.dump(self.config, file)

        return self

    def _load_method(self, filename: str) -> dict:
        filename = self._append_extension(filename)

        with open(filename, "r") as file:
            config = self._yaml.load(file.read())

        return config
