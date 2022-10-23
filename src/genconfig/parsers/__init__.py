from genconfig.parsers.json_parser import JsonParser
from genconfig.parsers.yaml_parser import YamlParser

parser_list = [JsonParser, YamlParser]

__all__ = ["JsonParser", "YamlParser"]
