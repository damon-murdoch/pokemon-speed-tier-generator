# Showdown Data
import src.showdown as showdown

# Utility Functions
import src.util as util

# Config Functions
import config as CONFIG

# JSON library
import json as JSON

# Math Library
import math

# OS Library
import sys, os


# Check if the current stat is a jump stat
def is_jump_stat(last_value, current_value):
    # Return true if the last value was not none, and difference between
    # the last value and the current value (regardless of signedness) is
    # greater than one (i.e. 2+ stat jumps between values)
    return last_value != None and abs(last_value - current_value) > 1


def build_spread_string(ivs, evs, nature, species=None):
    # Start building the combo string

    # Add the ivs/evs
    spread_string = f"{ivs}/{evs}"

    # Positive nature, add plus to string
    if nature == CONFIG.NATURE_POSITIVE:
        spread_string = f"{spread_string}+"
    # Negative nature, add minus to string
    elif nature == CONFIG.NATURE_NEGATIVE:
        spread_string = f"{spread_string}-"

    # Species is defined
    if species:
        # Add the species name to the combo string
        spread_string = f"{spread_string} {species}"

    # Return spread string
    return spread_string


# Main Process
if __name__ == "__main__":
    # Get showdown data files
    MOVES, POKEMON = showdown.get_showdown_data()

    # This table will be indexed with the following:
    # key: Speed Number (e.g. 167)
    # value: Pokemon which reach this stat (with conditions) (e.g. 252+ Mega Kangaskhan)
    speed_tiers = {}

    # Species Inclusions, Exclusions
    exclude_species = CONFIG.EXCLUDE_SPECIES
    include_species = CONFIG.INCLUDE_SPECIES

    # Loop over all of the Pokemon
    for pokemon in POKEMON:
        # Get the data for the species
        pokemon_data = POKEMON[pokemon]
        species = pokemon_data["name"]
        number = pokemon_data["num"]

        # If the exclusion list is set, and species is in the set
        if exclude_species != None and number in exclude_species:
            continue # Skip this species

        # If the inclusion list is set, and species is not in the set
        if include_species != None and number not in include_species:
            continue # Skip this species

        # Dereference values
        base_stats = pokemon_data["baseStats"]
        base_speed = base_stats["spe"]

        # Loop over all of the stat combinations
        for combination in CONFIG.STAT_COMBINATIONS:
            # Dereference values
            ivs = combination["ivs"]
            evs = combination["evs"]
            nature = combination["nature"]

            # Calculate the speed stat for the combination
            speed_stat = util.calculate_stat(
                base_speed,
                CONFIG.LEVEL,
                combination["ivs"],
                combination["evs"],
                combination["nature"],
            )

            # Start building the combo string

            # Add the evs
            combo_string = build_spread_string(ivs, evs, nature, species)

            # Loop over the stages
            for stage in CONFIG.STAGES:
                # Copy combo data for stage
                stage_stat = speed_stat
                stage_string = combo_string

                # Stage is greater than zero
                if stage > 0:
                    # Apply the stage modifier to the string
                    stage_string = f"+{stage} {stage_string}"

                    # Calculate the stage modifier
                    stage_modifier = 1 + (stage * 0.5)

                    # Apply stage modifier to the stat
                    stage_stat = math.floor(stage_stat * stage_modifier)

                # If the stat is in the tiers
                if stage_stat in speed_tiers:
                    # Add the combo string to the speed tiers
                    speed_tiers[stage_stat].append(stage_string)
                else:
                    # Create a new entry with the speed tier
                    speed_tiers[stage_stat] = [stage_string]

    # Get all of the speed stats
    tiers = list(speed_tiers.keys())

    # Sort the tiers based on the sort config
    tiers.sort(reverse=CONFIG.SORT_SLOWEST_FIRST)

    # Ensure the output directory exists
    os.makedirs(CONFIG.OUTPUT_FOLDER, exist_ok=True)

    # Output json is not none
    if CONFIG.OUTPUT_JSON != None:
        # Generate a json string from the table
        output = JSON.dumps(
            speed_tiers, sort_keys=CONFIG.JSON_SORT_KEYS, indent=CONFIG.JSON_INDENT
        )

        # Build the path to the json file
        json_path = os.path.join(CONFIG.OUTPUT_FOLDER, CONFIG.OUTPUT_JSON)

        # Open the json report file
        with open(json_path, "w+") as file:
            # Write the data to the file
            file.write(output)

    # Output markdown is not none
    if CONFIG.OUTPUT_MD != None:
        # Content string array
        content = ["| Speed | Amount | Benchmarks |", "| ----- | ------ | ---------- |"]

        # Loop over the sorted array
        for tier in tiers:
            # Get the data for the speed tier
            tier_data = speed_tiers[tier]

            # Get the number of benchmarks in the tier
            tier_count = len(tier_data)

            # Join the tier benchmarks array
            benchmarks = ", ".join(tier_data)

            # Build the speed tier column string
            content.append(f"| {tier} | {tier_count} | {benchmarks} |")

        # Combine the array to build the output string
        output = "\n".join(content)

        # Build the path to the json file
        md_path = os.path.join(CONFIG.OUTPUT_FOLDER, CONFIG.OUTPUT_MD)

        # Open the md report file
        with open(md_path, "w+", encoding="utf8") as file:
            # Write the data to the file
            file.write(output)

    # Get the script arguments
    args = sys.argv[1:]

    # At least one argument
    if len(args) > 0:
        # Loop over the arguments
        for arg in args:
            # If the arg is a valid species
            if arg in POKEMON:
                report = {}

                # Dereference species data
                species = POKEMON[arg]
                name = species["name"]

                print(f"Processing species {name} ...")

                # Get the base stats for the species
                base_stats = species["baseStats"]
                base_speed = base_stats["spe"]

                # Positive nature
                ev_positive = {}

                # Neutral nature
                ev_neutral = {}

                # Checks to see if evs change stats
                # compared to previous (lower) number
                last_positive = None
                last_neutral = None

                # Loop over the range of evs
                for evs in range(0, 256, 4):
                    # Calculate positive nature speed stat
                    speed_positive = util.calculate_stat(
                        base_speed,
                        CONFIG.LEVEL,
                        31,
                        evs,
                        CONFIG.NATURE_POSITIVE,
                    )

                    # If the last stat was null, or new stat is higher
                    if last_positive == None or last_positive < speed_positive:
                        # Benchmarks reached
                        benchmark = []

                        # Check if the current stat is a jump stat
                        jump_stat = is_jump_stat(last_positive, speed_positive)

                        # Stat is a jump stat
                        if jump_stat == True:
                            # Get benchmark speed
                            benchmark_speed = speed_positive - 2

                            # Speed is in speed tiers list
                            if benchmark_speed in tiers:
                                # Add the benchmarks to the list
                                benchmark += speed_tiers[benchmark_speed]

                        # Get benchmark speed
                        benchmark_speed = speed_positive - 1

                        # Speed is in speed tiers list
                        if benchmark_speed in tiers:
                            # Add the benchmarks to the list
                            benchmark += speed_tiers[benchmark_speed]

                        # At least one benchmark reached
                        if len(benchmark) > 0:

                            # Speed ties list
                            speed_ties = []

                            # Speed tying speed tier in list
                            if speed_positive in speed_tiers:
                                speed_ties = speed_tiers[speed_positive]

                            # Add the benchmark values to the nature list
                            ev_positive[evs] = {
                                "jump": jump_stat,
                                "stat": speed_positive,
                                "speedties": speed_ties,
                                "benchmark": benchmark,
                            }

                        # Update last positive
                        last_positive = speed_positive

                    # Calculate neutral nature speed stat
                    speed_neutral = util.calculate_stat(
                        base_speed,
                        CONFIG.LEVEL,
                        31,
                        evs,
                        CONFIG.NATURE_NEUTRAL,
                    )

                    # If the last stat was null, or new stat is higher
                    if last_neutral == None or last_neutral < speed_neutral:
                        # Get benchmark speed
                        benchmark = speed_neutral - 1

                        # If the speed stat below is in the tier list
                        if benchmark in tiers:
                            
                            # Speed ties list
                            speed_ties = []

                            # Speed tying speed tier in list
                            if speed_neutral in speed_tiers:
                                speed_ties = speed_tiers[speed_neutral]

                            # Add the benchmark values to the nature list
                            ev_neutral[evs] = {
                                "jump": False,  # Not possible for neutral natures
                                "stat": speed_neutral,
                                "speedties": speed_ties,
                                "benchmark": speed_tiers[benchmark],
                            }

                        # Update last neutral
                        last_neutral = speed_neutral

                # Positive nature
                iv_neutral = {}

                # Neutral nature
                iv_negative = {}

                # Checks to see if evs change stats
                # compared to previous (lower) number
                last_neutral = None
                last_negative = None

                # Loop over iv ranges
                for ivs in range(0, 32):
                    # Calculate positive nature speed stat
                    speed_neutral = util.calculate_stat(
                        base_speed,
                        CONFIG.LEVEL,
                        ivs,
                        0,
                        CONFIG.NATURE_NEUTRAL,
                    )

                    # If the last stat was null, or new stat is higher
                    if last_neutral == None or last_neutral < speed_neutral:
                        # Get benchmark speed
                        benchmark = speed_neutral - 1

                        # If the speed stat below is in the tier list
                        if benchmark in tiers:
                            
                            # Speed ties list
                            speed_ties = []

                            # Speed tying speed tier in list
                            if speed_neutral in speed_tiers:
                                speed_ties = speed_tiers[speed_neutral]

                            # Add the benchmark values to the nature list
                            iv_neutral[ivs] = {
                                "jump": False,  # Not possible for neutral natures
                                "stat": speed_neutral,
                                "speedties": speed_ties,
                                "benchmark": speed_tiers[benchmark],
                            }

                        # Update last positive
                        last_neutral = speed_neutral

                    # Calculate neutral nature speed stat
                    speed_negative = util.calculate_stat(
                        base_speed,
                        CONFIG.LEVEL,
                        ivs,
                        0,
                        CONFIG.NATURE_NEGATIVE,
                    )

                    # If the last stat was null, or new stat is higher
                    if last_negative == None or last_negative < speed_negative:
                        # Benchmarks reached
                        benchmark = []

                        # Check if the current stat is a jump stat
                        jump_stat = is_jump_stat(last_negative, speed_negative)

                        # Stat is a jump stat
                        if jump_stat == True:
                            # Get benchmark speed
                            benchmark_speed = speed_negative - 2

                            # Speed is in speed tiers list
                            if benchmark_speed in tiers:
                                # Add the benchmarks to the list
                                benchmark += speed_tiers[benchmark_speed]

                        # Get benchmark speed
                        benchmark_speed = speed_positive - 1

                        # Speed is in speed tiers list
                        if benchmark_speed in tiers:
                            # Add the benchmarks to the list
                            benchmark += speed_tiers[benchmark_speed]

                        # At least one benchmark reached
                        if len(benchmark) > 0:

                            # Speed ties list
                            speed_ties = []

                            # Speed tying speed tier in list
                            if speed_negative in speed_tiers:
                                speed_ties = speed_tiers[speed_negative]

                            # Add the benchmark values to the nature list
                            iv_negative[ivs] = {
                                "jump": jump_stat,
                                "stat": speed_negative,
                                "speedties": speed_ties,
                                "benchmark": benchmark,
                            }

                        # Update last negative
                        last_negative = speed_negative

                # Build the final report
                report = {
                    "species": species,
                    "positive_ev": ev_positive,
                    "neutral_ev": ev_neutral,
                    "neutral_iv": iv_neutral,
                    "negative_iv": iv_negative,
                }

                # Export species to json format
                if CONFIG.SPECIES_JSON == True:
                    # Generate a json string from the table
                    output = JSON.dumps(
                        report,
                        sort_keys=CONFIG.JSON_SORT_KEYS,
                        indent=CONFIG.JSON_INDENT,
                    )

                    # Generate json filename
                    species_json = f"{name}.json"

                    # Generate output json file full path
                    json_path = os.path.join(CONFIG.OUTPUT_FOLDER, species_json)

                    # Open the json report file path
                    with open(json_path, "w+") as file:
                        # Dump the report data to the file
                        file.write(output)

                # Export species to markdown format
                if CONFIG.SPECIES_MD == True:
                    content = [
                        "| Spread | Stat | Jump | Benchmarks | Speed Ties |",
                        "| ------ | ---- | ---- | ---------- | ---------- |",
                    ]

                    # Sort the positive evs from highest to lowest
                    ev_pos_sorted = list(ev_positive.keys())
                    ev_pos_sorted.sort(reverse=True)

                    # Loop over the sorted evs
                    for ev in ev_pos_sorted:
                        # Get the data from the report
                        ev_data = ev_positive[ev]
                        stat = ev_data["stat"]
                        jump = ev_data["jump"]

                        # Build the benchmarks, speed ties string
                        benchmark = ", ".join(ev_data["benchmark"])
                        speed_ties = ", ".join(ev_data["speedties"])

                        # Generate spread string
                        spread_string = build_spread_string(
                            31, ev, CONFIG.NATURE_POSITIVE
                        )

                        # Add row for spread to report
                        content.append(
                            f"| {spread_string} | {stat} | {jump} | {benchmark} | {speed_ties} |"
                        )

                    # Sort the neutral evs from highest to lowest
                    ev_neu_sorted = list(ev_neutral.keys())
                    ev_neu_sorted.sort(reverse=True)

                    # Loop over the sorted evs
                    for ev in ev_neu_sorted:
                        # Get the data from the report
                        ev_data = ev_neutral[ev]
                        stat = ev_data["stat"]
                        jump = ev_data["jump"]

                        # Build the benchmarks, speed ties string
                        benchmark = ", ".join(ev_data["benchmark"])
                        speed_ties = ", ".join(ev_data["speedties"])

                        # Generate spread string
                        spread_string = build_spread_string(
                            31, ev, CONFIG.NATURE_NEUTRAL
                        )

                        # Add row for spread to report
                        content.append(
                            f"| {spread_string} | {stat} | {jump} | {benchmark} | {speed_ties} |"
                        )

                    # Sort the neutral ivs from highest to lowest
                    iv_neu_sorted = list(iv_neutral.keys())
                    iv_neu_sorted.sort(reverse=True)

                    # Loop over the sorted ivs
                    for iv in iv_neu_sorted:
                        # Get the data from the report
                        iv_data = iv_neutral[iv]
                        stat = iv_data["stat"]
                        jump = iv_data["jump"]

                        # Build the benchmarks, speed ties string
                        benchmark = ", ".join(iv_data["benchmark"])
                        speed_ties = ", ".join(iv_data["speedties"])

                        # Generate spread string
                        spread_string = build_spread_string(
                            iv, 0, CONFIG.NATURE_NEUTRAL
                        )

                        # Add row for spread to report
                        content.append(
                            f"| {spread_string} | {stat} | {jump} | {benchmark} | {speed_ties} |"
                        )

                    # Sort the neutral ivs from highest to lowest
                    iv_neg_sorted = list(iv_negative.keys())
                    iv_neg_sorted.sort(reverse=True)

                    # Loop over the sorted ivs
                    for iv in iv_neg_sorted:
                        # Get the data from the report
                        iv_data = iv_negative[iv]
                        stat = iv_data["stat"]
                        jump = iv_data["jump"]

                        # Build the benchmarks, speed ties string
                        benchmark = ", ".join(iv_data["benchmark"])
                        speed_ties = ", ".join(iv_data["speedties"])

                        # Generate spread string
                        spread_string = build_spread_string(
                            iv, 0, CONFIG.NATURE_NEGATIVE
                        )

                        # Add row for spread to report
                        content.append(
                            f"| {spread_string} | {stat} | {jump} | {benchmark} | {speed_ties} |"
                        )

                    # Join the output contents
                    output = "\n".join(content)

                    # Generate md filename
                    species_md = f"{name}.md"

                    # Generate output md file full path
                    md_path = os.path.join(CONFIG.OUTPUT_FOLDER, species_md)

                    # Open the md report file path
                    with open(md_path, "w+", encoding="utf8") as file:
                        # Dump the report data to the file
                        file.write(output)
            else:
                print(f"Failed for argument '{arg}': Unable to find matching species!")
