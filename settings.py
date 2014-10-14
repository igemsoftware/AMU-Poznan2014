"""
.. module:: settings
    :synopsis: sets up urls.
        Change variable URL to our server IP
        if you do not like to download sh-miR designer project
"""

URL = "http://127.0.0.1:8080"

METHODS = {
    "mfold_create": URL + "/mfold/{}",
    "mfold_check": URL + "/mfold/status/{}",
    "mfold_result": URL + "/mfold/result/{}",

    "from_sirna_create": URL + "/from_sirna/{}",
    "from_sirna_check": URL + "/from_sirna/status/{}",
    "from_sirna_result": URL + "/from_sirna/result/{}",

    "from_transcript_create": URL + "/from_transcript/{}",
    "from_transcript_check": URL + "/from_transcript/status/{}",
    "from_transcript_result": URL + "/from_transcript/result/{}",
}
