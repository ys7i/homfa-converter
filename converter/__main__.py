import sys
from logging import basicConfig, INFO
from manager.manager import convert_formula, convert_aut_to_str, output_config


def setup():
    basicConfig(level=INFO, format="[%(levelname)s] %(message)s")


if __name__ == "__main__":
    setup()
    is_reverse = len(sys.argv) == 3 and sys.argv[2] == "reverse"
    aut = convert_formula(sys.argv[1], is_reverse)
    aut_lines = convert_aut_to_str(aut)
    output_config(aut_lines)
