# coding utf-8

from enum import StrEnum


class VideoQuality(StrEnum):
    TURBO = "360p"
    STANDARD = "540p"
    HD = "720p"
    FULL_HD = "1080p"
