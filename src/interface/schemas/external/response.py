# coding utf-8

from typing import (
    Annotated,
    Any,
    Optional,
    Literal,
)

from os import getenv

from json import loads

from pendulum import now

from pydantic import (
    Field,
    field_validator,
    computed_field,
    model_validator,
    root_validator,
    HttpUrl,
)

from datetime import date, datetime

from instaloader import Profile, Post

from time import sleep

from random import uniform

from instagrapi.types import (
    User,
    Media,
    UserShort,
)

from ....domain.conf import app_conf

from ....domain.entities.core import (
    ISchema,
    IConfEnv,
)


app_service: str = f"/{getenv('APP_SERVICE', 'default')}"

conf: IConfEnv = app_conf()


class StatusRes(ISchema):
    video_id: Annotated[
        int,
        Field(...),
    ]
    video_status: Annotated[
        int,
        Field(...),
    ]
    first_frame: Annotated[
        str,
        Field(...),
    ]
    url: Annotated[
        str,
        Field(...),
    ]


class TemplateResp(ISchema):
    restyle_id: Annotated[
        int,
        Field(...),
    ]
    display_name: Annotated[
        str,
        Field(...),
    ]
    restyle_prompt: Annotated[
        str,
        Field(...),
    ]


class ItemsResponse(ISchema):
    items: Annotated[
        list[TemplateResp],
        Field(...),
    ]


class TokensResponse(ISchema):
    credit_daily: Annotated[
        int,
        Field(default=0, exclude=True),
    ]
    credit_monthly: Annotated[
        int,
        Field(default=0, exclude=True),
    ]
    credit_package: Annotated[
        int,
        Field(default=0, exclude=True),
    ]

    @computed_field
    @property
    def credits(
        self,
    ) -> int:
        return sum(
            (
                self.credit_daily,
                self.credit_monthly,
                self.credit_package,
            )
        )


class AuthRes(ISchema):
    access_token: Annotated[
        str,
        Field(..., alias="Token"),
    ]


class ResResp(ISchema):
    result: Annotated[
        AuthRes,
        Field(..., alias="Result"),
    ]


class Resp(ISchema):
    video_id: Annotated[
        int,
        Field(...),
    ]
    detail: Annotated[
        str,
        Field(default="Success"),
    ]


class StatusResp(ISchema):
    data: Annotated[
        list[StatusRes],
        Field(...),
    ]


class GenerationStatus(ISchema):
    status: Annotated[
        str,
        Field(...),
    ]
    video_url: Annotated[
        str | None,
        Field(default=None),
    ]


class Effect(ISchema):
    display_name: Annotated[
        str,
        Field(...),
    ]
    template_id: Annotated[
        int,
        Field(...),
    ]
    prompt: Annotated[
        str,
        Field(..., alias="display_prompt"),
    ]


class FrameResp(ISchema):
    last_frame: Annotated[
        str,
        Field(...),
    ]


class ChannelItem(ISchema):
    channel_id: Annotated[
        int,
        Field(...),
    ]
    channel_name: Annotated[
        str,
        Field(...),
    ]
    effect_items: Annotated[
        list[Effect],
        Field(...),
    ]


class EffectResponse(ISchema):
    effect_channel_items: Annotated[
        list[ChannelItem],
        Field(...),
    ]


class UTResp(ISchema):
    Ak: Annotated[
        str,
        Field(..., alias="access_key_id"),
    ]
    Sk: Annotated[
        str,
        Field(..., alias="access_key_secret"),
    ]
    Token: Annotated[
        str,
        Field(..., alias="security_token"),
    ]


class VideoResp(ISchema):
    path: Annotated[
        str,
        Field(...),
    ]
    url: Annotated[
        str,
        Field(...),
    ]
    asset_id: Annotated[
        int,
        Field(..., alias="asset_id"),
    ]
    asset_type: Annotated[
        int,
        Field(..., alias="asset_type"),
    ]
    duration: Annotated[
        float,
        Field(...),
    ]


class Response(ISchema):
    err_code: Annotated[
        int,
        Field(..., alias="ErrCode"),
    ]
    err_msg: Annotated[
        str | None,
        Field(default=None, alias="ErrMsg"),
    ]
    resp: Annotated[
        Resp
        | ItemsResponse
        | EffectResponse
        | UTResp
        | FrameResp
        | ResResp
        | VideoResp
        | StatusResp
        | TokensResponse
        | Any,
        Field(default=None, alias="Resp"),
    ]


class ChatGPTData(ISchema):
    b64_json: Annotated[
        str,
        Field(...),
    ]


class ChatGPTError(ISchema):
    code: Annotated[
        str | None,
        Field(default=None),
    ]
    message: Annotated[
        str,
        Field(...),
    ]


