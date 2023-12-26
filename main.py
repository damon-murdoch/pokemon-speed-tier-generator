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
import os

# Main Process
if __name__ == "__main__":
    # Get showdown data files
    MOVES, POKEMON = showdown.get_showdown_data()

    # This table will be indexed with the following:
    # key: Speed Number (e.g. 167)
    # value: Pokemon which reach this stat (with conditions) (e.g. 252+ Mega Kangaskhan)
    speed_tiers = {}

    # Loop over all of the Pokemon
    for pokemon in POKEMON:
        # Get the data for the species
        pokemon_data = POKEMON[pokemon]
        species = pokemon_data["name"]

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
            combo_string = f"{ivs}/{evs}"

            # Positive nature, add plus to string
            if nature == CONFIG.NATURE_POSITIVE:
                combo_string = f"{combo_string}+"
            # Negative nature, add minus to string
            elif nature == CONFIG.NATURE_NEGATIVE:
                combo_string = f"{combo_string}-"

            # Add species to the combo string
            combo_string = f"{combo_string} {species}"

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
                    stage_modifier = (1 + (stage * 0.5))

                    # Apply stage modifier to the stat
                    stage_stat = math.floor(stage_stat * stage_modifier)

                # If the stat is in the tiers
                if stage_stat in speed_tiers:
                    # Add the combo string to the speed tiers
                    speed_tiers[stage_stat].append(stage_string)
                else:
                    # Create a new entry with the speed tier
                    speed_tiers[stage_stat] = [stage_string]

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
        content = [
            "| Speed | Amount | Benchmarks |", 
            "| ----- | ------ | ---------- |"
        ]

        # Get all of the speed stats
        tiers = list(speed_tiers.keys())

        # Sort the tiers based on the sort config
        tiers.sort(reverse=CONFIG.SORT_SLOWEST_FIRST)

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
        with open(md_path, "w+", encoding='utf8') as file:
            # Write the data to the file
            file.write(output)