from typing import NamedTuple, Optional

from .struct import UUIDStruct
from .enums import UUIDVariant


_variants: dict = {
    "0":   UUIDVariant(0),
    "10":  UUIDVariant(1),
    "110": UUIDVariant(2),
    "111": UUIDVariant(3),
}


class UUIDVarSeq(NamedTuple):
    """Структура clock_seq."""

    variant:       UUIDVariant
    clock_seq_hi:  int
    clock_seq_low: int


def get_variant_sequence(uuid: UUIDStruct) -> UUIDVarSeq:
    """Распарсить UUID.clock_seq_hi_and_reserved_clock_seq_low."""

    uuid_varseq: str = uuid.clock_seq_hi_and_reserved_clock_seq_low
    var_seq_hi: str  = bin(int(uuid_varseq[:2], 16))[2:].zfill(4)

    pos: int = 0
    variant: Optional[UUIDVariant] = None

    while not variant:
        pos += 1
        variant = _variants.get(var_seq_hi[:pos])

    clock_seq_hi: int  = int("0b0" + var_seq_hi[pos:], 2)
    clock_seq_low: int = int(uuid_varseq[2:], 16)

    return UUIDVarSeq(variant, clock_seq_hi, clock_seq_low,)
