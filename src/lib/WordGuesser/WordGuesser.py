import os
import unicodedata
import pkg_resources
from typing import List, Set


class WordGuesser:
    """
    Class to guess words
    """
    def __init__(self, language: str):
        """
        Constructor

        Params:
          - language: language to use
        """
        self.dictionary = self._load_dictionary(language)
        self.prefixes = set(
            [w[:i] for w in self.dictionary for i in range(1, len(w))]
        )
        self.solutions = []
        self.letter_counts = {}
        self.distinct_letters = set()

    def guess(
        self,
        letters: str,
        max_word_length: int = None,
        exact_length: bool = False
    ) -> List[str]:
        """
        Guess words that contain the set of letters

        Params:
          - letters: string containing the letters to form words
          - max_word_length: maximum length of the words to return
          - exact_length: return only words with len(w) == max_word_length
        Returns: list of words that contain the given letters
        """
        if max_word_length is None:
            max_word_length = len(letters)
        letters = WordGuesser._normalize_letters(letters)
        self.solutions = []
        self.letter_counts = {c: letters.count(c) for c in set(letters)}
        self.distinct_letters = set(letters)
        self._recursive_search("", max_word_length, exact_length)
        # Order solutions, first by length and second alfabetically
        self.solutions = list(sorted(self.solutions, key=lambda w: (-len(w), w)))
        return self.solutions

    def _recursive_search(self, solution: str, length: int, exact_length: bool) -> None:
        """
        Backtracking solution that searches through all possible letter combinations using an
        optimized method that only continues the search in a specific path it's viable 
        """
        if exact_length and len(solution) == length or not exact_length and len(solution) <= length:
            if len(solution) > 1 and solution in self.dictionary:
                self.solutions.append(solution)
        if len(solution) < length:
            for c in self.distinct_letters:
                if self._check_solution(solution, c):
                    solution += c
                    self._recursive_search(solution, length, exact_length)
                    solution = solution[:-1]

    def _check_solution(self, current_solution: str, c: str) -> bool:
        """
        Checks if the solution is still viable after adding another
        letter to it in order to continue exploring that search path.

        Params:
          - current_solution: current combination of letters that can form a valid word
          - c: character to add to the solution
        """
        if current_solution.count(c) >= self.letter_counts[c]:
            return False

        next_solution = current_solution + c    
        if next_solution not in self.prefixes and next_solution not in self.dictionary:
            return False
        return True

    @staticmethod
    def _load_dictionary(language: str) -> Set[str]:
        """
        Load dictionary with the words of a supported language.
        Currently only spanish and english are supported.

        Params:
          - language: name of the language (must be "english" or "spanish")

        Return: a collection (set) containing the words of the language
        """
        dict_path = pkg_resources.resource_filename(
            __name__, os.path.join("dictionaries", language)
        )
        if not os.path.exists(dict_path):
            raise Exception(f"Unsupported language {language}")
        with open(dict_path, "r", encoding="utf-8") as f:
            lines = f.read().split("\n")
            return set(filter(None, map(WordGuesser._normalize_letters, lines)))

    @staticmethod
    def _normalize_letters(letters: str) -> str:
        """
        Removes accents from the letters but preserving the spanish Ñ character and converts to uppercase
        https://stackoverflow.com/questions/29984925/replace-accent-marks-preserving-special-characters

        Params:
          - letters: letters to normalize

        Returns: normalized letters
        """
        good_accents = {"\N{COMBINING TILDE}"}
        transformed = "".join(
            char
            for char in unicodedata.normalize("NFKD", letters.upper())
            if unicodedata.category(char) != "Mn" or char in good_accents
        )
        return unicodedata.normalize("NFKC", transformed)
