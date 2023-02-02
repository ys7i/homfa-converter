from typing import List


class NBAutomata:
    def __init__(self, f):
        aut = f.translate("small", "buchi", "sbacc")
        assert not aut.is_empty()

        hoa_lines = aut.to_str("hoa").split("\n")
        header, body = self._split_header_body(hoa_lines)

        self.initial: int = initial
        self.config: List[dict[str, int]] = config

    def _split_header_body(self, lines: List[str]) -> tuple[List[str], List[str]]:
        body_index = lines.index("--BODY--")
        header = lines[:body_index]
        body = lines[body_index + 1 : -1]
        return header, body
