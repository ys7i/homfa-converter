import re
from typing import List
from converter.hoa_parser.dto import IntegratedAutomata
from converter.hoa_parser.alphabet.alphabet import (
    convert_num_to_alp,
)

# HOA形式のオートーマトン設定をパースする

# HOA形式の例
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


def parse_hoa(lines) -> IntegratedAutomata:
    """return
    atomic propositions, 受理条件, 初期状態, relation(state, transition)
    """
    body_index = lines.index("--BODY--")
    header = lines[:body_index]
    body = lines[body_index + 1 : -1]
    init_state = _find_initial_state(header[2])
    aps = _find_atomic_propositions(header[3])
    acc = _find_acc_condition(header[5], body)
    config = _find_config(body, aps)
    i_aut = IntegratedAutomata(
        initial=init_state, aps=sorted(aps), acc=acc, config=config
    )
    return i_aut


# parseする文字列の例
# AP: 3 "p0" "p1" "p2"
def _find_atomic_propositions(line: str) -> List[str]:
    ap_regex = r"AP: \d+ (.+)"
    ap_match = re.search(ap_regex, line)
    if ap_match is None:
        raise Exception("AP not found")
    # ap_line: ex) "p0" "p1" "p2"
    ap_line = ap_match.group(1).replace('"', "")
    return ap_line.split(" ")


# parseする文字列の例
# Acceptance: 1 Inf(0)
def _find_acc_condition(header_line: str, body: List[str]) -> List[int]:
    acc_regex = r"Acceptance: (\d+) (?:Inf\((\d+)\))+"
    acc_match = re.search(acc_regex, header_line)
    if acc_match is None:
        raise Exception("acc-name not found")
    acc_num_str, *rest = acc_match.groups()
    assert int(acc_num_str) == len(rest)
    if len(rest) != 1:
        raise Exception("found multiple acceptance conditions. This is not supported.😱")

    acc_state_list = []
    acc_state_regex = r"State: (\d+) \{{{}\}}".format(rest[0])
    for line in body:
        acc_match = re.search(acc_state_regex, line)
        if acc_match is not None:
            acc_state_list.append(int(acc_match.group(1)))
    return acc_state_list


# 初期状態を特定する
def _find_initial_state(line: str) -> int:
    init_regex = r"Start: (\d+)"
    init_match = re.search(init_regex, line)
    if init_match is None:
        raise Exception("Initial state not found")
    return int(init_match.group(1))


def _find_config(body: List[str], aps: List[str]) -> List[dict[str, int]]:
    """returns
    ex) [{'t': 0}, {'!2': 1}, {'!1&!2': 1, '1': 2}, {'!0': 0, '0&!1&!2': 1, '0&1': 2}]
    """
    state_regex = r"State: (\d+)"
    trans_regex = r"\[([^\]]+)\] (\d+)"

    state_rows = list(filter(lambda x: re.search(state_regex, x) is not None, body))
    now_state = 0
    config = [{} for _ in range(len(state_rows))]
    for line in body:
        if line.startswith("State:"):
            st_match = re.search(state_regex, line)
            assert st_match is not None
            now_state = int(st_match.group(1))
        else:
            tr_match = re.search(trans_regex, line)
            assert tr_match is not None
            condition_line = _relabel_line(tr_match.group(1), aps)
            # '1 | !2'等の場合(orの場合)に対応
            conditions = (
                condition_line.split("|") if "|" in condition_line else [condition_line]
            )
            for condition in conditions:
                config[now_state][condition] = int(tr_match.group(2))
    return config


def _relabel_line(line: str, aps: List[str]) -> str:
    """
    atomic propositionがp0, p1, p2の場合でもp1, p0, p2等の順番で0, 1, 2が割り振られる場合があるため、
    aps.sort()の順に0, 1, 2を振り直す
    line内の数字をアルファベットに変換し、対応する数字に戻す
    ex) aps = ['p1', 'p0', 'p2'], line="0&1|2"
    -> line="a&b|c"
    -> line="1&0|2"
    """
    if line == "t":
        return "t"
    bind_dict = {}
    for i, ap in enumerate(aps):
        alp = convert_num_to_alp(i)
        assert alp is not None
        # atomic propositionの数が11を超えると誤変換される
        line = line.replace(f"{i}", alp)
        bind_dict[ap] = alp

    sorted_aps = sorted(aps)
    for i, ap in enumerate(sorted_aps):
        alp = bind_dict[ap]
        line = line.replace(alp, str(i))
    return line
