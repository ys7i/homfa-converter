from collections import deque
from automata import Automata3
from logging import getLogger
from automata import NFAutomata, DFAutomata
import spot
from typing import List


def convert_formula(formula, is_reversed=False) -> Automata3:
    logger = getLogger(__name__)

    tf = spot.formula(formula)
    ff = spot.formula(f"!({formula})")
    assert tf.is_ltl_formula() and ff.is_ltl_formula()

    tf_aut = NFAutomata(tf)
    ff_aut = NFAutomata(ff)

    tf_aut.swap_acc_rej()
    ff_aut.swap_acc_rej()

    tfd_aut = tf_aut.create_dfa()
    ffd_aut = ff_aut.create_dfa()
    if is_reversed:
        tfd_aut = tfd_aut.reverse()
        ffd_aut = ffd_aut.reverse()
        logger.info("reversed")

    tfd_aut, ffd_aut = ffd_aut, tfd_aut
    aut = product_aut(tfd_aut, ffd_aut)
    return aut


def product_aut(tf: DFAutomata, ff: DFAutomata):
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
        tf_config = tf.get_config(int(tf_state))
        ff_config = ff.get_config(int(ff_state))
        zero_dst = f"{tf_config['zero']}|{ff_config['zero']}"
        one_dst = f"{tf_config['one']}|{ff_config['one']}"
        state_dict[item] = {
            "zero": zero_dst,
            "one": one_dst,
        }
        queue.append(zero_dst)
        queue.append(one_dst)

    state_map = {}
    product_aut = Automata3()
    for str in state_dict.keys():
        index = product_aut.push_config({"zero": -1, "one": -1})
        [tf_state, ff_state] = str.split("|")
        state_map[str] = index

    product_aut.set_initial(state_map[f"{tf.initial}|{ff.initial}"])
    for str in state_dict.keys():
        [tf_state, ff_state] = str.split("|")
        if int(tf_state) in tf.acc:
            product_aut.push_top(state_map[str])
        if int(ff_state) in ff.acc:
            product_aut.push_bottom(state_map[str])
        product_aut.set_config(
            state_map[str],
            state_map[state_dict[str]["zero"]],
            state_map[state_dict[str]["one"]],
        )

    return product_aut


def convert_auto_to_str(aut: Automata3) -> List[str]:
    aut_str = []
    for i, config in enumerate(aut.config):
        buffer_str = ""
        if i == aut.initial:
            buffer_str += ">"
        buffer_str += str(i)
        if i in aut.top:
            buffer_str += "top"
        if i in aut.bottom:
            buffer_str += "bottom"
        buffer_str += f" {config['zero']} {config['one']}"
        aut_str.append(buffer_str)
    return aut_str


def output_config(aut_lines):
    with open("./output_files/config.spec", mode="w") as f:
        for line in aut_lines:
            f.write(line + "\n")
