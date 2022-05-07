import logging
import pathlib

import os

ROOT_DIR = os.path.abspath(os.curdir)
print(f'\nROOT_DIR: {ROOT_DIR}')


def get_logger(namespace: str,class_name: str):
    logger = logging.getLogger(f'{namespace}.{class_name}')
    handler = logging.FileHandler(f'{namespace}.log')  # make more generic with a local logging module
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


