#!/usr/bin/env python3
"""nacronym: NASA acronym search tool
Usage:
    nacronym [options] <term>

Options:
    -h --help               Show this help
    -v --version            Show the version
    -c --case-sensitive     Enable case-sensitive searching
    -t <term-file>          Term file (JSON) override
    -m <match-threshold>    Match threshold can be: loose, medium, or strict [default: strict]
"""

#   nacronym: NASA acronym search tool
#
#   21 Jan 2016
#
#   Joe Gibson (joseph.j.gibson@nasa.gov)
#
#   License: MIT (http://gibsjose.mit-license.org)
#
#   https://gibsjose.com
#   https://github.com/gibsjose/nacronym

import sys
import os
import traceback
import time
import json
from docopt import docopt           # Argument parsing
from fuzzywuzzy import fuzz         # Fuzzy string matching
from fuzzywuzzy import process      #

MATCH_THRESHOLDS = {
    'loose': 50,
    'medium': 70,
    'strict': 90
}

class Term:
    """
    Stores the term as the term itself and a list of possible definitions
    """
    def __init__(self, term, definitions):
        """
        Initialize
        """
        # Convert a single definitions string to a list of length one
        if not isinstance(definitions, list):
            definitions = [definitions]

        self.data = {}
        self.data['term'] = term
        self.data['definitions'] = definitions

    def GetSpaces(self):
        """
        Helper for formatting the definition output for terms with multiple definitions
        """
        s = ''
        for c in self.data['term']:
            s += ' '

        return s

    def PrintDefinitions(self, prefix=''):
        """
        Print the term's definitions
        """
        # Single definition
        if len(self.data['definitions']) == 1:
            print(prefix + '\'' + self.data['definitions'][0] + '\'')

        # Multiple results
        else:
            def_count = 1
            print('')
            for definition in self.data['definitions']:
                print(prefix + str(def_count) + ':' + self.GetSpaces() + '\'' + definition + '\'')
                def_count += 1

class TermResults:
    """
    Stores the result of a term search as the original search term and a list of  possible definitions
    """
    def __init__(self, search):
        """
        Initialize
        """
        self.search = search
        self.terms = []

    def Add(self, term):
        """
        Add a term to the results
        """
        self.terms.append(term)

    def Print(self):
        """
        Print the result(s) if they exist
        """
        # No results
        if len(self.terms) == 0:
            print('No results for \'' + self.search + '\'')

            return 1

        # Single result
        elif len(self.terms) == 1:
            print(self.terms[0].data['term'] + ': ', end='')
            self.terms[0].PrintDefinitions()

            return 0

        # Multiple results
        else:
            print('Possible Matches for \'' + self.search + '\':')
            print('')
            for term in self.terms:
                print(term.data['term'] + ': ', end='')
                term.PrintDefinitions()
                print('')

            return 0

class TermDictionary:
    """
    Parses the terms in from the dictionary file and stores them for processing
    """
    def __init__(self, term_file):
        """
        Initialize
        """
        self.file = term_file
        self.terms = []
        self.data = self.Parse()

    def Parse(self):
        """
        Parse the JSON term file
        """
        with open(self.file, encoding='utf-8') as term_file:
            # Load JSON data
            self.data = json.loads(term_file.read())

        # Transform to list of terms
        for key in self.data:
            self.terms.append(Term(key, self.data[key]))

        return self.data

    def GetMatchRatio(self, search, term):
        """
        Wrapper for the `fuzz.ratio` method
        """
        search = search if arguments['--case-sensitive'] else search.upper()
        term = term if arguments['--case-sensitive'] else term.upper()

        return fuzz.ratio(search, term)

    def Search(self, search, match_threshold):
        """
        Search for the term and return a list of results
        """
        results = TermResults(search)

        for term in self.terms:
            # Convert to uppercase and perform fuzzy string match
            if self.GetMatchRatio(search, term.data['term']) > match_threshold:
                results.Add(term)

        return results

def main():
    """
    Get the term list and search for the given term
    """
    term = arguments['<term>']
    match_threshold = MATCH_THRESHOLDS[arguments['-m']]

    # Default to `terms.json` if no override
    if arguments['-t']:
        term_file = arguments['-t']
    else:
        term_file = os.path.join(os.path.dirname(__file__), 'terms.json')

    # Make sure term file exists
    if not os.path.exists(term_file):
        raise Exception('Term file \'' + term_file + '\' does not exist')

    # Create the term dictionary
    dictionary = TermDictionary(term_file)

    # Search for term
    results = dictionary.Search(term, match_threshold)

    # Print results
    status = results.Print()

    # Return status
    os._exit(status)

def entry():
    try:
        global arguments
        arguments = docopt(__doc__, version='nacronym 1.4.2')
        main()
        sys.exit(0)

    except KeyboardInterrupt as e: # Ctrl-C
        raise e
    except SystemExit as e: # sys.exit()
        raise e
    except Exception as e:
        print('Error: Unexpected Exception')
        print(str(e))
        traceback.print_exc()
        os._exit(1)

if __name__ == '__main__':
    entry()
