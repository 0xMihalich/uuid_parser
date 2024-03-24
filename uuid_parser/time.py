from datetime import datetime, timedelta
from typing import List, Optional, Union

from .errors import UUIDTimeError
from .struct import UUIDStruct
from .var_seq import UUIDVarSeq
from .variant import _variants


def get_time(uuid: UUIDStruct,
             version: Optional[int] = None,) -> Optional[datetime]:
    """Определить время генерации если это возможно."""
  
    timestamp: Optional[float] = None

    try:
        if version == 1.5:
            timestamp: float = (int(uuid.time_low +
                                    uuid.time_mid, 16) * 4 / 1e6 +
                                    0x12ce1960)
        elif version == 1:
            timestamp: float = (int((uuid.time_hi_and_version[1:] +
                                    uuid.time_mid +
                                    uuid.time_low), 16) -
                                    0x1b21dd213814000) / 1e7
        elif version == 2:
            timestamp: float = (int((uuid.time_hi_and_version[1:] +
                                    uuid.time_mid) +
                                    "".zfill(8), 16) -
                                    0x1b21dd213814000) / 1e7
        elif version == 6:
            timestamp: float = (int((uuid.time_low + 
                                    uuid.time_mid + 
                                    uuid.time_hi_and_version[1:]), 16) -
                                    0x1b21dd213814000) / 1e7
        elif version == 7:
            timestamp: float = (uuid.int >> 80) / 1e3
        elif version == 8:
            timestamp: float = ((uuid.int >> 80) * 1e6 -
                                (-((uuid.int >> 64) &
                                0xfff) << 8 | ((uuid.int >> 54) &
                                                0xff) * 10**6 //
                                                1048576)) / 1e9

        if timestamp:
            return datetime.fromtimestamp(0) + timedelta(seconds=timestamp)
        
        return
    except Exception as e:
        raise UUIDTimeError(e)


def change_time(uuid: UUIDStruct,
                uuid_version: Optional[Union[int, float]],
                varseq: UUIDVarSeq,
                time: datetime,) -> str:
    """Изменить временную метку UUID."""

    if not isinstance(time, datetime):
        raise UUIDTimeError("time must be a datetime.")
    
    _stamp: float = (time - datetime.fromtimestamp(0)).total_seconds()
    _version: int = int(uuid.str[14], 16)
    version: str = hex(_version)[2:]
    variant_bits: str = _variants.get(varseq.variant.value)
    uuid_blocks: List[str] = list(uuid)

    if uuid_version in (1, 2, 6,):
        timestamp: int = int(0x1b21dd213814000 + _stamp * 1e7)

        time_low: str = hex(timestamp & 0xffffffff)[2:].zfill(8)
        time_mid: str = hex((timestamp >> 32) & 0xffff)[2:].zfill(4)
        time_hi: str = hex((timestamp >> 48) & 0x0fff)[2:].zfill(4)[1:]

        if uuid_version == 1:
            uuid_blocks[0] = time_low
            uuid_blocks[1] = time_mid
            uuid_blocks[2] = version + time_hi
        elif uuid_version == 2:
            uuid_blocks[1] = time_mid
            uuid_blocks[2] = version + time_hi
        elif uuid_version == 6:
            uuid_blocks[0] = time_hi + time_mid + time_low[0]
            uuid_blocks[1] = time_low[1:5]
            uuid_blocks[2] = version + time_low[5:]

    elif uuid_version == 7:
        timestamp: int = (int(_stamp * 1e3) & 0xffffffffffff) << 80
        time_pattern: str = hex(timestamp)[2:].zfill(32)
        uuid_blocks[0] = time_pattern[:8]
        uuid_blocks[1] = time_pattern[8:12]

    elif uuid_version == 8:
        timestamp_ms, timestamp_ns = divmod(int(_stamp * 1e9), 10**6)
        subsec: int = timestamp_ns * 2**20 // 10**6
        subsec_a: int = subsec >> 8
        subsec_b: int = subsec & 0xff
        uuid_int: int = (timestamp_ms & 0xffffffffffff) << 80
        uuid_int |= subsec_a << 64
        uuid_int |= subsec_b << 54
        time_pattern: str = hex(uuid_int)[2:].zfill(32)
        clock_seq_bits: str = bin(int(time_pattern[16:19] + uuid_blocks[3][-1], 16))[2:].zfill(16)
        uuid_blocks[0] = time_pattern[:8]
        uuid_blocks[1] = time_pattern[8:12]
        uuid_blocks[2] = version + time_pattern[13:16]
        uuid_blocks[3] = (int(variant_bits + clock_seq_bits[len(variant_bits):], 2)
                         .to_bytes(2, "big").hex())

    elif uuid_version == 1.5:
        if _stamp > 1441396706.842621:
            raise UUIDTimeError('for UUIDv1.5 maximum date is "2015-09-05 05:58:26".')
        time_pattern: str = hex(int((_stamp - 0x12ce1960) * 1e6 / 4))[2:].zfill(12)
        uuid_blocks[0] = time_pattern[:8]
        uuid_blocks[1] = time_pattern[8:]

    else:
        raise UUIDTimeError(f"UUIDv{uuid_version or 0} don't have timestamp.")

    return "-".join(uuid_blocks)
