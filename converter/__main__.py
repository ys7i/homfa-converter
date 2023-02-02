import sys
from logging import basicConfig, INFO

import runner


def setup():
    basicConfig(level=INFO, format="[%(levelname)s] %(message)s")


if __name__ == "__main__":
    setup()
    is_reverse = len(sys.argv) == 3 and sys.argv[2] == "reverse"
    aut = runner.convert_formula(sys.argv[1], is_reverse)
    # aut_lines = runner.convert_auto_to_str(aut)
    # runner.output_config(aut_lines)
