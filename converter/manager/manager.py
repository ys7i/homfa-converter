from logging import getLogger
from typing import List

from converter.automata.automata3 import Automata3
from converter.manager.iaut_to_nba import convert_formula_to_nba
from converter.manager.nba_to_nfa import convert_nba_to_nfa
from converter.manager.nfa_to_dfa import convert_nfa_to_dfa
from converter.manager.product_dfa import product_aut
from converter.manager.reverse import convert_reversed_nfa_to_dfa, reverse_dfa_to_nfa


def convert_formula(formula, is_reversed=False) -> Automata3:
    logger = getLogger(__name__)

    tf_nba = convert_formula_to_nba(formula)
    ff_nba = convert_formula_to_nba(f"!({formula})")
    logger.info("succeeded🎉 from LTL formula to NBA")

    tf_nfa = convert_nba_to_nfa(tf_nba)
    ff_nfa = convert_nba_to_nfa(ff_nba)
    logger.info("succeeded🎉 from NFA to NBA")

    tf_dfa = convert_nfa_to_dfa(tf_nfa)
    ff_dfa = convert_nfa_to_dfa(ff_nfa)
    logger.info("succeeded🎉 from NFA to DFA")

    if is_reversed:
        tf_nfa = reverse_dfa_to_nfa(tf_dfa)
        ff_nfa = reverse_dfa_to_nfa(ff_dfa)

        tf_dfa = convert_reversed_nfa_to_dfa(tf_nfa)
        ff_dfa = convert_reversed_nfa_to_dfa(ff_nfa)
        logger.info("succeeded🎉 reversed")

    return product_aut(tf_dfa, ff_dfa)


def convert_aut_to_str(aut: Automata3) -> List[str]:
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
