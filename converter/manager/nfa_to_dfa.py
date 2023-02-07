from collections import deque

from converter.automata.dfa import DFAutomata
from converter.automata.nfa import NFAutomata


def convert_nfa_to_dfa(nfa: NFAutomata) -> DFAutomata:
    return get_dfa(nfa, True)


def get_dfa(
    nfa: NFAutomata,
    acc_all_condition: bool,  # 非決定な複数のstateのうちすべてがacc_stateにあるときのみacceptとするかどうか
) -> DFAutomata:
    queue = deque()
    initial_states = "|".join([str(init) for init in nfa.initial])
    queue.append(initial_states)
    states_config: dict[str, dict[str, str]] = {}
    # 0と1の遷移先を求める
    while len(queue) > 0:
        states_str = queue.popleft()
        states = [int(str_st) for str_st in states_str.split("|")]
        if states_str in states_config:
            continue
        zero_dsts = []
        one_dsts = []
        for st in states:
            zero_dsts.extend(nfa.config[st]["zero"])
            one_dsts.extend(nfa.config[st]["one"])
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
            if all([num in nfa.acc for num in nums]):
                acc.append(i)
        else:
            for ast in nfa.acc:
                if ast in nums:
                    acc.append(i)
                    break
        if st == initial_states:
            initial = i

        zero_index = state_list.index(states_config[st]["zero"])
        one_index = state_list.index(states_config[st]["one"])
        dfa_config.append({"zero": zero_index, "one": one_index})
    assert initial != -1
    return DFAutomata(initial=initial, acc=acc, config=dfa_config)