class ICalories(ISchema):
    title: Annotated[
        str | None,
        Field(default=None),
    ]
    kilocalories_per100g: Annotated[
        float,
        Field(...),
    ]
    proteins_per100g: Annotated[
        float,
        Field(...),
    ]
    fats_per100g: Annotated[
        float,
        Field(...),
    ]
    carbohydrates_per100g: Annotated[
        float,
        Field(...),
    ]
    fiber_per100g: Annotated[
        float,
        Field(...),
    ]


class CaloriesItems(ICalories):
    weight: Annotated[
        int,
        Field(...),
    ]


class ChatGPTCalories(ISchema):
    title: Annotated[
        str | None,
        Field(default=None, exclude=True),
    ]
    items: Annotated[
        list[CaloriesItems],
        Field(...),
    ]
    total: Annotated[
        ICalories,
        Field(...),
    ]

    @model_validator(mode="after")
    def set_title_to_total(self):
        if not self.total.title:
            if self.title:
                self.total.title = self.title
            elif self.items and self.items[0].title:
                self.total.title = self.items[0].title
        return self


class SharkDectorFactMessage(ISchema):
    message: Annotated[
        str,
        Field(...),
    ]
    status: Annotated[
        int,
        Field(default=200),
    ]


class DialogImageAnalysisMessage(ISchema):
    interaction_type: Annotated[
        str,
        Field(..., description="monologue or actual dialog"),
    ]
    second_participant_present: Annotated[
        str,
        Field(..., description="yes or no"),
    ]
    comment: Annotated[
        str,
        Field(...),
    ]
    status: Annotated[
        int,
        Field(default=200),
    ]


class ChatGPTErrorResponse(ISchema):
    error: Annotated[
        ChatGPTError,
        Field(...),
    ]


class ChatGPTResponse(ISchema):
    created: Annotated[
        int,
        Field(...),
    ]
    background: Annotated[
        str,
        Field(...),
    ]
    data: Annotated[
        list[ChatGPTData],
        Field(...),
    ]
    output_format: Annotated[
        str,
        Field(...),
    ]
    quality: Annotated[
        str,
        Field(...),
    ]
    size: Annotated[
        str,
        Field(...),
    ]


class ChatGPTResp(ISchema):
    url: Annotated[
        str,
        Field(...),
    ]
    detail: Annotated[
        str,
        Field(default="Success"),
    ]

    @field_validator("url", mode="after")
    @classmethod
    def create_preview_large_url(
        cls,
        value: str,
    ) -> str:
        if value is None:
            return value
        elif "cdn.wanxai.com" in value:
            return value
        relative_path = value.removeprefix("uploads/")
        return f"{conf.domain_url}{app_service}{conf.api_prefix}/media/{relative_path}"


class IInstagramResponse(ISchema):
    uuid: Annotated[
        str | None,
        Field(default=None),
    ]
    timestamp: Annotated[
        str,
        Field(default_factory=lambda: str(now())),
    ]
    status: Annotated[
        str,
        Field(default="success"),
    ]
    detail: Annotated[
        str,
        Field(...),
    ]


class InstagramSessionResponse(IInstagramResponse):
    detail: Annotated[
        str,
        Field(default="Session has been loaded"),
    ]


class InstagramAuthResponse(IInstagramResponse):
    detail: Annotated[
        str,
        Field(default="Successfull authorization and session has been saved"),
    ]


class InstagramUpdateUserResponse(IInstagramResponse):
    detail: Annotated[
        str,
        Field(default="Successfull user data updation"),
    ]


class InstagramTrackingUserResponse(IInstagramResponse):
    detail: Annotated[
        str,
        Field(default="Successfull added user to tracking"),
    ]


class IInstagramUserStatistics(ISchema):
    id: Annotated[
        int,
        Field(default=0),
    ]
    likes_count: Annotated[
        int,
        Field(default=0),
    ]
    comments_count: Annotated[
        int,
        Field(default=0),
    ]
    edge_followed_by: Annotated[
        int,
        Field(default=0, alias="followers_count"),
    ]
    edge_follow: Annotated[
        int,
        Field(default=0, alias="following_count"),
    ]
    edge_media_collections: Annotated[
        dict[str, Any] | int,
        Field(default=0, alias="publications_count"),
    ]
    mutual_subscriptions_count: Annotated[
        int,
        Field(default=0),
    ]
    non_reciprocal_following_count: Annotated[
        int,
        Field(default=0),
    ]
    non_reciprocal_followers_count: Annotated[
        int,
        Field(default=0),
    ]
    secret_fans: Annotated[
        int,
        Field(default=0),
    ]
    created_at: Annotated[
        date | None,
        Field(default_factory=lambda: now().date()),
    ]

    @classmethod
    def from_rocket(
        cls,
        data: dict[str, Any],
    ) -> "IInstagramUserStatistics":
        """Создаёт объект из словаря Rocket API, подтягивая нужные поля."""
        stats_mapping = {
            "likes_count": data.get("edge_liked_media_count", 0),
            "comments_count": data.get("edge_comments_count", 0),
            "followers_count": data.get("edge_followed_by", {}).get("count", 0),
            "following_count": data.get("edge_follow", {}).get("count", 0),
            "publications_count": data.get("edge_owner_to_timeline_media", {}).get(
                "count", 0
            ),
        }
        return cls(**stats_mapping)


