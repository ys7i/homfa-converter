from dataclasses import dataclass
from enum import Enum
from typing import List


class AMValue(Enum):
    TOP = 0
    BOTTOM = 1
    NONE = 3


@dataclass
class TestCase:
    formula: str
    pair: List[tuple[List[bool], AMValue]]


TEST_CASES = [
    TestCase(
        formula="p & F(!p & Fp)",
        pair=[
            ([True], AMValue.NONE),
            ([True, False], AMValue.NONE),
            ([True, True], AMValue.NONE),
            ([True, True, True], AMValue.NONE),
            ([True, True, False], AMValue.NONE),
            ([True, True, False, True], AMValue.TOP),
            ([True, True, False, False], AMValue.NONE),
            ([True, True, False, False, False], AMValue.NONE),
            ([True, True, False, False, True], AMValue.TOP),
            ([False], AMValue.BOTTOM),
        ],
    ),
    TestCase(
        formula="(!p W 0) xor Xp",
        pair=[
            ([True], AMValue.NONE),
            ([True, False], AMValue.BOTTOM),
            ([True, True], AMValue.TOP),
            ([False], AMValue.NONE),
            ([False, True], AMValue.TOP),
            ([False, False], AMValue.NONE),
            ([False, False, False], AMValue.NONE),
            ([False, False, False, False], AMValue.NONE),
        ],
    ),
    TestCase(
        formula="(p U !p) M F(!Fp xor Gp)",
        pair=[
            ([True], AMValue.NONE),
            ([True, False], AMValue.NONE),
            ([True, False, True], AMValue.NONE),
            ([True, False, False], AMValue.NONE),
            ([True, True, False], AMValue.NONE),
            ([False], AMValue.NONE),
            ([False, True], AMValue.NONE),
            ([False, True, False], AMValue.NONE),
            ([False, True, True], AMValue.NONE),
            ([False, False, True], AMValue.NONE),
        ],
    ),
    TestCase(
        formula="XFp -> X(((p xor X(0)) W 0) & ((p & Gp) <-> X(p U p)))",
        pair=[
            ([True], AMValue.NONE),
            ([True, False], AMValue.NONE),
            ([True, False, True], AMValue.BOTTOM),
            ([True, False, False], AMValue.NONE),
            ([True, True, False], AMValue.BOTTOM),
            ([False], AMValue.NONE),
            ([False, True], AMValue.NONE),
            ([False, True, False], AMValue.BOTTOM),
            ([False, True, True], AMValue.NONE),
            ([False, False, True], AMValue.BOTTOM),
        ],
    ),
    TestCase(
        formula="p0 & F(!p1)",
        pair=[
            ([True, False], AMValue.TOP),
            ([True, True], AMValue.NONE),
            ([True, True, True, True], AMValue.NONE),
            ([True, True, True, True, True, True], AMValue.NONE),
            ([True, True, True, False], AMValue.TOP),
            ([False, True], AMValue.BOTTOM),
        ],
    ),
    TestCase(
        formula="p0 & F(!p1 & Fp2)",
        pair=[
            ([True, False, True], AMValue.TOP),
            ([True, False, False], AMValue.NONE),
            ([True, False, False, False, False, False], AMValue.NONE),
            ([True, True, False], AMValue.NONE),
            ([True, False, False, False, False, True], AMValue.TOP),
            ([True, False, False, False, False, False, True, True, True], AMValue.TOP),
            ([True, True], AMValue.NONE),
            ([False, True, True], AMValue.BOTTOM),
            ([False, False, True], AMValue.BOTTOM),
        ],
    ),
    TestCase(
        formula="!(p0 & F(!p1 & Fp2)) | !(p1 & F(!p0))",
        pair=[
            ([False, True, True], AMValue.TOP),
        ],
    ),
]
