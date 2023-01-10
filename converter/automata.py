import spot
from typing import List
from collections import deque


class Automata:
    def __init__(self, f):
        self.non_empty_states = []
        self.aut = spot.translate(f, "BA")
        self.initial = -1
        self.acc = []
        self.config = []
        self.rej = []

        assert not self.aut.is_empty()
        lines = self.aut.to_str("lbtt").split("\n")[1:]
        self._set_config(lines)

    def _set_config(self, lines: List[str]):
        format_lines = self._format_lines(lines)
        reject_state = len(format_lines)

        flag = False
        for st_lines in format_lines:
            first_line = st_lines[0].split(" ")
            state_label = int(first_line[0])
            if len(first_line) >= 2 and first_line[1] == "1":
                self.initial = state_label
            if len(first_line) >= 3 and first_line[2] == "-1":
                self.acc.append(state_label)
            config_dict = {
                "zero": -1,
                "one": -1,
            }
            for transition in st_lines[1:]:
                str_list = transition.split(" ")
                if len(str_list) == 3 and str_list[1] == "!" and str_list[2] == '"p"':
                    config_dict["zero"] = int(str_list[0])
                    continue
                if len(str_list) == 2 and str_list[1] == '"p"':
                    config_dict["one"] = int(str_list[0])
                    continue
                assert len(str_list) == 2 and str_list[1] == "t"
                config_dict["zero"] = int(str_list[0])
                config_dict["one"] = int(str_list[0])

            if config_dict["zero"] == -1:
                config_dict["zero"] = reject_state
                flag = True
            if config_dict["one"] == -1:
                config_dict["one"] = reject_state
                flag = True
            self.config.append(config_dict)

        if flag:
            self.config.append({"zero": reject_state, "one": reject_state})
            assert len(self.config) == reject_state + 1
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

    def is_deterministic(self):
        return len(self.acc) == 1 and not self.initial == -1

    def get_config(self, index):
        assert len(self.config) > index
        return self.config[index]

    # self.rejectはupdateしないため, この関数使用後はrejectが意味をみたない
    def reverse(self):
        self.reject = None

        initials = sorted(self.acc)
        acc_state = self.initial
        nfa_config = [{"zero": [], "one": []} for cf in self.config]
        for i, cf in enumerate(self.config):
            nfa_config[cf["zero"]]["zero"].append(i)
            nfa_config[cf["one"]]["one"].append(i)
        queue = deque()
        initial_states = "|".join([str(init) for init in initials])
        queue.append(initial_states)
        states_config = {}
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
            zero_dsts.sort()
            one_dsts.sort()
            zero_dsts_str = "|".join([str(item) for item in zero_dsts])
            one_dsts_str = "|".join([str(item) for item in one_dsts])
            queue.extend([zero_dsts_str, one_dsts_str])
            states_config[states_str] = {"zero": zero_dsts_str, "one": one_dsts_str}

        state_list = list(states_config.keys())
        self.config = []
        self.acc = []
        for i, st in enumerate(state_list):
            # 初期, 受理状態を更新
            nums = [int(st) for st in st.split("|")]
            if acc_state in nums:
                self.acc.append(i)
            if st == initial_states:
                self.initial = i

            zero_index = state_list.index(states_config[st]["zero"])
            one_index = state_list.index(states_config[st]["one"])
            self.config.append({"zero": zero_index, "one": one_index})

        # zero_dsts = [for ]

        # configs = [for item in self.config]

    # def output_twa(self):
    #     bdict = spot.make_bdd_dict()
    #     aut = spot.make_twa_graph(bdict)
    #     p = buddy.bdd_ithvar(aut.register_ap("0"))
    #     notp = buddy.bdd_ithvar(aut.register_ap("1"))

    #     aut.new_states(len(self.config))
    #     assert self.initial >= 0
    #     aut.set_init_state(self.initial)
    #     for i, edges in enumerate(self.config):
    #         aut.new_edge(i, edges["zero"], p)
    #         aut.new_edge(i, edges["one"], ~p)
    #     return aut


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
