# coding utf-8

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Table,
)

from ......domain.entities.core import ITable


PixverseApplicationTemplates = Table(
    "pixverse_application_templates",
    ITable.metadata,
    Column(
        "application_id",
        Integer,
        ForeignKey("pixverse_applications.id"),
        primary_key=True,
    ),
    Column(
        "template_id",
        Integer,
        ForeignKey(
            "pixverse_templates.id",
        ),
        primary_key=True,
    ),
)

PixverseApplicationStyles = Table(
    "pixverse_application_styles",
    ITable.metadata,
    Column(
        "application_id",
        Integer,
        ForeignKey("pixverse_applications.id"),
        primary_key=True,
    ),
    Column(
        "style_id",
        Integer,
        ForeignKey(
            "pixverse_styles.id",
        ),
        primary_key=True,
    ),
)

PhotoGeneratorApplicationTemplates = Table(
    "photo_generator_application_templates",
    ITable.metadata,
    Column(
        "application_id",
        Integer,
        ForeignKey("photo_generator_applications.id"),
        primary_key=True,
    ),
    Column(
        "template_id",
        Integer,
        ForeignKey(
            "photo_generator_templates.id",
        ),
        primary_key=True,
    ),
)

PixverseApplicationCatagories = Table(
    "pixverse_application_categories",
    ITable.metadata,
    Column(
        "application_id",
        Integer,
        ForeignKey("pixverse_applications.id"),
        primary_key=True,
    ),
    Column(
        "category_id",
        Integer,
        ForeignKey(
            "pixverse_categories.id",
        ),
        primary_key=True,
    ),
)

PixverseAccountApplications = Table(
    "pixverse_account_applications",
    ITable.metadata,
    Column(
        "application_id",
        Integer,
        ForeignKey("pixverse_applications.id"),
        primary_key=True,
    ),
    Column(
        "account_id",
        Integer,
        ForeignKey(
            "pixverse_accounts.id",
        ),
        primary_key=True,
    ),
)


ApplicationProducts = Table(
    "application_products",
    ITable.metadata,
    Column(
        "application_id",
        Integer,
        ForeignKey("applications.id"),
        primary_key=True,
    ),
    Column(
        "product_id",
        Integer,
        ForeignKey("products.id"),
        primary_key=True,
    ),
)


UserServices = Table(
    "user_services",
    ITable.metadata,
    Column(
        "user_id",
        Integer,
        ForeignKey("auth_users.id"),
        primary_key=True,
    ),
    Column(
        "service_id",
        Integer,
        ForeignKey("services.id"),
        primary_key=True,
    ),
)

ServiceRoutes = Table(
    "service_routes",
    ITable.metadata,
    Column(
        "service_id",
        Integer,
        ForeignKey("services.id"),
        primary_key=True,
    ),
    Column(
        "route_id",
        Integer,
        ForeignKey("routes.id"),
        primary_key=True,
    ),
)


PikaApplicationTemplates = Table(
    "pika_application_templates",
    ITable.metadata,
    Column(
        "application_id",
        Integer,
        ForeignKey("pika_applications.id"),
        primary_key=True,
    ),
    Column(
        "template_id",
        Integer,
        ForeignKey(
            "pika_templates.id",
        ),
        primary_key=True,
    ),
)


PikaAccountApplications = Table(
    "pika_account_applications",
    ITable.metadata,
    Column(
        "application_id",
        Integer,
        ForeignKey("pika_applications.id"),
        primary_key=True,
    ),
    Column(
        "account_id",
        Integer,
        ForeignKey(
            "pika_accounts.id",
        ),
        primary_key=True,
    ),
)


WanApplicationTemplates = Table(
    "wan_application_templates",
    ITable.metadata,
    Column(
        "application_id",
        Integer,
        ForeignKey("wan_applications.id"),
        primary_key=True,
    ),
    Column(
        "template_id",
        Integer,
        ForeignKey(
            "wan_templates.id",
        ),
        primary_key=True,
    ),
)


WanAccountApplications = Table(
    "wan_account_applications",
    ITable.metadata,
    Column(
        "application_id",
        Integer,
        ForeignKey("wan_applications.id"),
        primary_key=True,
    ),
    Column(
        "account_id",
        Integer,
        ForeignKey(
            "wan_accounts.id",
        ),
        primary_key=True,
    ),
)

XimilarAccountApplications = Table(
    "ximilar_account_applications",
    ITable.metadata,
    Column(
        "application_id",
        Integer,
        ForeignKey("ximilar_applications.id"),
        primary_key=True,
    ),
    Column(
        "account_id",
        Integer,
        ForeignKey(
            "ximilar_accounts.id",
        ),
        primary_key=True,
    ),
)