class IRocketProfile(ISchema):
    id: Annotated[
        int,
        Field(..., alias="user_id"),
    ]
    username: Annotated[
        str,
        Field(...),
    ]
    full_name: Annotated[
        str,
        Field(...),
    ]
    biography: Annotated[
        str,
        Field(...),
    ]
    profile_pic_url: Annotated[
        str | None,
        Field(default=None, alias="profile_picture"),
    ]
    is_private: Annotated[
        bool,
        Field(...),
    ]
    is_verified: Annotated[
        bool,
        Field(...),
    ]
    is_business_account: Annotated[
        bool,
        Field(...),
    ]

    @classmethod
    def from_rocket(
        cls,
        data: dict[str, Any],
    ) -> "RocketProfile":
        """Создаёт объект RocketProfile из словаря Rocket API."""
        profile_data = {
            "user_id": int(data["id"]),
            "username": data.get("username", ""),
            "full_name": data.get("full_name", ""),
            "biography": data.get("biography", ""),
            "profile_picture": data.get("profile_pic_url"),
            "is_private": data.get("is_private", False),
            "is_verified": data.get("is_verified", False),
            "is_business_account": data.get("is_business_account", False),
        }
        return cls(**profile_data)


class RocketProfile(IRocketProfile):
    statistics: Annotated[
        IInstagramUserStatistics,
        Field(...),
    ]

    @classmethod
    def from_rocket(
        cls,
        data: dict[str, Any],
    ) -> "RocketProfile":
        """Создаёт объект RocketProfile из словаря Rocket API."""
        stats = IInstagramUserStatistics.from_rocket(data)
        profile_data = {
            "user_id": int(data["id"]),
            "username": data.get("username", ""),
            "full_name": data.get("full_name", ""),
            "biography": data.get("biography", ""),
            "profile_picture": data.get("profile_pic_url"),
            "is_private": data.get("is_private", False),
            "is_verified": data.get("is_verified", False),
            "is_business_account": data.get("is_business_account", False),
            "statistics": stats,
        }
        return cls(**profile_data)


class InstagramUserStatistics(ISchema):
    user_id: Annotated[
        int,
        Field(...),
    ]
    likes_count: Annotated[
        int,
        Field(...),
    ]
    comments_count: Annotated[
        int,
        Field(...),
    ]
    publications_count: Annotated[
        int,
        Field(...),
    ]
    followers_count: Annotated[
        int,
        Field(...),
    ]
    following_count: Annotated[
        int,
        Field(...),
    ]
    mutual_subscriptions_count: Annotated[
        int,
        Field(...),
    ]
    non_reciprocal_following_count: Annotated[
        int,
        Field(...),
    ]
    non_reciprocal_followers_count: Annotated[
        int,
        Field(...),
    ]
    tracking_id: Annotated[
        int | None,
        Field(default=None),
    ]
    created_at: Annotated[
        date,
        Field(default_factory=lambda: now().date()),
    ]

    @classmethod
    def from_instaloader_profile(
        cls,
        profile: Profile,
        user_id: int,
        mutual_count: int = 0,
        not_following_back_count: int = 0,
        not_followed_by_count: int = 0,
        max_posts: int = 10,
    ) -> "InstagramUserStatistics":
        posts = profile.get_posts()
        likes_count = 0
        comments_count = 0

        for i, post in enumerate(posts):
            if i >= max_posts:
                break
            likes_count += post.likes
            comments_count += post.comments
            sleep(uniform(0.4, 0.9))  # антибан

        return cls(
            user_id=user_id,
            likes_count=likes_count,
            comments_count=comments_count,
            followers_count=profile.followers,
            following_count=profile.followees,
            mutual_subscriptions_count=mutual_count,
            non_reciprocal_following_count=not_followed_by_count,
            non_reciprocal_followers_count=not_following_back_count,
        )


class IInstagramPost(ISchema):
    id: Annotated[
        int,
        Field(...),
    ]
    post_url: Annotated[
        str,
        Field(...),
    ]
    thumbnail_url: Annotated[
        str | None,
        Field(default=None),
    ]
    likes_count: Annotated[
        int,
        Field(...),
    ]
    comments_count: Annotated[
        int,
        Field(...),
    ]
    views_count: Annotated[
        int | None,
        Field(default=0),
    ]
    avg_likes: Annotated[
        float,
        Field(default=0),
    ]
    avg_views: Annotated[
        float,
        Field(default=0),
    ]


