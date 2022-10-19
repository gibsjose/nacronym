# Nacronym
Search for NASA term definitions amongst an endless supply of acronyms.

This was developed specifically for the HFCS team in the SSCO at NASA GSFC (there are some acronyms to get you started with...), so most of the terms are specific to our group.

NASA JPL maintains their own online glossary [here](https://solarsystem.nasa.gov/basics/glossary.php).

## Install

### Manual
Create a virtual environment and activate it:
```
python3 -m venv nacronymvenv
source nacronymvenv/bin/activate
```

Build and install this script in that environment:
```
pip install build
python -m build
pip install --force-reinstall dist/nacronym-0.1-py3-none-any.whl
```

### PIP

## Usage

If you installed `nacronym` manually, make sure to activate the virtual environment.
Then provide with a term file.


## Term File
The term file is a simple JSON file where the key is the acronym/term and the value is either a single definition string or a list of definition strings. For example, a small term file could look like this:

```json
{
    "MMU": "Memory Management Unit",
    "PLB": ["Processor Local Bus", "Programmable Logic Block"],
    "MPMC": "Memory Controller"
}
```
