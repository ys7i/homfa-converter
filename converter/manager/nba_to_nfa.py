from converter.automata.nba import NBAutomata
from converter.automata.nfa import NFAutomata


def convert_nba_to_nfa(nba: NBAutomata) -> NFAutomata:
    return NFAutomata(
        initial=[nba.initial], acc=nba.rej, rej=nba.acc, config=nba.config
    )
