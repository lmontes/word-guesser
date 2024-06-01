import pytest
from src.lib.WordGuesser import WordGuesser


def test_load_supported_language():
    assert len(WordGuesser._load_dictionary("spanish")) > 0
    assert len(WordGuesser._load_dictionary("english")) > 0


def test_load_unsupported_language():
    with pytest.raises(Exception):
        WordGuesser._load_dictionary("chinese")

    with pytest.raises(Exception):
        WordGuesser("chinese")


def test_normalize_letters():
    assert WordGuesser._normalize_letters("AÑO") == "AÑO"     # Preserve Ñ
    assert WordGuesser._normalize_letters("ÁRBOL") == "ARBOL" # Remove accent


def test_result():
    wg = WordGuesser("spanish")

    result = wg.guess("ARAÑA")

    assert len(result) > 0
    assert "ARAÑA" in result


@pytest.mark.parametrize("max_length", [2, 3, 4, 5])
def test_max_word_length(max_length):
    wg = WordGuesser("spanish")

    result = wg.guess("ARBOL", max_word_length=max_length)

    lengths_less_equal_max_length = map(lambda w : len(w) <= max_length, result)

    assert all(lengths_less_equal_max_length)


@pytest.mark.parametrize(
    ["letters", "max_length"],
    [
        ("ARBOL", 3),
        ("ARBOL", 4),
        ("ARBOL", 5),
        ("ARRIBA", 5),
        ("ARRIBA", 6)
    ]
)
def test_exact_length(letters, max_length):
    wg = WordGuesser("spanish")

    result = wg.guess(letters, exact_length=True, max_word_length=max_length)

    lengths_exact_length = map(lambda w : len(w) <= len(letters), result)

    assert all(lengths_exact_length)
