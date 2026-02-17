# coding utf-8

from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
)


class ISchema(BaseModel):
    """Базовый класс схемы с расширенной конфигурацией для сериализации моделей.

    Наследуется от Pydantic BaseModel и добавляет:
    - Возможность обращаться к полям как по имени, так и по алиасу
    - Автоматическое преобразование Enum в их значения
    - Удобное свойство для сериализации в dict

    Свойство `dict` обеспечивает сериализацию:
    - Использует алиасы полей (если они заданы)
    - Исключает поля со значением None
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        loc_by_alias=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
        # extra="allow",
    )

    @property
    def dict(
        self,
    ) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            exclude_none=True,
        )
