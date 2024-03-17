from typing import NamedTuple


class UUIDStruct(NamedTuple):
    """Общая структура uuid."""

    time_low: str
    time_mid: str
    time_hi_and_version: str
    clock_seq_hi_and_reserved_clock_seq_low: str
    node: str

    @classmethod
    def from_uuidstr(cls: "UUIDStruct",
                     uuid_string: str,) -> "UUIDStruct":
        """Инициализация из uuid-строки."""
        
        return UUIDStruct(*uuid_string.lower().split("-"))
    
    @property
    def str(self: "UUIDStruct") -> str:
        """Вернуть uuid-строку."""

        return "-".join(self)
    
    @property
    def int(self: "UUIDStruct") -> str:
        """Вернуть uuid как число."""

        return int("".join(self), 16)
