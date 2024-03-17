from .struct import UUIDStruct


def get_version(uuid: UUIDStruct) -> int:
    """Получить номер версии UUID."""

    return int(uuid.time_hi_and_version[0], 16)
