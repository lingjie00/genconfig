#!/usr/bin/env python
"""Entry point for program"""
import argparse
import logging
import json
import sys

from configen.parsers import JsonParser, YamlParser
from configen.utils import merge


logger = logging.getLogger(__name__)


def entry(args):
    """Command line interface entry point.

    Example:
        configen config.json
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", help="path to the config file/folder", type=str)
    parser.add_argument(
        "-o", "--output", help="path to save the loaded config", type=str)
    parser.add_argument(
        "-f", "--format", help="config output format",
        choices=["json", "yaml"], default="json", type=str)
    parser.add_argument(
        "-i", "--ignored",
        nargs="*",
        help="list of files to be ignored, support regex", type=str)
    parser.add_argument(
        "-v", "--verbose",
        help="debug level", type=str, default="INFO")
    parser.add_argument(
        "-a", "--append",
        help="append arbitrary dictionary in json format", type=str
    )
    parser.add_argument(
        "-r", "--read",
        nargs="*",
        help="which filetype to read", type=str, default=["*"]
    )
    args = parser.parse_args(args)

    # variables needed
    config_path = args.path
    output_path = args.output
    output_format = args.format
    ignored = tuple(args.ignored) if args.ignored else ()
    append_dict = json.loads(args.append) if args.append else {}
    read_format = args.read

    logging.basicConfig(
        datefmt='%m/%d/%Y %I:%M:%S %p',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=args.verbose
    )
    mega_config = {}

    # initate parsers
    config_parser_dict = {
        "json": JsonParser(),
        "yaml": YamlParser()
    }
    if read_format == "*":
        read_format = list(config_parser_dict.keys())

    # load config
    for config_parser_name in read_format:
        config_parser = config_parser_dict[config_parser_name]
        config = config_parser.load(config=config_path, ignored=ignored)
        merge(mega_config, config.config)

    # override the append dict
    if append_dict:
        logger.info(f"Override dictionary value with {append_dict}")
    mega_config.update(append_dict)

    # save config
    if output_path is not None:
        config_parser_dict[output_format].write(output_path, mega_config)


if __name__ == "__main__":
    logger.info("Start Configen command line interface")
    entry(sys.argv[1:])
