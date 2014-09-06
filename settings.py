"""
.. module:: settings
    :synopsis: sets up all urls
"""

URL = "http://127.0.0.1:8080"

METHODS = {
    "mfold_create": URL + "/mfold/{}",
    "mfold_check": URL + "/mfold/status/{}",
    "mfold_result": URL + "/mfold/result/{}",
    "shmir_create": URL + "/designer/{}",
    "shmir_check": URL + "/designer/status/{}",
    "shmir_result": URL + "/designer/result/{}",
}
