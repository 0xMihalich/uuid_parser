from datetime import datetime, timedelta
from typing import Optional

from .errors import UUIDTimeError
from .struct import UUIDStruct
from .version import get_version


def get_time(uuid: UUIDStruct,
             version: Optional[int] = None,) -> Optional[datetime]:
    """Определить время генерации если это возможно."""

    if not version:
        version: int = get_version(uuid)
    
    timestamp: Optional[float] = None

    try:
        if version == 1.5:
            timestamp = int(uuid.time_low + uuid.time_mid, 16) * 4
            
            return datetime.fromtimestamp(0x12ce1960) + timedelta(microseconds=timestamp)
        
        if version == 1:
            timestamp: float = (int((uuid.time_hi_and_version[1:] +
                                    uuid.time_mid +
                                    uuid.time_low), 16) -
                                    0x1b21dd213814000) * 1e2 / 1e9
        elif version == 2:
            timestamp: float = (int((uuid.time_hi_and_version[1:] +
                                    uuid.time_mid) +
                                    "".zfill(8), 16) -
                                    0x1b21dd213814000) * 1e2 / 1e9
        elif version == 6:
            timestamp: float = (int((uuid.time_low + 
                                    uuid.time_mid + 
                                    uuid.time_hi_and_version[1:]), 16) -
                                    0x1b21dd213814000) * 1e2 / 1e9
        elif version == 7:
            timestamp: float = (uuid.int >> 80) / 1e3
        elif version == 8:
            timestamp: float = ((uuid.int >> 80) * 1e6 -
                                (-((uuid.int >> 64) &
                                0x0FFF) << 8 | ((uuid.int >> 54) &
                                                0xFF) * 10**6 //
                                                1048576)) / 1e9

        if timestamp:
            return datetime.fromtimestamp(0) + timedelta(seconds=timestamp)
        
        return
    except Exception as e:
        raise UUIDTimeError(e)
