import re
from typing import List

# HOA形式のオートーマトン設定をパースする

# HOA形式のheader
# HOA: v1
# States: 4
# Start: 3
# AP: 3 "p0" "p1" "p2"
# acc-name: Buchi
# Acceptance: 1 Inf(0)
# properties: trans-labels explicit-labels state-acc deterministic
# properties: stutter-invariant terminal

# HOA形式のbody
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

# 知りたい情報(ap, acceptance condition, 初期状態, relation)
def parse_hoa(header, body):
    init_state = _find_initial_state(header[2])
    aps = _find_atomic_propositions(header[3])
    acc = _find_acc_condition(header[5])
    print(init_state, aps, acc)


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
def _find_acc_condition(line: str) -> List[int]:
    acc_regex = r"Acceptance: (\d+) (?:Inf\((\d+)\))+"
    acc_match = re.search(acc_regex, line)
    if acc_match is None:
        raise Exception("acc-name not found")
    acc_num_str, *rest = acc_match.groups()
    assert int(acc_num_str) == len(rest)
    return [int(str) for str in rest]


# 初期状態を特定する
def _find_initial_state(line: str) -> int:
    init_regex = r"Start: (\d+)"
    init_match = re.search(init_regex, line)
    if init_match is None:
        raise Exception("Initial state not found")
    return int(init_match.group(1))


# stateとtransitionを特定する
def _find_state_and_transition(body: List[str]) -> int:
    init_regex = r"Start: (\d+)"
    init_match = re.search(init_regex, line)
    if init_match is None:
        raise Exception("Initial state not found")
    return int(init_match.group(1))
