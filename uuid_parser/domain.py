from .var_seq import UUIDVarSeq


_domains: dict = {
    0: "Person",
    1: "Group",
    2: "Organization",
}


def get_domain(varseq: UUIDVarSeq) -> str:
    """Определить тип local domain для UUIDv2."""

    domain: int = varseq.clock_seq_low

    return f'{domain} [{_domains.get(domain, "Custom")}]'