class InstagramPost(ISchema):
    user_id: Annotated[
        int,
        Field(...),
    ]
    likes_count: Annotated[
        int,
        Field(...),
    ]
    comments_count: Annotated[
        int,
        Field(...),
    ]
    views_count: Annotated[
        int | None,
        Field(default=0),
    ]
    avg_likes: Annotated[
        float,
        Field(default=0),
    ]
    avg_views: Annotated[
        float,
        Field(default=0),
    ]
    post_url: Annotated[
        str,
        Field(...),
    ]
    thumbnail_url: Annotated[
        str | None,
        Field(default=None),
    ]

    @classmethod
    def from_rocket(
        cls,
        data: dict[str, Any],
        user_id: int,
    ) -> "InstagramPost":
        return cls(
            user_id=user_id,
            likes_count=data["like_count"],
            comments_count=data["comment_count"],
            post_url=f"https://www.instagram.com/p/{data['code']}/",
            thumbnail_url=data["image_versions2"]["candidates"][0]["url"],
        )


class InstagramUser(ISchema):
    username: Annotated[
        str,
        Field(...),
    ]
    full_name: Annotated[
        str,
        Field(...),
    ]
    biography: Annotated[
        str | None,
        Field(default=None),
    ]
    profile_picture: Annotated[
        HttpUrl,
        Field(...),
    ]
    is_private: Annotated[
        bool,
        Field(...),
    ]
    is_verified: Annotated[
        bool,
        Field(...),
    ]
    is_business_account: Annotated[
        bool,
        Field(...),
    ]


class ITrackingUser(InstagramUser):
    likes_count: Annotated[
        int,
        Field(default=0),
    ]
    followers_count: Annotated[
        int,
        Field(default=0),
    ]


class InstagramUserResponse(InstagramUser):
    statistics: Annotated[
        list[IInstagramUserStatistics],
        Field(...),
    ]
    posts: Annotated[
        list[IInstagramPost],
        Field(...),
    ]


class InstagramFollower(ISchema):
    user_id: Annotated[
        int,
        Field(...),
    ]
    relation_type: Literal[
        "follower",
        "following",
        "not_following_back",
        "not_followed_by",
        "secret_fan",
        "unfollower",
        "mutual",
    ]
    pk: Annotated[
        str | None,
        Field(default=None, alias="related_user_id"),
    ]
    username: Annotated[
        str,
        Field(..., alias="related_username"),
    ]
    full_name: Annotated[
        str | None,
        Field(default=None, alias="related_full_name"),
    ]
    profile_pic_url: Annotated[
        HttpUrl,
        Field(..., alias="profile_picture"),
    ]
    created_at: Annotated[
        datetime,
        Field(default_factory=lambda: now()),
    ]


class ChatGPTCosmetic(ISchema):
    title: Annotated[
        str,
        Field(...),
    ]
    description: Annotated[
        str,
        Field(...),
    ]
    purpose: Annotated[
        str,
        Field(...),
    ]


class ChatGPTCosmeticMessage(ISchema):
    content: Annotated[
        list[ChatGPTCosmetic],
        Field(...),
    ]

    @field_validator("content", mode="before")
    @classmethod
    def validate_content(
        cls,
        value: str | Any,
    ) -> Any:
        if isinstance(value, str):
            value = value.strip()
            if value.startswith("```json"):
                value = value.removeprefix("```json").strip()
            if value.endswith("```"):
                value = value.removesuffix("```").strip()
            return loads(value)
        return value


class ChatGPTCosmeticChoice(ISchema):
    index: Annotated[
        int,
        Field(...),
    ]
    message: Annotated[
        ChatGPTCosmeticMessage,
        Field(...),
    ]


class ChatGPTCosmeticResponse(ISchema):
    choices: Annotated[
        list[ChatGPTCosmeticChoice],
        Field(...),
    ]
    error: Annotated[
        Any | None,
        Field(default=None),
    ]

    def fetch_data(
        self,
    ) -> list[ChatGPTCosmetic]:
        return self.choices[0].message.content


class ChatGPTInstagram(ISchema):
    description: Annotated[
        str,
        Field(...),
    ]
    hashtags: Annotated[
        list[str],
        Field(...),
    ]


class ChatGPTSubtitle(ISchema):
    url: Annotated[
        str,
        Field(...),
    ]
    detail: Annotated[
        str,
        Field(default="Success"),
    ]

    @field_validator("url", mode="after")
    @classmethod
    def create_preview_url(
        cls,
        value: str,
    ) -> str:
        if value is None:
            return value
        relative_path = value.removeprefix("uploads/")
        return f"{conf.domain_url}{app_service}{conf.api_prefix}/media/{relative_path}"


class ChatGPTInstagramMessage(ISchema):
    content: Annotated[
        ChatGPTInstagram,
        Field(...),
    ]

    @field_validator("content", mode="before")
    @classmethod
    def validate_content(
        cls,
        value,
    ) -> Any:
        return loads(value)


