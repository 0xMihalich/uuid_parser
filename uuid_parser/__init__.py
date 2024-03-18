from datetime import datetime
from re import compile, IGNORECASE, Pattern
from typing import Dict, Optional, Union

from .enums import UUIDVariant, UUIDVersion
from .errors import UUIDNotMaxError, UUIDNotNilError, UUIDParserError, UUIDVerionError
from .info import get_secret, UUIDInfo, UUIDDict
from .struct import UUIDStruct
from .time import get_time
from .var_seq import get_variant_sequence, UUIDVarSeq
from .version import get_version


__author__  = "0xMihalich"
__version__ = "0.1.1"
__date__    = "2024-03-18 02:19:15"


class UUIDParser:
    """Вывод информации о UUID."""

    pattern: Pattern = compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$',
                               IGNORECASE,)

    def __init__(self: "UUIDParser",
                 uuid_str: str,) -> None:
        """Инициализация класса."""

        if not isinstance(uuid_str, str):
            raise UUIDParserError(f"UUID must be string, not a {type(uuid_str)}.")
        elif not bool(self.pattern.match(uuid_str)):
            raise UUIDParserError("UUID string not valid.")

        self.uuid: UUIDStruct = UUIDStruct.from_uuidstr(uuid_str)
        self.version: int = get_version(self.uuid)
        self.varseq: UUIDVarSeq = get_variant_sequence(self.uuid)

        if self.varseq.variant.value == 0 and self.uuid.int != 0 and self.varseq.clock_seq_low <= 13:
            self.version = 1.5
        
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

    def __str__(self: "UUIDParser") -> str:
        """Строковое представление класса."""

        _num: int = len(self.dict) - 1
        col0: int = 64
        col1: int = 19
        col2: int = 44

        version: str = f"{type(self).__name__} v{__version__} result"
        header: str = f"┌{'─' * col0}┐\n│{version: ^{col0}}│\n╞{'═' * col0}╡\n"
        border: str = f"│{'-' * col1}│{'-' * col2}│\n"
        footer: str = f"└{'─' * col1}┴{'─' * col2}┘"

        string: str = header

        for num, cols in enumerate(self.dict.items()):
            _col1, _col2 = cols
            string += f"│{_col1: ^{col1}}│{_col2: ^{col2}}│\n"
            string += footer if num == _num else border

        return string

    def __repr__(self: "UUIDParser") -> str:
        """Строковое представление класса для интерпретатора."""

        return self.__str__()
