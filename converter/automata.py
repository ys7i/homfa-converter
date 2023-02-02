from typing import List
from dfa import get_dfa, DFAutomata
from hoa_parser import parse_hoa


class NFAutomata:
    def __init__(self, f):
        self.aut = f.translate("small", "buchi", "sbacc")
        self.initial = -1
        self.acc = []
        self.config = []
        assert not self.aut.is_empty()
        hoa_lines = self.aut.to_str("hoa").split("\n")
        self._parse_hoa(hoa_lines)
        # lines = self.aut.to_str("lbtt").split("\n")[1:]
        # self._set_config(lines)

    # HOA: v1
    # States: 4
    # Start: 3
    # AP: 3 "p0" "p1" "p2"
    # acc-name: Buchi
    # Acceptance: 1 Inf(0)
    # properties: trans-labels explicit-labels state-acc deterministic
    # properties: stutter-invariant terminal
    # --BODY--
    # State: 0 {0}
    # [t] 0
    # State: 1
    # [2] 0
    # [!2] 1
    # State: 2
    # [!1&2] 0
    # [!1&!2] 1
    # [1] 2
    # State: 3
    # [0&!1&2] 0
    # [0&!1&!2] 1
    # [0&1] 2
    # --END--
    def _parse_hoa(self, lines: List[str]):
        body_index = lines.index("--BODY--")
        header = lines[:body_index]
        body = lines[body_index + 1 : -1]
        parse_hoa(header, body)

    def _set_config(self, lines: List[str]):
        self.config = []
        format_lines = self._format_lines(lines)
        # format_linesの例
        # [
        #     ['0 1 -1', '1 & & p0 ! p1 p2', '2 & & p0 ! p1 ! p2', '3 & p0 p1'],
        #     ['1 0 0 -1', '1 t'],
        #     ['2 0 -1', '1 p2', '2 ! p2'],
        #     ['3 0 -1', '1 & ! p1 pch2', '2 & ! p1 ! p2', '3 p1']
        # ]
        reject_state = -1
        for st_line in format_lines:
            first_line = st_line[0].split(" ")
            state_label = int(first_line[0])
            print(st_line)
            if len(first_line) >= 2 and first_line[1] == "1":
                self.initial = state_label
            if len(first_line) >= 3 and first_line[2] == "-1":
                self.acc.append(state_label)
            config_dict: dict[str, List[int]] = {
                "zero": [],
                "one": [],
            }
            for transition in st_line[1:]:
                str_list = transition.split(" ")
                if len(str_list) == 3 and str_list[1] == "!" and str_list[2] == '"p"':
                    config_dict["zero"].append(int(str_list[0]))
                    continue
                if len(str_list) == 2 and str_list[1] == '"p"':
                    config_dict["one"].append(int(str_list[0]))
                    continue
                assert len(str_list) == 2 and str_list[1] == "t"
                config_dict["zero"].append(int(str_list[0]))
                config_dict["one"].append(int(str_list[0]))

            if len(config_dict["zero"]) == 0:
                reject_state = len(format_lines)
                config_dict["zero"] = [reject_state]
            if len(config_dict["one"]) == 0:
                reject_state = len(format_lines)
                config_dict["one"] = [reject_state]
            self.config.append(config_dict)

        if reject_state != -1:
            assert len(self.config) == reject_state
            self.config.append({"zero": [reject_state], "one": [reject_state]})
        assert self.initial != -1
        assert len(self.acc) > 0
        self.rej = [reject_state]

    # lbtt形式のstringをstateごとの二重配列に変換
    # linesの例
    # [
    #     ['0 1 -1', '1 & & p0 ! p1 p2', '2 & & p0 ! p1 ! p2', '3 & p0 p1'],
    #     ['1 0 0 -1', '1 t'],
    #     ['2 0 -1', '1 p2', '2 ! p2'],
    #     ['3 0 -1', '1 & ! p1 p2', '2 & ! p1 ! p2', '3 p1']
    # ]
    def _format_lines(self, lines: List[str]) -> List[List[str]]:
        new_lines = []
        line_buffer = []
        for line in lines:
            if line == "":
                continue
            if line == "-1":
                new_lines.append(line_buffer)
                line_buffer = []
                continue
            line_buffer.append(line)
        return new_lines

    def swap_acc_rej(self):
        self.acc, self.rej = self.rej, self.acc

    def create_dfa(self) -> DFAutomata:
        return get_dfa([self.initial], self.config, self.acc, True)


class Automata3:
    def __init__(self):
        self.initial = -1
        self.top = []
        self.bottom = []
        self.config = []

    def set_initial(self, initial):
        self.initial = initial

    def push_config(self, config):
        self.config.append(config)
        return len(self.config) - 1

    def set_config(self, index: int, zero: int, one: int):
        self.config[index] = {"zero": zero, "one": one}

    def push_top(self, state):
        self.top.append(state)

    def push_bottom(self, state):
        self.bottom.append(state)
