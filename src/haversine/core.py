"""Great-circle distance between two points on Earth.

Uses the Haversine formula. Points are (lat, lon) tuples in degrees.
"""

import math

EARTH_RADIUS_METERS = 6371000.8
EARTH_RADIUS_KILOMETERS = EARTH_RADIUS_METERS / 1000.0
EARTH_RADIUS_MILES = EARTH_RADIUS_METERS / 1609.344
EARTH_RADIUS_NAUTICAL_MILES = EARTH_RADIUS_METERS / 1852.0


def haversine(a, b, radius=EARTH_RADIUS_METERS):
    """Return the great-circle distance between two points.

    Parameters
    ----------
    a, b : tuple of (float, float)
        (latitude, longitude) in decimal degrees.
    radius : float, default EARTH_RADIUS_METERS
        Radius of the sphere. The result is in whatever unit this is.

    Returns
    -------
    float
        Distance along the sphere's surface in the same unit as ``radius``.

    Notes
    -----
    Points are normalized into valid angular ranges before computing.
    The formula degenerates to 0 for coincident or antipodal-adjacent points;
    those are handled by checking the rounded sin² term before asin.
    """
    lat1, lon1 = a
    lat2, lon2 = b

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)

    sin_dphi = math.sin(dphi / 2.0)
    sin_dlam = math.sin(dlam / 2.0)
    h = sin_dphi * sin_dphi + math.cos(phi1) * math.cos(phi2) * sin_dlam * sin_dlam

    # Clamp away from the numeric edges of asin, which occur at coincident
    # (h -> 0) and antipodal (h -> 1) points. Both are legitimate inputs.
    h = min(1.0, max(0.0, h))
    return 2.0 * radius * math.asin(math.sqrt(h))


def haversine_unit(a, b, unit="meters"):
    """Return the great-circle distance in a named unit.

    Parameters
    ----------
    a, b : tuple of (float, float)
        (latitude, longitude) in decimal degrees.
    unit : str
        One of: "meters", "kilometers", "km", "miles", "nautical_miles".
    """
    if unit == "meters":
        return haversine(a, b, EARTH_RADIUS_METERS)
    if unit == "kilometers":
        return haversine(a, b, EARTH_RADIUS_KILOMETERS)
    if unit == "km":
        return haversine(a, b, EARTH_RADIUS_KILOMETERS)
    if unit == "miles":
        return haversine(a, b, EARTH_RADIUS_MILES)
    if unit == "nautical_miles":
        return haversine(a, b, EARTH_RADIUS_NAUTICAL_MILES)
    raise ValueError(
        "unknown unit %r; expected 'meters', 'kilometers', 'km', 'miles', or 'nautical_miles'" % unit
    )
