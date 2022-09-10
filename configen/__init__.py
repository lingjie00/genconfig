"""
.. include:: ../README.md
"""
from importlib.metadata import version
from configen.configen import cli
from configen.base_parser import Parser
from configen.json_parser import JsonParser
from configen.yaml_parser import YamlParser

__author__ = "Ling"
__email__ = "lingjie@u.nus.edu"
__version__ = version("configen")
__all__ = [cli, Parser, JsonParser, YamlParser]
