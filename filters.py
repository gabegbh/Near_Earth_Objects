import itertools


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


def create_filters(
        date=None, start_date=None, end_date=None,
        distance_min=None, distance_max=None,
        velocity_min=None, velocity_max=None,
        diameter_min=None, diameter_max=None,
        hazardous=None
):
    """Create a collection of filters from user-specified criteria.

    Each of these arguments is provided by the main module with a value from the
    user's options at the command line. Each one corresponds to a different type
    of filter. For example, the `--date` option corresponds to the `date`
    argument, and represents a filter that selects close approaches that occurred
    on exactly that given date. Similarly, the `--min-distance` option
    corresponds to the `distance_min` argument, and represents a filter that
    selects close approaches whose nominal approach distance is at least that
    far away from Earth. Each option is `None` if not specified at the command
    line (in particular, this means that the `--not-hazardous` flag results in
    `hazardous=False`, not to be confused with `hazardous=None`).

    The return value must be compatible with the `query` method of `NEODatabase`
    because the main module directly passes this result to that method. For now,
    this can be thought of as a collection of `AttributeFilter`s.

    If a param is taken that does not work i.e. start_date after end_date, it attaches 
    an unsupported_parameter arg to the filters list along with a message of the 
    infraction. The db.query function will see it and raise the warning message and 
    rightly return an empty results list without doing the filtering.

    :param date: A `date` on which a matching `CloseApproach` occurs.
    :param start_date: A `date` on or after which a matching `CloseApproach` occurs.
    :param end_date: A `date` on or before which a matching `CloseApproach` occurs.
    :param distance_min: A minimum nominal approach distance for a matching `CloseApproach`.
    :param distance_max: A maximum nominal approach distance for a matching `CloseApproach`.
    :param velocity_min: A minimum relative approach velocity for a matching `CloseApproach`.
    :param velocity_max: A maximum relative approach velocity for a matching `CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a matching `CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a matching `CloseApproach`.
    :param hazardous: Whether the NEO of a matching `CloseApproach` is potentially hazardous.
    :return: A collection of filters for use with `query`.
    """

    filters = {
    'date' : (date, start_date, end_date),
    'dist' : (distance_min, distance_max),
    'vel' : (velocity_min, velocity_max),
    'diam' : (diameter_min, diameter_max)
    }

    d = filters['date']
    if d[1] and d[2]:
        if d[2] < d[1]:
            filters['unsup_params'] = f"Your end_date ({d[2]}) cannot be earlier than your start_date ({d[1]}). Please refine your filter arguments"

    d = filters['dist']
    if all([d[0], d[1]]):
        if d[1] < d[0]:
            filters['unsup_params'] = f"Your max_distance ({d[1]}) cannot be less than your min_distance ({d[0]}). Please refine your filter arguments"
    
    d = filters['vel']
    if all([d[0], d[1]]):
        if d[1] < d[0]:
            filters['unsup_params'] = f"Your max_velocity ({d[1]}) cannot be less than your min_velocity ({d[0]}). Please refine your filter arguments"
    
    d = filters['diam']
    if all([d[0], d[1]]):
        if d[1] < d[0]:
            filters['unsup_params'] = f"Your max_diameter ({d[1]}) cannot be less than your min_diameter ({d[0]}). Please refine your filter arguments"

    filters = dict(filter(lambda v: any(v[1]), filters.items()))

    if hazardous != None:
        filters['haz'] = hazardous

    return filters
        

def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.

    If `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """
    ret = iterator
    if n and n > 0:
        ret = itertools.islice(iterator, n)

    return ret