class ChatGPTInstagramChoice(ISchema):
    index: Annotated[
        int,
        Field(...),
    ]
    message: Annotated[
        ChatGPTInstagramMessage,
        Field(...),
    ]


class ChatGPTInstagramResponse(ISchema):
    choices: Annotated[
        list[ChatGPTInstagramChoice],
        Field(...),
    ]

    def fetch_data(
        self,
    ) -> ChatGPTInstagram:
        return self.choices[0].message.content


class TopmediaAuthData(ISchema):
    member_id: Annotated[
        str,
        Field(...),
    ]
    member_code: Annotated[
        str,
        Field(...),
    ]
    access_token: Annotated[
        str,
        Field(..., alias="token"),
    ]
    email: Annotated[
        str,
        Field(...),
    ]


class TopmediaTokenData(ISchema):
    can_use_pro: Annotated[
        int,
        Field(...),
    ]
    gen_pro_times: Annotated[
        int,
        Field(...),
    ]
    pro_times: Annotated[
        int,
        Field(...),
    ]


class TopmediaSlangData(ISchema):
    accent: Annotated[
        str,
        Field(...),
    ]
    accent_flag: Annotated[
        str,
        Field(...),
    ]
    accent_flag_png: Annotated[
        str,
        Field(...),
    ]
    recognized: Annotated[
        list[str | Any],
        Field(...),
    ]
    show_accent: Annotated[
        list[str | Any],
        Field(...),
    ]


class TopmediaSpeechData(ISchema):
    id: Annotated[
        int,
        Field(...),
    ]
    audition_status: Annotated[
        int,
        Field(...),
    ]
    oss_url: Annotated[
        str,
        Field(...),
    ]
    oss_path: Annotated[
        str,
        Field(...),
    ]
    name: Annotated[
        str,
        Field(..., alias="display_name"),
    ]


class TopmediaOssData(ISchema):
    url: Annotated[
        str,
        Field(...),
    ]


class TopmediaSpeechResponse(ISchema):
    type: Annotated[
        int,
        Field(default=0),
    ]
    name: Annotated[
        str,
        Field(...),
    ]
    speaker: Annotated[
        str,
        Field(...),
    ]
    oss_url: Annotated[
        str,
        Field(...),
    ]


class TopmediaSongResponse(ISchema):
    type: Annotated[
        int,
        Field(default=0),
    ]
    title: Annotated[
        str,
        Field(...),
    ]
    song_url: Annotated[
        str,
        Field(...),
    ]

    @field_validator("song_url", mode="after")
    @classmethod
    def validate_song_url(
        cls,
        value: str,
    ) -> str:
        return f"https://audiopipe.suno.ai/?item_id={value}"


class TopmediaSongData(ISchema):
    song_ids: Annotated[
        list[str],
        Field(...),
    ]


class TopmediaMusicData(ISchema):
    id: Annotated[
        int,
        Field(...),
    ]
    song_id: Annotated[
        str | None,
        Field(default=None),
    ]
    title: Annotated[
        str | None,
        Field(default=None),
    ]
    is_upload: Annotated[
        int,
        Field(...),
    ]
    create_time: Annotated[
        str,
        Field(...),
    ]


class TopmediaMusicResponse(ISchema):
    result: Annotated[
        list[TopmediaMusicData],
        Field(...),
    ]


class TopmediaResponse(ISchema):
    code: Annotated[
        int | None,
        Field(default=None),
    ]
    status: Annotated[
        int | None,
        Field(default=None),
    ]
    resp: Annotated[
        TopmediaAuthData
        | TopmediaTokenData
        | TopmediaSlangData
        | TopmediaSpeechData
        | TopmediaOssData
        | TopmediaSpeechResponse
        | TopmediaSongData
        | TopmediaSongResponse
        | TopmediaMusicResponse,
        Field(..., alias="data"),
    ]
    msg: Annotated[
        str,
        Field(default="Success", alias="message"),
    ]


class TopmediaAPIResponseData(ISchema):
    status: Annotated[
        int,
        Field(...),
    ]
    message: Annotated[
        str,
        Field(default="Success"),
    ]
    data: Annotated[
        TopmediaSpeechResponse | list[TopmediaSongResponse] | Any,
        Field(...),
    ]


class TopmediaAPIResponse(ISchema):
    message: Annotated[
        str,
        Field(default="Speech"),
    ]
    resp: Annotated[
        TopmediaAPIResponseData,
        Field(..., alias="data"),
    ]


class ChartData(ISchema):
    month: Annotated[
        str,
        Field(...),
    ]
    count: Annotated[
        int,
        Field(...),
    ]


class QwenChatData(ISchema):
    id: Annotated[
        str,
        Field(...),
    ]


class QwenMessageContent(ISchema):
    content: Annotated[
        str,
        Field(...),
    ]


