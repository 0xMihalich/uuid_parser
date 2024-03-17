from enum import Enum


_versions: dict = {
    "Nil_UUID": "Nil UUID",
    "Date_MAC": "Date and MAC-address",
    "Date_MAC_DCE": "Date, MAC-address and DCE",
    "Namespace_Name_MD5": "MD5 from Namespace and Name",
    "Random": "Random bytes",
    "Namespace_Name_SHA1": "SHA1 from Namespace and Name",
    "Datesort_MAC": "Sorted Date and MAC-address",
    "Monotonic": "Monotonic",
    "RFC_Native": "RFC Native",
    "Max_UUID": "Max UUID",
}


class UUIDVersion(Enum):
    """Перечисление версий UUID."""

    Nil_UUID: int            = 0
    Date_MAC: int            = 1
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

        return f'UUIDv{self.value} [{_versions.get(self.name, "Unknown")}]'


class UUIDVariant(Enum):
    """Перечисление вариантов UUID."""

    apollo: int    = 0
    standart: int  = 1
    microsoft: int = 2
    reserved: int  = 3

    @property
    def string(self: "UUIDVariant") -> str:

        return f"{self.value} [{self.name.capitalize()}]"
