from typing import List
from dataclasses import dataclass


@dataclass
class NBAutomata:
    initial: int
    config: List[dict[str, List[int]]]
    acc: List[int]
    rej: List[int]
