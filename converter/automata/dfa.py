from typing import List
from dataclasses import dataclass


@dataclass
class DFAutomata:
    initial: int
    config: List[dict[str, int]]
    acc: List[int]
    # def __init__(self, initial: int, acc: List[int], config: List[dict[str, int]]):
    #     self.config = config
    #     self.initial = initial
    #     self.acc = acc

    # def get_config(self, index):
    #     assert index < len(self.config) and index > -1
    #     return self.config[index]
