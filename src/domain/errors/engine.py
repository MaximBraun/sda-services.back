# coding utf-8


class EngineError(NotImplementedError):
    """Raised when a required method is not implemented in a subclass."""

    def __init__(
        self,
        cls_name: str,
    ) -> None:
        super().__init__(
            f"{cls_name}: initialization must be implemented in a subclass.",
        )
