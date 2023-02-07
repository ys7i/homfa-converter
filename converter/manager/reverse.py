from converter.automata.dfa import DFAutomata
from converter.automata.nfa import NFAutomata
from converter.manager import nfa_to_dfa


def reverse_dfa_to_nfa(dfa: DFAutomata) -> NFAutomata:
    if len(dfa.acc) == 0:
        return NFAutomata(
            initial=[0],
            config=[{"zero": [0], "one": [0]}],
            acc=[],
            rej=[0],
        )
    initials = sorted(dfa.acc)
    acc_state = [dfa.initial]
    nfa_config = [{"zero": [], "one": []} for _ in dfa.config]
    reject_state = -1
    for i, cf in enumerate(dfa.config):
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
    return NFAutomata(
        initial=initials,
        config=nfa_config,
        acc=acc_state,
        rej=[] if reject_state == -1 else [reject_state],
    )


def convert_reversed_nfa_to_dfa(nfa: NFAutomata) -> DFAutomata:
    return nfa_to_dfa.get_dfa(nfa, False)
