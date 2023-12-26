# Speed Tiers Generator

This script is designed to generate speed tiers for Pokémon based on various combinations of Individual Values (IVs), Effort Values (EVs), and Natures. The resulting speed tiers provide insights into the speed stats of different Pokémon under specific conditions. If you would like to see an example output file with the default configuration, please see 
[example.json](./example.json) and [EXAMPLE.MD](./EXAMPLE.MD).

## Prerequisites

Make sure you have the required dependencies installed. You can install them using the following command:

```bash
pip install -r requirements.txt
```

## Configuration

Modify the `config.py` file to customize the script's behavior. Adjust settings such as output file names, sorting preferences, and more.

## Running the Script

Execute the script to generate speed tiers:

```bash
python main.py
```

## Output

The script generates output in two formats:

1. **JSON File**: If configured, a JSON file is created with speed tiers and corresponding Pokémon benchmarks.

2. **Markdown File**: If configured, a Markdown file is generated with a table displaying speed tiers, the number of benchmarks in each tier, and specific Pokémon benchmarks.
