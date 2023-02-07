from typing import List
from dataclasses import dataclass


@dataclass
class NFAutomata:
    initial: List[int]
    config: List[dict[str, List[int]]]
    acc: List[int]
    rej: List[int]
