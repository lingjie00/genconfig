#!/usr/bin/env python
"""Entry point for program"""
import argparse
import logging
import json
import sys
import os

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
        "-i", "--ignored",
        nargs="*",
        help="list of files to be ignored, support regex", type=str)
    parser.add_argument(
        "-k", "--keep",
        nargs="*",
        help="""list of files to be kept (outside of keep list will not be
            included), support regex""", type=str)
    parser.add_argument(
        "-v", "--verbose",
        help="debug level", type=str, default="INFO")
    parser.add_argument(
        "-a", "--append",
        help="append arbitrary dictionary in json format", type=str
    )
    parser.add_argument(
        "-f", "--folder",
        help="use folder name as key", type=bool, default=True
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
    ignored = tuple(args.ignored) if args.ignored else ()
    keep = tuple(args.keep) if args.keep else None
    append_dict = json.loads(args.append) if args.append else {}
    read_format = args.read
    use_folder = args.folder

    logging.basicConfig(
        datefmt='%m/%d/%Y %I:%M:%S %p',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=args.verbose
    )
    mega_config = {}

    # initiate parsers
    config_parser_dict = {
        "json": JsonParser(),
        "yml": YamlParser()
    }
    if read_format == ["*"]:
        read_format = list(config_parser_dict.keys())
    output_name, output_format = os.path.splitext(output_path)
    output_format = output_format.replace(".", "")

    logger.debug(f"{config_path=}")
    logger.debug(f"{output_path=}")
    logger.debug(f"{ignored=}")
    logger.debug(f"{append_dict=}")
    logger.debug(f"{read_format=}")

    # load config by folder structure
    file = [config_path]
    if os.path.isdir(config_path):
        files = os.listdir(config_path)
        files = map(lambda x: os.path.join(config_path, x), files)
    # ensure files are sorted
    files = sorted(files)
    for file in files:
        logger.info(f"Reading file {file}")
        filename, file_extension = os.path.splitext(file)
        file_extension = file_extension.replace(".", "")
        # check if file is in the read_format
        if file_extension in read_format or os.path.isdir(file):
            logger.debug(f"Using {file_extension} parser")
            # read
            config_parser = config_parser_dict[file_extension]
            config = config_parser.load(
                config=file, ignored=ignored, keep=keep, use_folder=use_folder)
            merge(mega_config, config.config)

    # override the append dict
    if append_dict:
        logger.info(f"Override dictionary value with {append_dict}")
    mega_config.update(append_dict)

    # save config
    if output_path is not None:
        config_parser_dict[output_format].write(output_path, mega_config)


def main():
    """Main entry point."""
    return entry(sys.argv[1:])


if __name__ == "__main__":
    logger.info("Start Configen command line interface")
    main()
