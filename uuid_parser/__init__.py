from datetime import datetime
from re import compile, IGNORECASE, Pattern
from typing import Dict, Optional, Union
from uuid import UUID

from .database_1c import from_1c, to_1c
from .enums import UUIDVariant, UUIDVersion
from .errors import UUIDNotMaxError, UUIDNotNilError, UUIDParserError, UUIDVerionError
from .info import get_secret, UUIDInfo, UUIDDict
from .struct import UUIDStruct
from .time import change_time, get_time
from .type_conv import to_bytes, to_string
from .var_seq import get_variant_sequence, UUIDVarSeq
from .variant import change_variant
from .version import get_version


__author__  = "0xMihalich"
__version__ = "0.1.4"
__date__    = "2024-03-23 17:27:03"


class UUIDParser:
    """Вывод информации о UUID."""

    pattern: Pattern = compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$',
                               IGNORECASE,)

    def __init__(self: "UUIDParser",
                 uuid: Union[str, bytes, UUID,],) -> None:
        """Инициализация класса."""

        if not isinstance(uuid, Union[str, bytes, UUID,]):
            raise UUIDParserError(f"UUID must be string, bytes or uuid.UUID, not a {type(uuid)}.")
        
        if isinstance(uuid, str):
            if not bool(self.pattern.match(uuid)):
                raise UUIDParserError("UUID string not valid.")
        elif isinstance(uuid, bytes):
            if len(uuid) != 16:
                raise UUIDParserError("UUID bytes not valid.")
            uuid: str = to_string(uuid)
        elif isinstance(uuid, UUID):
            uuid: str = str(uuid)

        self.uuid: UUIDStruct = UUIDStruct.from_uuidstr(uuid)
        self.version: int = get_version(self.uuid)
        self.varseq: UUIDVarSeq = get_variant_sequence(self.uuid)

        if self.varseq.variant.value == 0 and self.uuid.int != 0 and self.varseq.clock_seq_low <= 13:
            self.version = 1.5
        elif self.uuid.str == "00000000-0000-0000-c000-000000000046":
            self.version = None
        
        if self.version == 0 and self.uuid.int != 0:
            raise UUIDNotNilError(f"{self.uuid.str} have version 0 and not match with Nil UUID.")
        elif self.version == 15 and self.uuid.str != "ffffffff-ffff-ffff-ffff-ffffffffffff":
            raise UUIDNotMaxError(f"{self.uuid.str} have max version and not match with Max UUID.")
        elif self.version not in UUIDVersion.values():
            raise UUIDVerionError(f"UUIDv{self.version} not supported now.")
        
        self.time: Optional[datetime] = get_time(self.uuid, self.version,)
        self.secret: Dict[str, Union[int, str]] = get_secret(self.uuid, self.version, self.varseq,)
        
        self.dict: UUIDDict = UUIDDict()
        self.dict.update(self.secret)
        self.dict["UUID"]           = self.uuid.str
        self.dict["Version"]        = UUIDVersion(self.version).string
        self.dict["Variant"]        = UUIDVariant(self.varseq.variant).string
        self.dict["Generated time"] = self.time.strftime("%Y-%m-%d %H:%M:%S") if self.time else "Undefined"

        self.info: UUIDInfo = UUIDInfo(self.dict["Version"],
                                       self.dict["Variant"],
                                       self.time,
                                       self.secret,)

    def __repr__(self: "UUIDParser") -> str:
        """Строковое представление класса для интерпретатора."""

        _num: int = len(self.dict) - 1
        col0: int = 64
        col1: int = 19
        col2: int = 44

        version: str = f"{type(self).__name__} v{__version__} result"
        header: str = f"┌{'─' * col0}┐\n│{version: ^{col0}}│\n╞{'═' * col0}╡\n"
        border: str = f"│{'-' * col1}│{'-' * col2}│\n"
        footer: str = f"└{'─' * col0}┘"

        string: str = header

        for num, cols in enumerate(self.dict.items()):
            _col1, _col2 = cols
            string += f"│{_col1: ^{col1}}│{_col2: ^{col2}}│\n"
            string += footer if num == _num else border

        return string
    
    def __int__(self: "UUIDParser") -> int:
        """Вернуть как Integer."""

        return self.uuid.int

    def __hash__(self: "UUIDParser") -> int:
        """Посчитать hash UUID."""

        return hash(self.uuid.int)

    def __str__(self: "UUIDParser") -> str:
        """Вернуть как UUID строку."""

        return self.uuid.str

    def __bytes__(self: "UUIDParser") -> bytes:
        """Вернуть как Bytes."""

        return to_bytes(self.uuid.str)

    def hex(self: "UUIDParser") -> str:
        """Вернуть как HEX String."""

        return bytes(self).hex().strip("0") or "0"

    def change_variant(self: "UUIDParser", variant: int) -> "UUIDParser":
        """Изменить UUID variant. Возвращает новый объект UUIDParser."""

        return UUIDParser(change_variant(self.uuid, self.varseq, variant,))
    
    def change_time(self: "UUIDParser", time: datetime) -> "UUIDParser":
        """Изменить временную метку UUID. Возвращает новый объект UUIDParser."""

        return UUIDParser(change_time(self.uuid, self.version, self.varseq, time,))
    
    @classmethod
    def from_1c(cls: "UUIDParser", uuid_1c: bytes) -> "UUIDParser":
        """Получить объект UUIDParser из формата 1С UUID."""

        return cls(from_1c(uuid_1c))

    @property
    def to_1c(self: "UUIDParser") -> bytes:
        """Преобразовать объект UUIDParser в формат 1С UUID."""

        return to_1c(str(self))
