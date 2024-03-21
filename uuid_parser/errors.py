class UUIDParserError(Exception):
    """Базовый класс ошибки."""


class UUIDTimeError(UUIDParserError):
    """Ошибка получения времени генерации."""


class UUIDVariantError(UUIDParserError):
    """Ошибка UUID variant."""


class UUIDVerionError(UUIDParserError):
    """Неизвестная версия UUID."""


class UUIDNotNilError(UUIDVerionError):
    """Получен не Nil UUID."""


class UUIDNotMaxError(UUIDVerionError):
    """Получен не Max UUID."""