class QwenChatMessage(ISchema):
    content_list: Annotated[
        list[QwenMessageContent] | None,
        Field(default_factory=list),
    ]


class QwenChatHistory(ISchema):
    messages: Annotated[
        dict[str, QwenChatMessage],
        Field(...),
    ]


class QwenChat(ISchema):
    history: Annotated[
        QwenChatHistory,
        Field(...),
    ]


class QwenGenerationData(ISchema):
    id: Annotated[
        str,
        Field(...),
    ]
    user_id: Annotated[
        str,
        Field(...),
    ]
    title: Annotated[
        str,
        Field(...),
    ]
    chat: Annotated[
        QwenChat,
        Field(...),
    ]
    current_id: Annotated[
        str,
        Field(..., alias="currentId"),
    ]


class QwenUploadData(ISchema):
    access_key_id: Annotated[
        str,
        Field(...),
    ]
    access_key_secret: Annotated[
        str,
        Field(...),
    ]
    security_token: Annotated[
        str,
        Field(...),
    ]
    bucketname: Annotated[
        str,
        Field(...),
    ]
    endpoint: Annotated[
        str,
        Field(...),
    ]
    file_path: Annotated[
        str,
        Field(...),
    ]
    file_url: Annotated[
        str,
        Field(...),
    ]
    file_id: Annotated[
        str,
        Field(...),
    ]


class QwenUserReponse(ISchema):
    user_id: Annotated[
        str,
        Field(..., alias="id"),
    ]


class QwenResponse(ISchema):
    success: Annotated[
        bool,
        Field(...),
    ]
    request_id: Annotated[
        str,
        Field(...),
    ]
    resp: Annotated[
        QwenGenerationData | QwenChatData | QwenUploadData | bool | Any,
        Field(..., alias="data"),
    ]


class QwenAuthResponse(ISchema):
    id: Annotated[
        str,
        Field(...),
    ]
    email: Annotated[
        str,
        Field(...),
    ]
    name: Annotated[
        str,
        Field(...),
    ]
    token: Annotated[
        str,
        Field(...),
    ]


class QwenErrorResponse(ISchema):
    detail: Annotated[
        str | None,
        Field(default=None),
    ]


class QwenPhotoAPIResponse(ISchema):
    message: Annotated[
        str,
        Field(default="success", alias="detail"),
    ]
    status: Annotated[
        int,
        Field(default=200),
    ]
    media_url: Annotated[
        str,
        Field(..., alias="url"),
    ]


class QwenAPIResponse(ISchema):
    media_url: Annotated[
        str,
        Field(..., alias="url"),
    ]
    message: Annotated[
        str,
        Field(..., alias="detail"),
    ]

    @field_validator("message", mode="after")
    @classmethod
    def validate_message(
        cls,
        value: str,
    ) -> str:
        return value.capitalize()


class GemCharacteristics(ISchema):
    streak: Annotated[
        str,
        Field(...),
    ]
    crystal_system: Annotated[
        str,
        Field(...),
    ]
    luster: Annotated[
        str,
        Field(...),
    ]
    hardness: Annotated[
        str,
        Field(...),
    ]
    mohs_hardness: Annotated[
        int,
        Field(...),
    ]
    tenacity: Annotated[
        str,
        Field(...),
    ]
    cleavage: Annotated[
        str,
        Field(...),
    ]
    magnetism: Annotated[
        str,
        Field(...),
    ]
    radioactivity: Annotated[
        str,
        Field(...),
    ]


class GemProperties(ISchema):
    luster: Annotated[
        str,
        Field(...),
    ]
    hardness: Annotated[
        str,
        Field(...),
    ]
    crystal_system: Annotated[
        str,
        Field(...),
    ]
    streak: Annotated[
        str,
        Field(...),
    ]
    tenacity: Annotated[
        str,
        Field(...),
    ]
    cleavage: Annotated[
        str,
        Field(...),
    ]
    magnetism: Annotated[
        str,
        Field(...),
    ]
    radioactivity: Annotated[
        str,
        Field(...),
    ]


class ChatGPTGemstone(ISchema):
    name: Annotated[
        str,
        Field(...),
    ]
    also_known_as: Annotated[
        list[str],
        Field(...),
    ]
    characteristics: Annotated[
        GemCharacteristics,
        Field(...),
    ]
    images: Annotated[
        list[str] | None,
        Field(default=None),
    ]
    description: Annotated[
        str,
        Field(...),
    ]
    properties: Annotated[
        GemProperties,
        Field(...),
    ]
    interesting_facts: Annotated[
        list[str],
        Field(..., min_items=1),
    ]
    history: Annotated[
        str,
        Field(...),
    ]


