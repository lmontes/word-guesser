import os
import unicodedata
import pkg_resources
from typing import List, Set


class WordGuesser():
    def __init__(self, language: str):
        self._dictionary = self.__load_dict__(language)
        self._prefixes = {
            word[:i] for word in self._dictionary for i in range(1, len(word))
        }
        self._solutions = []
        self._letter_count = {}
        self._distinct_letters = set()


    def guess_words(self, letters: str, max_word_length: int, exact_length: bool = False) -> List[str]:
        letters = WordGuesser.__normalize_word__(letters)
        self._solutions = []
        self._letter_count = {c : letters.count(c) for c in set(letters)}
        self._distinct_letters = set(letters)
        self.__recursive_search__("", max_word_length, exact_length)
        self._solutions = list(sorted(self._solutions, key = lambda w : (-len(w), w)))
        return self._solutions


    def last_solution(self) -> List[str]:
        return self._solutions


    def __recursive_search__(self, solution: str, length: int, exact_length: bool) -> None:
        if (
            (
                (exact_length and len(solution) == length)
                or (not exact_length and len(solution) <= length)
            )
            and len(solution) > 1
            and solution in self._dictionary
        ):
            self._solutions.append(solution)
        if len(solution) < length:
            for c in self._distinct_letters:
                if self.__check__(solution, c):
                    solution += c
                    self.__recursive_search__(solution, length, exact_length)
                    solution = solution[:-1]


    def __check__(self, current_solution: str, c: str) -> bool:
        if current_solution.count(c) >= self._letter_count[c]:
            return False
        if current_solution + c not in self._prefixes and current_solution + c not in self._dictionary:
            return False
        return True


    @staticmethod
    def __load_dict__(language: str) -> Set[str]:
        dict_path = pkg_resources.resource_filename(__name__, os.path.join("dictionaries", language))
        if not os.path.exists(dict_path):
            raise Exception(f"Unsupported language {language}")
        with  open(dict_path, "r") as f:
            lines = f.read().split("\n")
            return set(filter(None, map(WordGuesser.__normalize_word__, lines)))


    # Remove accents but preserve Spanish Ñ
    # https://stackoverflow.com/questions/29984925/replace-accent-marks-preserving-special-characters
    @staticmethod
    def __normalize_word__(w: str) -> str:
        good_accents = {
            u"\N{COMBINING TILDE}"
        }
        transformed = "".join(c for c in unicodedata.normalize("NFKD", w.upper()) if unicodedata.category(c) != "Mn" or c in good_accents)
        return unicodedata.normalize("NFKC", transformed)
