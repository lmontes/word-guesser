import pytest
import unicodedata
from WordGuesser import WordGuesser


def test_load_supported_language():
    assert len(WordGuesser.__load_dict__("spanish")) > 0
    assert len(WordGuesser.__load_dict__("english")) > 0


def test_load_unsupported_language():
    with pytest.raises(Exception):
        WordGuesser.__load_dict__("chinese")

    with pytest.raises(Exception):
        WordGuesser("chinese")


def test_normalize_word():
    assert WordGuesser.__normalize_word__("AÑO") == "AÑO"     # Preserve Ñ
    assert WordGuesser.__normalize_word__("ÁRBOL") == "ARBOL" # Remove accent


def test_result():
    wg = WordGuesser("spanish")

    letters = "ARAÑA"
    result = wg.guess_words(letters, len(letters))

    assert len(result) > 0
    assert "ARAÑA" in result
