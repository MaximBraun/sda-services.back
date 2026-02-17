# coding utf-8

from enum import StrEnum


class TopmediaMethod(StrEnum):
    AUTH = "auth"

    VOICE = "voice"

    PROFILE = "profile"

    MUSIC = "music"


class PikaMethod(StrEnum):
    GENEREATE = "generate"

    AUTH = "auth"

    BASE = "base"

    LOGIN = "login"

    EMAIL = "email"

    PASSWORD = "password"

    SUBMIT = "submit"

    TEXT = "text"


class WanMethod(StrEnum):
    API = "api"

    OSS = "oss"


class XimilarMethod(StrEnum):
    API = "api"
