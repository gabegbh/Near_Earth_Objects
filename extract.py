"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """

    neo_ret = set()
    with open(neo_csv_path) as f:
        reader = csv.reader(f)
        next(reader)
        for data in reader:
            args = {'designation':data[3], 'name':data[4], "diameter":data[15], 'hazardous':data[7]=='Y'}
            temp = dict(filter(lambda v: v[1] != '', args.items()))
            neo_ret.add(NearEarthObject(**temp))
    return neo_ret


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """

    ca_ret = set()
    with open(cad_json_path) as f:
        dic = json.load(f)
        for ca in dic['data']:
            args = {'designation':ca[0], 'time':ca[3], 'distance':ca[4], 'velocity':ca[7]}
            temp = dict(filter(lambda v: v[1] != '', args.items()))
            ca_ret.add(CloseApproach(**temp))
    return ca_ret
