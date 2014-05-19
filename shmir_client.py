#!/usr/bin/env python

import requests
import time
import zipfile
import argparse

URL = "http://127.0.0.1:8080"

METHODS = {
    # "mfold_create": URL + "/mfold/{}",
    "mfold_create": URL + "/mfold/",
    # "mfold_check": URL + "/mfold/status/{}",
    "mfold_check": URL + "/mfold/result/{}",
    # "mfold_result": URL + "/mfold/result/{}",
    "mfold_result": URL + "/mfold/file/{}",
    "shmir_create": URL + "/designer/{}",
    "shmir_check": URL + "/designer/status/{}",
    "shmir_result": URL + "/designer/result/{}",
}


def unzip(filename):
    with zipfile.ZipFile(filename) as zip_file:
        zip_file.extractall(path=".")


def get_request(method, data):
    req = requests.get(METHODS[method].format(data))
    if req.status_code == 200:
        return req


# mfold
def mfold_create(sequence):
    # temporary
    import json
    return requests.post(METHODS["mfold_create"], data=json.dumps({'data': sequence})).json()["task_id"]
    # return get_request("mfold_create", sequence).json()["task_id"]


def mfold_check(task_id):
    return get_request("mfold_check", task_id).json()["status"]


def mfold_result(task_id, zipname):
    req = get_request("mfold_result", task_id)
    with open(zipname, "wb") as f:
        for chunk in req.iter_content():
            f.write(chunk)
    unzip(zipname)
    print("Done")


# shmir
def shmir_create(sequences):
    return get_request("shmir_create", sequences).json()["task_id"]


def shmir_check(task_id):
    return get_request("shmir_check", task_id).json()["status"]


def shmir_result(task_id):
    data = get_request("shmir_result", task_id).json()


def change_ttw(x):
    if x < 15:
        return 0
    elif x > 42:
        return 120
    return 1.2 ** (x - 15)


def wait_until_task(creator, create_data,
                    checker,
                    getter, get_data=()):

    ttw = 0.5
    counter = 0

    task_id = creator(create_data)

    while checker(task_id) != "ok":
        time.sleep(ttw)
        ttw += change_ttw(counter)

    return getter(task_id, *get_data)


mfold = lambda sequence, zipname: (
    wait_until_task(
        mfold_create, sequence, mfold_check,
        mfold_result, (zipname, )
    )
)


# mfold("UTGCCAAA", "now.zip")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='sh-miR client')
    parser.add_argument('--mfold', nargs=1, type=str, help='mfold')
    parser.add_argument('--shmir', nargs='+', type=str, help='shmir')

    args = parser.parse_args()
    if args.shmir and len(args.shmir) > 2:
        parser.error("sh-miR need 1 or 2 sequences")

    if args.mfold:
        mfold(args.mfold, "now.zip")
