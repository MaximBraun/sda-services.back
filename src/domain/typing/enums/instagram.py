# coding utf-8

from enum import StrEnum


class InstagramRelationType(StrEnum):
    FOLLOWER = "follower"
    FOLLOWING = "following"
    SECRET_FANS = "secret_fans"
    NON_RECIPROCAL = "non_reciprocal"
