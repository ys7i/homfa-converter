from typing import List
from collections import deque


class DFAutomata:
    def __init__(self, initial: int, acc: List[int], config: List[dict[str, int]]):
        self.config = config
        self.initial = initial
        self.acc = acc

    def get_config(self, index):
        assert index < len(self.config) and index > -1
        return self.config[index]

    def reverse(self):
        assert self.config is not None
        self.reject = None
        initials = sorted(self.acc)
        acc_state = self.initial
        nfa_config = [{"zero": [], "one": []} for _ in self.config]
        reject_state = -1
        for i, cf in enumerate(self.config):
            nfa_config[cf["zero"]]["zero"].append(i)
            nfa_config[cf["one"]]["one"].append(i)
        for cf in nfa_config:
            if len(cf["zero"]) == 0:
                reject_state = len(nfa_config)
                cf["zero"].append(reject_state)
            if len(cf["one"]) == 0:
                reject_state = len(nfa_config)
                cf["one"].append(reject_state)
        if reject_state != -1:
            nfa_config.append({"zero": [reject_state], "one": [reject_state]})
        return get_dfa(initials, nfa_config, [acc_state], False)


def get_dfa(
    initials: List[int],
    nfa_config: List[dict[str, List[int]]],
    acc_state: List[int],
    acc_all_condition: bool,  # 非決定な複数のstateのうちすべてがacc_stateにあるときのみacceptとするかどうか
) -> DFAutomata:
    queue = deque()
    initial_states = "|".join([str(init) for init in initials])
    queue.append(initial_states)
    states_config: dict[str, dict[str, str]] = {}
    if len(initials) == 0:
        return DFAutomata(0, [], [{"zero": 0, "one": 0}])
    # 0と1の遷移先を求める
    while len(queue) > 0:
        states_str = queue.popleft()
        states = [int(str_st) for str_st in states_str.split("|")]
        if states_str in states_config:
            continue
        zero_dsts = []
        one_dsts = []
        for st in states:
            zero_dsts.extend(nfa_config[st]["zero"])
            one_dsts.extend(nfa_config[st]["one"])
        zero_dsts = sorted(list(set(zero_dsts)))
        one_dsts = sorted(list(set(one_dsts)))
        zero_dsts_str = "|".join([str(item) for item in zero_dsts])
        one_dsts_str = "|".join([str(item) for item in one_dsts])
        queue.extend([zero_dsts_str, one_dsts_str])
        states_config[states_str] = {"zero": zero_dsts_str, "one": one_dsts_str}

    state_list = list(states_config.keys())
    dfa_config = []
    acc = []
    initial = -1
    for i, st in enumerate(state_list):
        # 初期, 受理状態を更新
        nums = [int(st) for st in st.split("|")]
        # numsのうちすべてがacc_stateにある必要がある
        if acc_all_condition:
            if all([num in acc_state for num in nums]):
                acc.append(i)
        else:
            for ast in acc_state:
                if ast in nums:
                    acc.append(i)
                    break
        if st == initial_states:
            initial = i

        zero_index = state_list.index(states_config[st]["zero"])
        one_index = state_list.index(states_config[st]["one"])
        dfa_config.append({"zero": zero_index, "one": one_index})
    assert initial != -1
    return DFAutomata(initial, acc, dfa_config)


class NFAutomata:
    def __init__(self, f):
        self.non_empt_states = []
        self.aut = f.translate("small", "buchi", "sbacc")
        self.initial = -1
        self.acc = []
        self.config = []
        assert not self.aut.is_empty()
        lines = self.aut.to_str("lbtt").split("\n")[1:]
        self._set_config(lines)

    def _set_config(self, lines: List[str]):
        self.config = []
        format_lines = self._format_lines(lines)
        reject_state = -1
        for st_lines in format_lines:
            first_line = st_lines[0].split(" ")
            state_label = int(first_line[0])
            if len(first_line) >= 2 and first_line[1] == "1":
                self.initial = state_label
            if len(first_line) >= 3 and first_line[2] == "-1":
                self.acc.append(state_label)
            config_dict: dict[str, List[int]] = {
                "zero": [],
                "one": [],
            }
            for transition in st_lines[1:]:
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

    def _format_lines(self, lines: List[str]):
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

    # def get_reverse(self) -> DFAutomata:

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
