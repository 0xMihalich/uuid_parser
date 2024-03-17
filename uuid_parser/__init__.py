from datetime import datetime
from re import compile, IGNORECASE, Pattern
from typing import Optional

from .enums import UUIDVariant, UUIDVersion
from .errors import UUIDNotMaxError, UUIDNotNilError, UUIDParserError, UUIDTimeError, UUIDVerionError
from .info import get_secret, UUIDInfo
from .secret import Secret
from .struct import UUIDStruct
from .time import get_time
from .var_seq import get_variant_sequence, UUIDVarSeq
from .version import get_version


_string: str = """Parse result:
-------------
UUID string: '{parser.uuid.str}'

Basic
-----
Version: {parser.info.version.string}
Variant: {parser.info.variant.string}
Generated time: {parser.stime}

Secret
------{parser.secret}"""


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

        if self.version == 0 and self.uuid.int != 0:
            raise UUIDNotNilError(f"{self.uuid.str} have version 0 and not match with Nil UUID.")
        if self.version == 15 and self.uuid.str != "ffffffff-ffff-ffff-ffff-ffffffffffff":
            raise UUIDNotMaxError(f"{self.uuid.str} have max version and not match with Max UUID.")
        elif 8 < self.version < 15:
            raise UUIDVerionError(f"UUIDv{self.version} not supported now.")
        
        try:
            self.time: Optional[datetime] = get_time(self.uuid, self.version,)
        except Exception as e:
            raise UUIDTimeError(e)
        
        if self.version == 0:
            self.varseq: UUIDVarSeq = UUIDVarSeq(UUIDVariant(0), 0, 0,)
        else:
            self.varseq: UUIDVarSeq = get_variant_sequence(self.uuid)
        
        self.stime: str = self.time.strftime("%Y-%m-%d %H:%M:%S") if self.time else "Undefined"
        self.secret: Secret = Secret(get_secret(self.uuid, self.version, self.varseq,))
        self.info: UUIDInfo = UUIDInfo(UUIDVersion(self.version),
                                       self.varseq.variant,
                                       self.time,
                                       dict(self.secret),)

    def __str__(self: "UUIDParser") -> str:
        """Строковое представление класса."""

        return _string.format(parser=self)

    def __repr__(self: "UUIDParser") -> str:
        """Строковое представление класса для интерпретатора."""

        return self.__str__()
