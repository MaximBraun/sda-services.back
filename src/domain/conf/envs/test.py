# coding utf-8

import logging

from ...entities.core import IConfEnv


class TestConfEnv(IConfEnv):
    logging_level: int = logging.DEBUG
