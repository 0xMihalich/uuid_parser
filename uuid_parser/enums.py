from enum import Enum
from typing import List, TypeVar, Union


NoneType = TypeVar("NoneType", bound=type(None))

_versions: dict = {
    "Nil_UUID"           : "Nil UUID",
    "Date_MAC"           : "Date and MAC-address",
    "IUnknown_COM"       : "Microsoft COM IUnknown",
    "Apollo_NCS"         : "Apollo Network Computing System",
    "Date_MAC_DCE"       : "Date, MAC-address and DCE",
    "Namespace_Name_MD5" : "MD5 from Namespace and Name",
    "Random"             : "Random bytes",
    "Namespace_Name_SHA1": "SHA1 from Namespace and Name",
    "Datesort_MAC"       : "Sorted Date and MAC-address",
    "Monotonic"          : "Monotonic",
    "RFC_Native"         : "RFC Native",
    "Max_UUID"           : "Max UUID",
}


class UUIDVersion(Enum):
    """Перечисление версий UUID."""

    Nil_UUID: int            = 0
    Date_MAC: int            = 1
    IUnknown_COM: NoneType   = None
    Apollo_NCS: float        = 1.5
    Date_MAC_DCE: int        = 2
    Namespace_Name_MD5: int  = 3
    Random: int              = 4
    Namespace_Name_SHA1: int = 5
    Datesort_MAC: int        = 6
    Monotonic: int           = 7
    RFC_Native: int          = 8
    Max_UUID: int            = 15

    @property
    def string(self: "UUIDVersion") -> str:
        """Отобразить в виде строки."""

        return f'UUIDv{self.value or 0} [{_versions.get(self.name, "Unknown")}]'

    @classmethod
    def values(cls: "UUIDVersion") -> List[Union[int, float,]]:
        """Вернуть список значений."""

        return list(cls._value2member_map_)


class UUIDVariant(Enum):
    """Перечисление вариантов UUID."""

    apollo: int    = 0
    standart: int  = 1
    microsoft: int = 2
    reserved: int  = 3

    @property
    def string(self: "UUIDVariant") -> str:
        """Отобразить в виде строки."""

        return f"{self.value} [{self.name.capitalize()}]"
