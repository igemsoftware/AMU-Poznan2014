#!/usr/bin/env python

import zipfile
import argparse
from utils import (
    unzip,
    get_request,
    get_json,
    creator,
    checker,
    wait_until_task,
)
from os import remove, rename


# mfold
mfold_create = lambda sequence: creator("mfold_create", sequence)
mfold_check = lambda task_id: checker("mfold_check", task_id)


def mfold_result(task_id, zipname="now.zip", path="./results/mfold/"):
    req = get_request("mfold_result", task_id)
    try:
        with open(zipname, "wb") as f:
            for chunk in req.iter_content():
                f.write(chunk)
        unzip(zipname, path)
        remove(zipname)
    except zipfile.BadZipfile:
        print("Error: {}".format(req.json()['error']))


mfold = lambda sequence: (
    wait_until_task(
        mfold_create, sequence, mfold_check, mfold_result,
    )
)


# shmir
shmir_create = lambda sequences: creator("shmir_create", sequences)
shmir_check = lambda task_id: checker("shmir_check", task_id)


def shmir_result(task_id):
    data = get_json("shmir_result", task_id, 'data')

    path = "./results/shmir/{}/".format(task_id)
    print("Results under: {}".format(path))

    for no, (points, shmir, name, mfold_id) in enumerate(data):
        mfold_result(mfold_id, path=path)
        new_path = path + name
        rename(path + mfold_id, new_path)
        print("{}: name: {}, score: {}, pdf: {}\n   result: {}".format(
            no, name, points, new_path, shmir
        ))

shmir = lambda sequences: (
    wait_until_task(
        shmir_create, sequences, shmir_check, shmir_result
    )
)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='sh-miR client')
    parser.add_argument('--mfold', nargs=1, type=str, help='mfold')
    parser.add_argument('--shmir', nargs='+', type=str, help='shmir')

    args = parser.parse_args()
    if args.shmir and len(args.shmir) > 2:
        parser.error("sh-miR need 1 or 2 sequences")
    elif args.shmir:
        shmir(" ".join(args.shmir))

    if args.mfold:
        mfold(args.mfold[0])
