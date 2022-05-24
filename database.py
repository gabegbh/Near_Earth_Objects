"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches
        for neo in self._neos:
            cas = set()
            for ca in self._approaches:
                # print(ca.designation, '::::: ',neo.designation)
                if ca.designation == neo.designation:
                    ca.neo = neo
                    cas.add(ca)
            neo.approaches = cas

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        for neo in self._neos:
            if neo.designation == designation:
                return neo
        return None

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        for neo in self._neos:
            if neo.name == name:
                return neo
        return None

    def query(self, args):  #date=None, dist=None, vel=None, diam=None, haz=None
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaningfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """

        fil_app = self._approaches

        if 'date' in args:
            d = args['date']
            if d[0]:
                fil_app = set(filter(lambda app: app.time.date() == d[0], fil_app))
            elif d[1] and d[2]:
                fil_app = set(filter(lambda app: d[1] <= app.time.date() <= d[2], fil_app))
            elif d[1]:
                fil_app = set(filter(lambda app: app.time.date() >= d[1], fil_app))
            else:
                fil_app = set(filter(lambda app: app.time.date() <= d[2], fil_app))

        if 'dist' in args:
            d = args['dist']
            if d[0] and d[1]:
                fil_app = set(filter(lambda app:  d[0] <= app.distance <= d[1], fil_app))
            elif d[0]:
                fil_app = set(filter(lambda app: app.distance >= d[0], fil_app))
            else:
                fil_app = set(filter(lambda app: app.distance <= d[1], fil_app))

        if 'vel' in args:
            v = args['vel']
            if v[0] and v[1]:
                fil_app = set(filter(lambda app: v[0] <= app.velocity <= v[1], fil_app))
            elif v[0]:
                fil_app = set(filter(lambda app: app.velocity >= v[0], fil_app))
            else:
                fil_app = set(filter(lambda app: app.velocity <= v[1], fil_app))
            
        if 'diam' in args:
            d = args['diam']
            if d[0] and d[1]:
                fil_app = set(filter(lambda app: d[0] <= app.neo.diameter <= d[1], fil_app))
            elif d[0]:
                fil_app = set(filter(lambda app: app.neo.diameter >= d[0], fil_app))
            else:
                fil_app = set(filter(lambda app: app.neo.diameter <= d[1], fil_app))
            
        if 'haz' in args:
            if args['haz']:
                fil_app = set(filter(lambda app: app.neo.hazardous, fil_app))
            else: 
                fil_app = set(filter(lambda app: not app.neo.hazardous, fil_app))
            
        for app in fil_app:
            yield app