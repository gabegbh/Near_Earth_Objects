from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **kwargs):
        """Create a new `NearEarthObject`.

        :param kwargs: A dictionary of excess keyword arguments supplied to the constructor.
        """

        self.designation = ''
        self.name = None
        self.diameter = float('nan')
        self.hazardous = False

        self.__dict__.update(kwargs)
        self.diameter = float(self.diameter)
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""

        return f'{self.designation} ({self.name})'

    def __str__(self):
        """Return `str(self)`."""

        haz = 'is' if self.hazardous else 'is not'
        return f"NEO: {self.fullname} with a diameter of {self.diameter:.2f} {haz} potentially hazardous"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"

    def serialize(self):
        ret = {}
        ret['designation'] = self.designation
        ret['name'] = self.name
        ret['diameter_km'] = self.diameter
        ret['potentially_hazardous'] = self.hazardous
        return ret

class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **kwargs):
        """Create a new `CloseApproach`.

        :param kwargs: A dictionary of excess keyword arguments supplied to the constructor.
        """

        self.designation = ''
        self.time = None
        self.distance = 0.0
        self.velocity = 0.0
        self.neo = None

        self.__dict__.update(kwargs)

        self.distance = float(self.distance)
        self.velocity = float(self.velocity)

        self.time = cd_to_datetime(self.time)

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """

        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""

        return f"On {self.time_str}, {self.neo.fullname} passes Earth from {self.distance:.2f}au at {self.velocity:.2f}km/h"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"

    def serialize(self, doc_type=None):
        ret = {}
        ret['datetime_utc'] = self.time_str
        ret['distance_au'] = self.distance
        ret['velocity_km_s'] = self.velocity
        if doc_type == 'json':
            ret['neo'] = self.neo.serialize()
        elif doc_type == 'csv':
            ret.update(self.neo.serialize())
        return ret
