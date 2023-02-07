from dataclasses import dataclass
from typing import List


@dataclass
class IntegratedAutomata:
    initial: int
    aps: List[str]
    acc: List[int]
    config: List[dict[str, int]]