class PikaResponse(ISchema):
    success: Annotated[
        bool | None,
        Field(default=None),
    ]
    code: Annotated[
        int | str | None,
        Field(default=None),
    ]
    error: Annotated[
        str | None,
        Field(default=None),
    ]
    message: Annotated[
        str | None,
        Field(default=None, alias="msg"),
    ]
    error_code: Annotated[
        str | None,
        Field(default=None),
    ]


class PikaAuthResponse(ISchema):
    id: Annotated[
        str,
        Field(...),
    ]
    role: Annotated[
        str,
        Field(...),
    ]
    email: Annotated[
        str,
        Field(...),
    ]


class PikaCreditResponse(ISchema):
    free_credits: Annotated[
        int,
        Field(default=0),
    ]
    subscription_credits: Annotated[
        int,
        Field(default=0),
    ]

    @computed_field
    @property
    def credits(
        self,
    ) -> int:
        return sum(
            (self.free_credits, self.subscription_credits),
        )


class GenerationVideo(ISchema):
    id: Annotated[
        str,
        Field(...),
    ]
    model: Annotated[
        str,
        Field(...),
    ]
    resolution: Annotated[
        str,
        Field(...),
    ]
    status: Annotated[
        str,
        Field(...),
    ]


class GenerationDetails(ISchema):
    promptText: Annotated[
        str,
        Field(...),
    ]
    videos: Annotated[
        list[GenerationVideo],
        Field(...),
    ]


class GenerationData(ISchema):
    id: Annotated[
        str,
        Field(...),
    ]
    generation: Annotated[
        GenerationDetails,
        Field(...),
    ]


class PikaGenerationResponse(ISchema):
    success: Annotated[
        bool,
        Field(default=True),
    ]
    data: Annotated[
        GenerationData,
        Field(...),
    ]


class PikaVideoResponse(ISchema):
    success: Annotated[
        bool,
        Field(default=False),
    ]
    video_url: Annotated[
        str | None,
        Field(default=None),
    ]

    @classmethod
    def from_data(
        cls,
        data: dict,
    ) -> "PikaVideoResponse":
        try:
            media_url = data["data"]["results"][0]["videos"][0].get("resultUrl", None)
        except (KeyError, IndexError, TypeError):
            media_url = None

        return cls(
            success=True if media_url is not None else False,
            video_url=media_url,
        )


class IPikaResponse(ISchema):
    video_id: Annotated[
        str,
        Field(...),
    ]
    detail: Annotated[
        str,
        Field(default="Success"),
    ]


class IWanTaskResult(ISchema):
    download_url: Annotated[
        str,
        Field(..., alias="downloadUrl"),
    ]


class IWanResponseData(ISchema):
    id: Annotated[
        int,
        Field(...),
    ]
    task_result: Annotated[
        list[IWanTaskResult] | None,
        Field(default=None, alias="taskResult"),
    ]


class IWanPolicyData(ISchema):
    accessId: Annotated[
        str,
        Field(..., alias="access_id"),
    ]
    policy: Annotated[
        str,
        Field(...),
    ]
    signature: Annotated[
        str,
        Field(...),
    ]
    dir: Annotated[
        str,
        Field(...),
    ]
    host: Annotated[
        str,
        Field(...),
    ]
    expire: Annotated[
        int,
        Field(...),
    ]
    key: Annotated[
        str,
        Field(...),
    ]


class WanResponse(ISchema):
    success: Annotated[
        bool,
        Field(default=False),
    ]
    http_code: Annotated[
        int,
        Field(..., alias="httpCode"),
    ]
    error_code: Annotated[
        int,
        Field(..., alias="errorCode"),
    ]
    error_msg: Annotated[
        str | None,
        Field(default=None, alias="errorMsg"),
    ]
    data: Annotated[
        bool | str | IWanResponseData | IWanPolicyData | None,
        Field(default=None),
    ]
    request_id: Annotated[
        str,
        Field(..., alias="requestId"),
    ]
    failed: Annotated[
        bool,
        Field(...),
    ]
    trace_id: Annotated[
        str,
        Field(..., alias="traceId"),
    ]


class IWanResponse(ISchema):
    media_id: Annotated[
        str,
        Field(...),
    ]
    detail: Annotated[
        str,
        Field(default="Success"),
    ]


class IWanMediaResponse(ISchema):
    success: Annotated[
        bool,
        Field(default=False),
    ]
    media_urls: Annotated[
        str | list[str],
        Field(...),
    ]

    @classmethod
    def from_data(
        cls,
        data: WanResponse,
    ) -> "IWanMediaResponse":
        task_result: list[str] | None = (
            [media.download_url for media in data.data.task_result]
            if data.data.task_result
            else None
        )
        return cls(
            success=data.success,
            media_urls=task_result or "generating",
        )


class LocationResponse(ISchema):
    title: Annotated[
        str,
        Field(...),
    ]
    source_url: Annotated[
        str,
        Field(...),
    ]
    image_url: Annotated[
        str,
        Field(...),
    ]


