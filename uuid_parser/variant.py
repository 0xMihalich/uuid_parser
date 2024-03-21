from typing import Dict, List

from .errors import UUIDVariantError
from .struct import UUIDStruct
from .var_seq import UUIDVarSeq


_variants: Dict[int, str] = {
    0: "0",
    1: "10",
    2: "110",
    3: "111",
}


def change_variant(uuid: UUIDStruct, varseq: UUIDVarSeq, variant: int,) -> str:
    """Изменить UUID variant. Возвращает UUID строку."""

    uuid_variant: int = varseq.variant.value

    if uuid_variant == variant:
        raise UUIDVariantError("Variant value is same.")
    elif not isinstance(variant, int):
        raise UUIDVariantError("Variant value is not integer.")
    
    variant_bits: str = _variants.get(variant)

    if variant is None:
        raise UUIDVariantError("Variant value error.")
    
    block_list: List[str] = list(uuid)
    clock_seq_bits: str = bin(int(block_list[3], 16))[2:].zfill(16)

    block_list[3] = (int(variant_bits + clock_seq_bits[len(variant_bits):], 2)
                    .to_bytes(2, "big").hex())
    
    return "-".join(block_list)
