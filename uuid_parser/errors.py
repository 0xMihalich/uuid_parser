class UUIDParserError(Exception):
    """Базовый класс ошибки."""


class UUIDTimeError(UUIDParserError):
    """Ошибка получения времени генерации."""


class UUIDVariantError(UUIDParserError):
    """Ошибка UUID variant."""


class UUIDVersionError(UUIDParserError):
    """Неизвестная версия UUID."""


class UUIDNotNilError(UUIDVersionError):
    """Получен не Nil UUID."""


class UUIDNotMaxError(UUIDVersionError):
    """Получен не Max UUID."""
