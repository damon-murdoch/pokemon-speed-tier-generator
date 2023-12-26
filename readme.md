# Pokemon Showdown API Data Template

## Overview

This repository serves as a template for projects that require data from the Pokemon Showdown! API. The provided script allows users to easily fetch and manage data related to moves and the Pokedex.

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/your-username/pokemon-showdown-api-template.git
    ```

2. Navigate to the project directory:

    ```bash
    cd pokemon-showdown-api-template
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Fetching Pokemon Showdown! Data

The `showdown.py` script in the `src` directory provides a function to retrieve data from the Pokemon Showdown! API. The primary function is `get_showdown_data`, which fetches data for moves and the Pokedex.

```python
# Import the module
import src.showdown as showdown

# Get Showdown data files
MOVES, POKEMON = showdown.get_showdown_data()
```

The `get_showdown_data` function takes an optional argument `force` (default is `False`). When set to `True`, it forces a fresh download of the data even if the data files already exist.

### Data Directory

The fetched data is stored in the `data` directory. Two files, `moves.json` and `pokedex.json`, respectively, contain the moves and Pokedex information.

### Example

```python
# Import the module
import src.showdown as showdown

# Get Showdown data files, force a fresh download
MOVES, POKEMON = showdown.get_showdown_data(force=True)
```

## Data Structure

### Moves Data

The moves data is stored in the `moves.json` file. It includes information about various Pokemon moves.

### Pokedex Data

The Pokedex data is stored in the `pokedex.json` file. It contains comprehensive information about Pokemon species.

## Dependencies

- `requests==2.26.0`

## Contributing

Feel free to contribute to this template to enhance its functionality or usability. Submit issues or pull requests as needed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.