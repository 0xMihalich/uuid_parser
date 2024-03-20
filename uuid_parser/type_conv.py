from struct import pack, unpack, unpack_from
from typing import List


_STRUCT: str = "%sI2H2s6s"


def to_string(uuid_bytes: bytes) -> str:
    """Перевести байты в uuid строку."""

    variant, *_ = unpack_from("1s", uuid_bytes, 8)
    order: str = "<" if variant.hex()[0] in ("c", "d") else ">"
    
    return "-".join(hex(block)[2:].zfill(8) if num == 0
                    else block.hex() if num in (3, 4) else hex(block)[2:].zfill(4)
                    for num, block in enumerate(unpack(_STRUCT % order, uuid_bytes)))


def to_bytes(uuid_string: str) -> bytes:
    """Перевести uuid строку в байты."""

    uuid_list: List[str] = uuid_string.split("-")
    order: str = "<" if uuid_list[3][0] in ("c", "d") else ">"

    return pack(_STRUCT % order, *(bytes.fromhex(block) if num in (3, 4)
                                   else int(block, 16)
                                   for num, block in enumerate(uuid_list)))
