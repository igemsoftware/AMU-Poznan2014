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
def mfold_result(task_id, zipname="now.zip", path="./results/mfold/"):
    req = get_request("mfold_result", task_id)
    try:
        with open(zipname, "wb") as f:
            for chunk in req.iter_content():
                f.write(chunk)
        unzip(zipname, path)
        remove(zipname)
        print("Results under: {}/".format(path + task_id))
    except zipfile.BadZipfile:
        print("Error: {}".format(req.json()['error']))


def mfold(sequence):
    return wait_until_task(
        lambda sequence: creator("mfold_create", sequence),
        sequence,
        lambda task_id: checker("mfold_check", task_id),
        mfold_result
    )


# from_sirna
def from_sirna_result(task_id):
    data = get_json("from_sirna_result", task_id, 'data')

    path = "./results/sirna/{}/".format(task_id)
    print("Results under: {}".format(path))

    for no, (points, shmir, name, mfold_id) in enumerate(data['result']):
        mfold_result(mfold_id, path=path)
        new_path = path + name
        rename(path + mfold_id, new_path)
        print("{}: name: {}, score: {}, pdf: {}\n   result: {}".format(
            no, name, points, new_path, shmir
        ))


def from_sirna(sequences):
    return wait_until_task(
        lambda sequences: creator("from_sirna_create", sequences),
        sequences,
        lambda task_id: checker("from_sirna_check", task_id),
        from_sirna_result
    )


def transcript_create(transcript_name, **kwargs):
    return creator("transcript_create", transcript_create, {'params': kwargs})


if __name__ == '__main__':
    mfold_help = "Mfold option to fold sequence via mfold"
    from_sirna_help = "From sirna creates shmirs from sirna"
    parser = argparse.ArgumentParser(description="sh-miR client")
    parser.add_argument("--mfold", "-mf", nargs=1, type=str, help=mfold_help)
    parser.add_argument("--from_sirna", "-fs", nargs="+", type=str, help=from_sirna_help)

    args = parser.parse_args()
    if args.from_sirna and len(args.from_sirna) > 2:
        parser.error("sh-miR need 1 or 2 sequences")
    elif args.from_sirna:
        from_sirna(" ".join(args.from_sirna))

    if args.mfold:
        mfold(args.mfold[0])
