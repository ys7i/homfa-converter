from enum import Enum
import numpy as np
from typing import List
import spot

from converter.hoa_parser.dto import IntegratedAutomata
from hoa_parser.hoa_parser import parse_hoa
from converter.automata.nba import NBAutomata


class Condition(Enum):
    ZERO = 0
    ONE = 1
    BOTH = 2


def convert_formula_to_nba(formula: str) -> NBAutomata:
    f = spot.formula(formula)
    assert f.is_ltl_formula()
    aut = f.translate("small", "buchi", "sbacc")
    assert not aut.is_empty()
    hoa_lines = aut.to_str("hoa").split("\n")
    i_aut = parse_hoa(hoa_lines)
    return construct_nba_from_iaut(i_aut)


def find_aps_combination(aps_len: int, target: str) -> List[Condition]:
    """atomic propositionの組み合わせをTrue or Falseのリストで返す
        :param int aps_len: length of atomic propositions ex) 3
        :param str target: string which represents the combination of aps ex) "0&!1"
    :return: the combination of aps ex) [ONE, ZERO, BOTH]
    """
    if target == "t":
        return [Condition.BOTH for _ in range(aps_len)]
    combination = [Condition.BOTH for _ in range(aps_len)]
    for ap in target.split("&"):
        ap_index = int(ap.replace("!", ""))
        assert ap_index is not np.nan and ap_index < aps_len
        if ap.startswith("!"):
            combination[ap_index] = Condition.ZERO
        else:
            combination[ap_index] = Condition.ONE
    return combination


def construct_nba_from_iaut(i_aut: IntegratedAutomata) -> NBAutomata:
    nba_config = [{"zero": [], "one": []} for _ in range(len(i_aut.config))]
    for i, transition in enumerate(i_aut.config):
        trans_keys = transition.keys()
        for key in trans_keys:
            dst = transition[key]
            # true transition
            # 複数のapの組み合わせを1つのapで表すように変換
            if key == "t":
                pre_index = i
                for _ in range(len(i_aut.aps) - 1):
                    nba_config.append({"zero": [], "one": []})
                    cur_index = len(nba_config) - 1
                    nba_config[pre_index]["zero"].append(cur_index)
                    nba_config[pre_index]["one"].append(cur_index)
                    pre_index = cur_index
                nba_config[pre_index]["zero"].append(dst)
                nba_config[pre_index]["one"].append(dst)
            else:
                conditions = find_aps_combination(len(i_aut.aps), key)
                dst = transition[key]
                pre_index = i
                for condition in conditions[:-1]:
                    nba_config.append({"zero": [], "one": []})
                    cur_index = len(nba_config) - 1
                    if condition != Condition.ZERO:
                        nba_config[pre_index]["one"].append(cur_index)
                    if condition != Condition.ONE:
                        nba_config[pre_index]["zero"].append(cur_index)
                    pre_index = cur_index
                condition = conditions[-1]
                if condition != Condition.ZERO:
                    nba_config[pre_index]["one"].append(dst)
                if condition != Condition.ONE:
                    nba_config[pre_index]["zero"].append(dst)
    # reject stateが必要であれば追加
    rej_state = -1
    for i, config in enumerate(nba_config):
        if len(config["zero"]) == 0:
            if rej_state == -1:
                rej_state = len(nba_config)
                nba_config.append({"zero": [rej_state], "one": [rej_state]})
            nba_config[i]["zero"].append(rej_state)
        if len(config["one"]) == 0:
            if rej_state == -1:
                rej_state = len(nba_config)
                nba_config.append({"zero": [rej_state], "one": [rej_state]})
            nba_config[i]["one"].append(rej_state)
    return NBAutomata(
        initial=i_aut.initial,
        config=nba_config,
        acc=i_aut.acc,
        rej=[] if rej_state == -1 else [rej_state],
    )
