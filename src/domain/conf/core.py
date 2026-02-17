# coding utf-8

from functools import lru_cache

from typing import (
    Any,
    Generator,
    Type,
)

from ..conf.envs import (
    DevConfEnv,
    ProdConfEnv,
    TestConfEnv,
)

from ..entities.core import IConfEnv

from ..typing import TConf


env: TConf = IConfEnv().app_env


class AppConf:
    """Фабрика конфигураций приложения для разных окружений.

    Класс реализует паттерн Factory для динамического выбора
    и загрузки конфигурации в зависимости от текущего окружения.
    Использует кэширование для оптимизации повторных запросов.

    Основные возможности:
    - Автоматический выбор конфигурации по текущему окружению
    - Ленивая загрузка конфигураций
    - Кэширование результатов
    - Единая точка доступа ко всем конфигурациям

    Атрибуты:
        _env (TConf): Текущее окружение (dev/prod/test)
    """

    def __init__(
        self,
        env: TConf = env,
    ) -> None:
        """Инициализация фабрики конфигураций.

        Args:
            env (TConf): Текущее окружение (по умолчанию берется из переменных окружения)
        """
        self._env = env

    @lru_cache
    def __call__(
        self,
    ) -> Type[Any]:
        """Получение конфигурации для текущего окружения (с кэшированием).

        Returns:
            Type[Any]: Класс конфигурации для текущего окружения

        Raises:
            EnvironmentError: Если окружение не поддерживается
        """
        return next(
            getattr(self, self._env),
        )

    @property
    def dev(
        self,
    ) -> Generator[dict[str, Any], Any, None]:
        """Генератор конфигурации для development окружения.

        Yields:
            DevConfEnv: Конфигурация development окружения

        Пример использования:
            >>> conf = next(AppConf().dev)
        """
        yield DevConfEnv()

    @property
    def prod(
        self,
    ) -> Generator[dict[str, Any], Any, None]:
        """Генератор конфигурации для production окружения.

        Yields:
            ProdConfEnv: Конфигурация production окружения

        Пример использования:
            >>> conf = next(AppConf().prod)
        """
        yield ProdConfEnv()

    @property
    def test(
        self,
    ) -> Generator[dict[str, Any], Any, None]:
        """Генератор конфигурации для test окружения.

        Yields:
            TestConfEnv: Конфигурация test окружения

        Пример использования:
            >>> conf = next(AppConf().test)
        """
        yield TestConfEnv()


app_conf = AppConf()
