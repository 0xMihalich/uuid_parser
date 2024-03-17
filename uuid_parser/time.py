from datetime import datetime
from typing import Optional

from .struct import UUIDStruct
from .version import get_version


def get_time(uuid: UUIDStruct,
             version: Optional[int] = None,) -> Optional[datetime]:
    """Определить время генерации если это возможно."""

    if not version:
        version: int = get_version(uuid)
    
    timestamp: Optional[float] = None

    if version == 1:
        timestamp: float = (int((uuid.time_hi_and_version[1:] +
                                 uuid.time_mid +
                                 uuid.time_low), 16) -
                                 0x1b21dd213814000) * 1e2 / 1e9
    elif version == 2:
        timestamp: float = (int((uuid.time_hi_and_version[1:] +
                                 uuid.time_mid) + "".zfill(8), 16) -
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
        if timestamp < 0:                             # заплатка для не правильных uuid, созданных мной для тестов.
            timestamp = 0.0                           # можно убрать чтобы сразу рейзило ошибку
        elif timestamp > 3e10:                        # заплатка для зарезервированных gpt guid, в которых была найдена невалидная метка времени
            return datetime(9999, 12, 31, 23, 59, 59) # можно убрать чтобы сразу рейзило ошибку
        return datetime.fromtimestamp(timestamp)
