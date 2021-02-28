import os
from WordGuesser import WordGuesser


guessers = {}


MAX_LETTERS = int(os.getenv("MAX_LETTERS", 12))
MAX_RESULTS = int(os.getenv("MAX_RESULTS", 25))
CORS_DOMAIN = os.getenv("CORS_DOMAIN", "*")


def cloud_function(request):
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": CORS_DOMAIN,
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600"
        }
        return ("", 204, headers)

    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": CORS_DOMAIN
    }

    if request.method != "POST":
        return ("", 405, headers)

    try:
        request_data = request.get_json(force=True)

        language = request_data["language"]
        if language not in guessers:
            guessers[language] = WordGuesser(language)

        letters = request_data["letters"]
        if len(letters) > MAX_LETTERS:
            return ("", 422, headers)

        words = guessers[language].guess_words(letters, len(letters))
        if len(words) > MAX_RESULTS:
            words = words[0:MAX_RESULTS]

        return ({"words": words}, 200, headers)
    except Exception as ex:
        print(ex)
        return (str(ex), 500, headers)