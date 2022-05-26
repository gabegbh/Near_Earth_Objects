"""
Write module.

Write module for directing the stream of results
from a query to a csv or json file.
"""

import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly,
    each output row corresponds to the information in a single
    close approach from the `results` stream and its associated
    near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where
    the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )

    with open(filename, 'w') as w:
        writter = csv.DictWriter(w, fieldnames=fieldnames)
        writter.writeheader()
        for ca in results:
            writter.writerow(ca.serialize(doc_type='csv'))


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`.
    Roughly, the output is a list containing dictionaries,
    each mapping `CloseApproach` attributes to their values
    and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where
    the data should be saved.
    """
    with open(filename, 'w') as w:
        serialized_ca = [ca.serialize(doc_type='json') for ca in results]
        json.dump(serialized_ca, w, indent='')