class IWeightCalories(ISchema):
    title: Annotated[
        str | None,
        Field(default=None),
    ]
    weight: Annotated[
        int,
        Field(...),
    ]
    kilocalories: Annotated[
        float,
        Field(...),
    ]
    proteins: Annotated[
        float,
        Field(...),
    ]
    fats: Annotated[
        float,
        Field(...),
    ]
    carbohydrates: Annotated[
        float,
        Field(...),
    ]
    fiber: Annotated[
        float,
        Field(...),
    ]


class CaloriesWeightDishes(ISchema):
    title: Annotated[
        str,
        Field(...),
    ]
    weight: Annotated[
        int,
        Field(...),
    ]
    items: Annotated[
        list[IWeightCalories],
        Field(...),
    ]
    total: Annotated[
        IWeightCalories,
        Field(...),
    ]


class ChatGPTWeightCalories(ISchema):
    dishes: Annotated[
        list[CaloriesWeightDishes],
        Field(...),
    ]


class ChatGPTCaloriesMessage(ISchema):
    content: Annotated[
        ChatGPTCalories,
        Field(...),
    ]

    @field_validator("content", mode="before")
    @classmethod
    def validate_content(
        cls,
        value,
    ) -> Any:
        return loads(value)


class ChatGPTWeightCaloriesMessage(ISchema):
    content: Annotated[
        ChatGPTWeightCalories,
        Field(...),
    ]

    @field_validator("content", mode="before")
    @classmethod
    def validate_content(
        cls,
        value,
    ) -> Any:
        return loads(value)


class ChatGPTCaloriesChoice(ISchema):
    index: Annotated[
        int,
        Field(...),
    ]
    message: Annotated[
        ChatGPTCaloriesMessage,
        Field(...),
    ]


class ChatGPTCaloriesResponse(ISchema):
    choices: Annotated[
        list[ChatGPTCaloriesChoice],
        Field(...),
    ]

    def fetch_data(
        self,
    ) -> ChatGPTCalories:
        return self.choices[0].message.content


class ChatGPTWeightCaloriesChoice(ISchema):
    index: Annotated[
        int,
        Field(...),
    ]
    message: Annotated[
        ChatGPTWeightCaloriesMessage,
        Field(...),
    ]


class ChatGPTWeightCaloriesResponse(ISchema):
    choices: Annotated[
        list[ChatGPTWeightCaloriesChoice],
        Field(...),
    ]

    def fetch_data(
        self,
    ) -> ChatGPTWeightCalories:
        return self.choices[0].message.content


class AntiqueDetails(ISchema):
    name: Annotated[
        str | None,
        Field(default=None),
    ]
    category: Annotated[
        str | None,
        Field(default=None),
    ]
    period: Annotated[
        str | None,
        Field(default=None),
    ]
    origin: Annotated[
        str | None,
        Field(default=None),
    ]
    style: Annotated[
        str | None,
        Field(default=None),
    ]
    materials: Annotated[
        str | None,
        Field(default=None),
    ]
    artist: Annotated[
        str | None,
        Field(default=None),
    ]
    rarity: Annotated[
        str | None,
        Field(default=None),
    ]
    release_date: Annotated[
        str | None,
        Field(default=None),
    ]
    color: Annotated[
        str | None,
        Field(default=None),
    ]
    condition: Annotated[
        str | None,
        Field(default=None),
    ]
    provenance: Annotated[
        str | None,
        Field(default=None),
    ]


class Antiques(ISchema):
    title: Annotated[
        str,
        Field(...),
    ]
    current_value: Annotated[
        int | float | None,
        Field(default=None),
    ]
    low_value: Annotated[
        int | float | None,
        Field(default=None),
    ]
    high_value: Annotated[
        int | float | None,
        Field(default=None),
    ]
    description: Annotated[
        str,
        Field(...),
    ]
    details: Annotated[
        AntiqueDetails,
        Field(...),
    ]

    @field_validator("current_value", "low_value", "high_value")
    @classmethod
    def validate_value(
        cls,
        value,
    ) -> float:
        return value / 1000


class ChatGPTAntiquesMessage(ISchema):
    content: Annotated[
        Antiques,
        Field(...),
    ]

    @field_validator("content", mode="before")
    @classmethod
    def validate_content(cls, value) -> list:
        if isinstance(value, str):
            value = value.strip()
            if value.startswith("```"):
                value = "\n".join(value.splitlines()[1:-1])
            return loads(value)
        return value


class ChatGPTAntiquesChoice(ISchema):
    index: Annotated[
        int,
        Field(...),
    ]
    message: Annotated[
        ChatGPTAntiquesMessage,
        Field(...),
    ]


class ChatGPTAntiquesResponse(ISchema):
    choices: Annotated[
        list[ChatGPTAntiquesChoice],
        Field(...),
    ]

    def fetch_data(
        self,
    ) -> list[Antiques]:
        return self.choices[0].message.content
