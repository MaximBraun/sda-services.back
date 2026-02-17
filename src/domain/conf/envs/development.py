# coding utf-8

import logging

from ...entities.core import IConfEnv


class DevConfEnv(IConfEnv):
    logging_level: int = logging.DEBUG
