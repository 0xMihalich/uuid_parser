from hashlib import md5, sha1
from json import dumps
from struct import unpack

from .enums import UUIDVersion, UUIDVariant
from .errors import UUIDVerionError
from .info import UUIDInfo, UUIDDict
from .struct import UUIDStruct
from .time import change_time
from .type_conv import to_bytes
from .var_seq import get_variant_sequence


_var_bits: dict = {
    UUIDVariant(0): "0",
    UUIDVariant(1): "10",
    UUIDVariant(2): "110",
    UUIDVariant(3): "111",
}


def get_version(uuid: UUIDStruct) -> int:
    """Получить номер версии UUID."""

    return int(uuid.time_hi_and_version[0], 16)


def change_version(uuid_str: str, uuid_info: UUIDInfo, uuid_dict: UUIDDict, version: int,) -> str:
    """Изменить версию UUID."""

    if uuid_info.version.name in ('Nil_UUID', 'IUnknown_COM', 'Max_UUID',):
        raise UUIDVerionError("Can't change version for special UUID.")
    elif uuid_info.version.name in ('Namespace_Name_MD5', 'Namespace_Name_SHA1',):
        raise UUIDVerionError("Can't change version from Hashed UUID.")
    elif uuid_info.version.name == 'Random' and version not in (3, 5,):
        raise UUIDVerionError("Random UUID must be changed to Hashed UUID only.")
    elif version == 4:
        raise UUIDVerionError("Can't change version to Random UUID.")
    
    if not isinstance(version, int):
        raise UUIDVerionError("Version must be integer.")
    elif version in (0, 15,):
        raise UUIDVerionError("Can't change version to Nil UUID / Max UUID.")
    elif version not in UUIDVersion.values():
        raise UUIDVerionError("Unknown UUID version.")
    elif version == uuid_info.version.value:
        raise UUIDVerionError("Same UUID version.")
    
    if version not in (3, 5,):
        uuid = UUIDStruct.from_uuidstr(uuid_str[:14] + hex(version)[2:] + uuid_str[15:])
        varseq = get_variant_sequence(uuid)

        return change_time(uuid, version, varseq, uuid_info.time,)
    
    namespace_name: bytes = to_bytes(uuid_str) + bytes(dumps(uuid_dict, ensure_ascii=False,), "utf-8")

    if version == 3:
        uuid_hash: bytes = md5(namespace_name).digest()
    elif version == 5:
        uuid_hash: bytes = sha1(namespace_name).digest()[:16]


    def _var_change(block: int) -> str:

        bit_block: str = bin(block)[2:].zfill(16)
        var_bits: str = _var_bits[uuid_info.variant]

        return hex(int(var_bits + bit_block[len(var_bits):], 2))[2:].zfill(4)

    
    hash_uuid: str = ("-".join(block.hex() if num != 3 else _var_change(block)
                             for num, block in enumerate(unpack("4s2s2sH6s", uuid_hash))))

    return hash_uuid[:14] + hex(version)[2:] + hash_uuid[15:]
