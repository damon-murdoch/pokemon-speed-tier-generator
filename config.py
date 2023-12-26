# Constants - Don't touch these

# Nature Effects
NATURE_POSITIVE = 1.1
NATURE_NEUTRAL = 1.0
NATURE_NEGATIVE = 0.9

# Settings

# JSON Settings

# JSON Output key sorting
JSON_SORT_KEYS = True

# JSON Output indentation
JSON_INDENT = 2

# Report Output Settings

# Output folder path
OUTPUT_FOLDER = 'out'

# Output json file path
OUTPUT_JSON = 'tiers.json'

# Output markdown file path
OUTPUT_MD = 'TIERS.MD'

# Level for which the calculations will
# be run (Use level 100 for Smogon Formats)
LEVEL = 50

# If this is set to true, the report will
# be generated with slowest speed stats 
# at the top. By default, it will be
# sorted with fastest at the top.
SORT_SLOWEST_FIRST = False

# Stat Combination to calculate, for each species
STAT_COMBINATIONS = [
    {"evs": 252, "ivs": 31, "nature": NATURE_POSITIVE},
    {"evs": 252, "ivs": 31, "nature": NATURE_NEUTRAL},
    {"evs": 0, "ivs": 31, "nature": NATURE_NEUTRAL},
    {"evs": 0, "ivs": 0, "nature": NATURE_NEGATIVE},
]

# Stages which should be 
# applied to all combinations
STAGES = [
    0, # Neutral
    # 1, # Choice Scarf
    # 2, # Tailwind
]