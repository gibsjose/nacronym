# Nacronym
Search for NASA term definitions amongst an endless supply of acronyms.

This was developed specifically for the HFCS team in the SSCO at NASA GSFC (there are some acronyms to get you started with...), so most of the terms are specific to our group.

NASA JPL maintains their own online glossary [here](https://solarsystem.nasa.gov/basics/glossary.php).

## Dependencies
#### Python 3
```
brew install python3
```

#### Dependency: `fuzzywuzzy` for fuzzy string matching
```
pip3 install fuzzywuzzy
```

#### Dependency: `python-Levenshtein` as an optional (but recommended) dependency for `fuzzywuzzy`
```
pip3 install python-Levenshtein
```

## Term File
The term file is a simple JSON file where the key is the acronym/term and the value is either a single definition string or a list of definition strings. For example, a small term file could look like this:

```json
{
    "MMU": "Memory Management Unit",
    "PLB": ["Processor Local Bus", "Programmable Logic Block"],
    "MPMC": "Memory Controller"
}
```
