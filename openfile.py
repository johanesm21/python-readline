from loguru import logger
from tqdm import tqdm
import argparse
import pathlib
import sys
import time
import os
import pathvalidate


def setup_loguru():
    """Function to setup loguru for the first time running"""

    # remove all existing handlers and adding a new one with spesific format
    logger.remove()
    logger.add(
        sys.stdout,
        format="<g>{time:DD-MM-YYYY HH:mm:ss.SSS}</> | <lvl>{level: <8}</> | <c>{name}</>:<c>{function}</>:<c>{line}</> - <lvl>{message}</lvl>",
        colorize=True,
    )


def open_file(filepath: str):
    """Function to open specified file and showing the progress"""

    print("")

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as opened_file:
            file_size_in_bytes = os.stat(filepath).st_size

            with tqdm(
                total=file_size_in_bytes, unit="B", unit_scale=True, unit_divisor=1024
            ) as current:
                for line in opened_file:
                    readed_line_in_bytes = len(line.encode())
                    current.update(readed_line_in_bytes)

        print("")
    except Exception as error:
        logger.error(f"Opening file {args.file} failed with error {error}!")
        sys.exit(1)


def wait_for(wait_time: int):
    """Function to wait for specified time (in seconds)"""

    print("")
    for i in tqdm(range(0, wait_time)):
        time.sleep(1)
    print("")


if __name__ == "__main__":

    setup_loguru()

    parser = argparse.ArgumentParser(
        prog="Read File Lines Progress",
        description="Use this program to open a file and counting its lines",
        add_help=True,
    )

    parser.add_argument(
        "-f",
        "--file",
        help="Path for the file to be opened",
        type=str,
        required=True,
    )

    args = parser.parse_args()

    logger.info("Starting script....")
    logger.info(f"Using options ==> file = {args.file}")

    # sanitize file path from arguments
    try:
        filepath = pathvalidate.sanitize_filepath(args.file)
    except Exception as error:
        logger.error(
            f"Invalid file path provided! Please provide the correct file path!"
        )
        sys.exit(1)

    # check if file exists
    if not pathlib.Path(filepath).resolve().exists():
        logger.error(f"File {filepath} not exists or bad path supplied!")
        sys.exit(1)

    logger.info(f"Opening file {filepath}")
    open_file(filepath)

    logger.info(f"Script ended sucessfully!")
