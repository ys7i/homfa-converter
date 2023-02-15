from typing import List
from dataclasses import dataclass


@dataclass
class Automata3:
    initial: int
    config: List[dict[str, List[int]]]
    top: List[int]
    bottom: List[int]


# class Automata3:
#     def __init__(self):
#         self.initial = -1
#         self.top = []
#         self.bottom = []
#         self.config = []

#     def set_initial(self, initial):
#         self.initial = initial

#     def push_config(self, config):
#         self.config.append(config)
#         return len(self.config) - 1

#     def set_config(self, index: int, zero: int, one: int):
#         self.config[index] = {"zero": zero, "one": one}

#     def push_top(self, state):
#         self.top.append(state)

#     def push_bottom(self, state):
#         self.bottom.append(state)
