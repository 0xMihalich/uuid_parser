from struct import unpack
from typing import List

from .errors import UUIDParserError


def from_1c(uuid_1c: bytes) -> str:
    """Получить UUID строку из формата 1С."""

    if not isinstance(uuid_1c, bytes):
            raise UUIDParserError("1C UUID must be bytes.")
    elif len(uuid_1c) != 16:
        raise UUIDParserError("1C UUID bytes not valid.")

    _uuid: List[bytes] = list(unpack("2s6s2s2s4s", uuid_1c))
    _uuid[0], _uuid[1] = _uuid[1], _uuid[0]

    return "-".join(_bytes.hex() for _bytes in _uuid[::-1])


def to_1c(uuid: str) -> bytes:
    """Преобразовать UUID в формат 1С."""

    if not isinstance(uuid, str):
            raise UUIDParserError("UUID must be string.")
    elif len(uuid) != 36:
            raise UUIDParserError("UUID string not valid.")

    _uuid: List[str] = uuid.split("-")
    _uuid[3], _uuid[4] = _uuid[4], _uuid[3]

    return bytes.fromhex("".join(_str for _str in _uuid[::-1]))
