import unittest
from typing import List
import re
from converter.manager import manager
from tests.test_cases import AMValue, TEST_CASES


class AutomataForTest:
    def __init__(self, aut_lines: List[str]):
        self.bottom = []
        self.top = []
        self.config = {}
        for line in aut_lines:
            state = 0
            if line.startswith(">"):
                result = self.get_group_str(line, r"^>(\d+)")
                assert result is not None
                self.initial = int(result)

            top_state = self.get_group_str(line, r"^>?(\d+)top")
            if top_state is not None:
                state = int(top_state)
                self.top.append(state)
            else:
                bottom_state = self.get_group_str(line, r"^>?(\d+)bottom")
                if bottom_state is not None:
                    state = int(bottom_state)
                    self.bottom.append(state)
                else:
                    state = self.get_group_str(line, r"^>?(\d+)")
                    assert state is not None
                    state = int(state)
            splited_line = line.split()
            self.config[str(state)] = {
                "0": int(splited_line[1]),
                "1": int(splited_line[2]),
            }

    def get_group_str(self, target_str: str, regexp):
        result = re.match(regexp, target_str)
        if result is None:
            return None
        else:
            return result.groups()[0]

    def run(self, input) -> AMValue:
        state = self.initial
        for value in input:
            if value:
                state = self.config[str(state)]["1"]
            else:
                state = self.config[str(state)]["0"]
        if int(state) in self.top:
            return AMValue.TOP
        elif int(state) in self.bottom:
            return AMValue.BOTTOM
        else:
            return AMValue.NONE


class TestExecutor(unittest.TestCase):
    def test_forward(self):
        for case in TEST_CASES:
            aut = manager.convert_formula(case.formula, False)
            aut_lines = manager.convert_aut_to_str(aut)
            aut_for_test = AutomataForTest(aut_lines)
            for pair in case.pair:
                am_value = aut_for_test.run(pair[0])
                self.assertEqual(am_value, pair[1])

    def test_reverse(self):
        for case in TEST_CASES:
            aut = manager.convert_formula(case.formula, True)
            aut_lines = manager.convert_aut_to_str(aut)
            aut_for_test = AutomataForTest(aut_lines)
            for pair in case.pair:
                am_value = aut_for_test.run(reversed(pair[0]))
                self.assertEqual(am_value, pair[1])
