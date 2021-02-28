# Word Guesser

This repository contains the source code of a Python 3 library that can guess words from a sequence of unordered letters. The library uses an internal dictionary to validate the words, at this moment supports only spanish and english languages.

## Web application

To demonstrate the use of the library a simple web application has been created. This demo application can be tried in the [word-guesser web page](https://lmont.es/word-guesser). In the next image we can see a screen capture from the web application.

![](images/screenshot.png)

The application code is also located in this repository. The file  [index.html](index.html) contains all the frontend code.

The file [main.py](main.py) uses the library to implement a REST API that is used by the web application. That API is deployed as a [Cloud Function](https://cloud.google.com/functions) in [Google Cloud](https://cloud.google.com).

In order to ease the deployment of the API as a cloud function the code can be packaged as a zip file. We can use the [create-zip.sh](create-zip.sh) script to do it. When this script is executed it creates a file called **bundle.zip** with all the necessary file structure.

The tested cloud function configuration is:

* **Runtime**: Python 3.8
* **Memory**: 256 MiB
* **Executed function**: cloud_function

## Others

### Test package

```bash
pip install -r requirements-dev.txt
```

```bash
$ pytest

============================================================================== test session starts ===============================================================================
platform linux -- Python 3.7.4, pytest-5.4.1, py-1.8.1, pluggy-0.13.1
plugins: anyio-2.0.2
collected 4 items                                                                                                                                                           
tests/test_word_guesser.py ....                                                                                                                                            [100%]

=============================================================================== 4 passed in 0.67s ================================================================================
```

### Build package word-guesser

```bash
python setup.py sdist bdist_wheel
```

## Useful links

* [Handling CORS requests in Google Cloud functions](https://cloud.google.com/functions/docs/writing/http?hl=en#handling_cors_requests)
* [Google Cloud functions source code structure](https://cloud.google.com/functions/docs/writing?hl=en#structuring_source_code)
* [Authoritative guide to CORS for REST APIs](https://www.moesif.com/blog/technical/cors/Authoritative-Guide-to-CORS-Cross-Origin-Resource-Sharing-for-REST-APIs/)
* [Replace accent marks preserving special characters](https://stackoverflow.com/questions/29984925/replace-accent-marks-preserving-special-characters)
