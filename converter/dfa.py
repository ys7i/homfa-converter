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
