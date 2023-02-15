from collections import deque
from converter.automata.automata3 import Automata3

from converter.automata.dfa import DFAutomata


def product_aut(tf: DFAutomata, ff: DFAutomata):
    """
    tfの受理状態をtop,
    ffの受理状態をbottomとして3値automatonを合成
    """
    queue = deque()
    state_dict = {}

    tf_init = tf.initial
    ff_init = ff.initial
    queue.append(f"{tf_init}|{ff_init}")
    while len(queue) > 0:
        item = queue.popleft()
        if item in state_dict:
            continue
        [tf_state, ff_state] = item.split("|")
        tf_config = tf.config[int(tf_state)]
        ff_config = ff.config[int(ff_state)]
        zero_dst = f"{tf_config['zero']}|{ff_config['zero']}"
        one_dst = f"{tf_config['one']}|{ff_config['one']}"
        state_dict[item] = {
            "zero": zero_dst,
            "one": one_dst,
        }
        queue.append(zero_dst)
        queue.append(one_dst)

    state_map = {}
    aut3_config = []
    for str in state_dict.keys():
        aut3_config.append({"zero": -1, "one": -1})
        index = len(aut3_config) - 1
        [tf_state, ff_state] = str.split("|")
        state_map[str] = index

    initial = state_map[f"{tf.initial}|{ff.initial}"]

    top = []
    bottom = []
    for str in state_dict.keys():
        [tf_state, ff_state] = str.split("|")
        if int(tf_state) in tf.acc:
            top.append(state_map[str])
        if int(ff_state) in ff.acc:
            bottom.append(state_map[str])
        aut3_config[state_map[str]] = {
            "zero": state_map[state_dict[str]["zero"]],
            "one": state_map[state_dict[str]["one"]],
        }

    return Automata3(initial=initial, config=aut3_config, top=top, bottom=bottom)
