from datetime import datetime
from typing import Dict, NamedTuple, Optional, Union

from .domain import get_domain
from .enums import UUIDVersion, UUIDVariant
from .struct import UUIDStruct
from .var_seq import UUIDVarSeq


class UUIDInfo(NamedTuple):
    """Информация о UUID объекте."""

    version:    UUIDVersion
    variant:    UUIDVariant
    time:       Optional[datetime]
    secret:     Dict[str, Union[int, str]]


def get_secret(uuid: UUIDStruct,
               ver: int,
               varseq: UUIDVarSeq,) -> Dict[str, Union[int, str]]:
    """Получить secret."""

    secret: dict = {}

    if ver in (1, 6,):
        secret["MAC Address"] = ":".join(uuid.node[_i:_i + 2].upper()
                                         for _i in range(0, 12, 2))
        secret["Clock Sequence"] = (int(hex(varseq.clock_seq_hi) + 
                                      hex(varseq.clock_seq_low)[2:], 16))
    elif ver == 2:
        secret["MAC Address"] = ":".join(uuid.node[_i:_i + 2].upper()
                                         for _i in range(0, 12, 2))
        secret["Clock Sequence"] = varseq.clock_seq_hi
        secret["Local Domain"] = get_domain(varseq)
        secret["Unique ID"] = int(uuid.time_low, 16)
    elif ver == 3:
        secret["MD5 Hash Pattern"] = (f"{uuid.time_low}{uuid.time_mid}?"
                                      f"{uuid.time_hi_and_version[1:]}?"
                                      f"{uuid.clock_seq_hi_and_reserved_clock_seq_low[1:]}"
                                      f"{uuid.node}")
    elif ver == 4:
        secret["Unique Key"] = int(f"{uuid.time_low}{uuid.time_mid}"
                                   f"{uuid.time_hi_and_version[1:]}"
                                   f"{uuid.clock_seq_hi_and_reserved_clock_seq_low[1:]}"
                                   f"{uuid.node}", 16)
    elif ver == 5:
        secret["SHA1 Hash Pattern"] = (f"{uuid.time_low}{uuid.time_mid}?"
                                       f"{uuid.time_hi_and_version[1:]}?"
                                       f"{uuid.clock_seq_hi_and_reserved_clock_seq_low[1:]}"
                                       f"{uuid.node}")
    elif ver == 7:
        secret["Unique Key"] = int(f"{uuid.time_hi_and_version[1:]}"
                                   f"{uuid.clock_seq_hi_and_reserved_clock_seq_low[1:]}"
                                   f"{uuid.node}", 16)
    elif ver == 8:
        secret["Unique Key"] = int(f"{uuid.clock_seq_hi_and_reserved_clock_seq_low[3]}"
                                   f"{uuid.node}", 16)
    
    return secret
