from typing import Optional
import re

ALP_STR = "abcdefghijklmnopqrstuvwxyz"


def convert_num_to_alp(num: int) -> Optional[str]:
    """
    0から25までの数字をaからzに変換する
    それ以外の数字にはNoneを返す
    """
    if num < 0 or num > 25:
        return None
    else:
        return ALP_STR[num]


def convert_alp_to_num(alp: str) -> Optional[int]:
    """
    aからzまでのアルファベットを0から25に変換する
    それ以外の文字列にはNoneを返す
    """
    if re.match(r"^[a-z]$", alp) is None:
        return None
    else:
        return ALP_STR.index(alp)
