import math


def calculate_hp(base_hp, level, iv, ev):
    return math.floor(((2 * base_hp + iv + (ev // 4)) * level) // 100 + level + 10)


def calculate_stat(base_stat, level, iv, ev, nature_multiplier):
    return math.floor((((2 * base_stat + iv + (ev // 4)) * level) // 100 + 5) * nature_multiplier)
