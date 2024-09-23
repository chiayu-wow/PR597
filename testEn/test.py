from geographiclib.geodesic import Geodesic
from pygeodesy import ellipsoidalVincenty as ev
geod = Geodesic.WGS84  # define the WGS84 ellipsoid

def test():
    print('cool')

g = geod.Inverse(0, 0, 10, 0)  # go north 10 degrees from equator
print("The distance is {:.2f} meters = {:.3f} nautical miles".format(g['s12'],
                                                                      g['s12']/1852.0))
print("The initial heading is {:03.1f} degrees.".format(g['azi1']))
print()

g = geod.Inverse(0, 0, 0, -10)  # go West 10 degrees along equator
print("The distance is {:.2f} meters = {:.3f} nautical miles".format(g['s12'],
                                                                      g['s12']/1852.0))
print("The initial heading is {:03.1f} degrees.".format(g['azi1']))
print()

g = geod.Inverse(0, -10, 10, 0)  # go NorthEast 10 deg N & 10 deg E.
print("The distance is {:.2f} meters = {:.3f} nautical miles".format(g['s12'],
                                                                      g['s12']/1852.0))
print("The initial heading is {:03.1f} degrees.".format(g['azi1']))
print()

# Display the entire returned object from the Inverse() function:
def flip_direction(direction: str) -> str:
    """Given a compass direction 'E', 'W', 'N', or 'S', return the opposite.
    Raises exception with none of those.

    :param direction: a string containing 'E', 'W', 'N', or 'S'
    :return: a string containing 'E', 'W', 'N', or 'S'
    """
    if direction == 'E':
        return 'W'
    elif direction == 'W':
        return 'E'
    elif direction == 'N':
        return 'S'
    elif direction == 'S':
        return 'N'
    else:
        raise ValueError('Invalid or unsupported direction {} given.'.format(direction))
def myLatLon(lat: str, lon: str) -> ev.LatLon:
    """Given a latitude and longitude, normalize them if necessary,
    to return a valid ellipsoidalVincenty.LatLon object.

    :param lat: the latitude as a string
    :param lon: the longitude as a string
    """

    # get number portion:
    if lon[-1] in ['E', 'W']:
        lon_num = float(lon[:-1])
        lon_dir = lon[-1]
    else:
        lon_num = float(lon)
    if lon_num > 180.0:  # Does longitude exceed range?
        lon_num = 360.0 - lon_num
        lon_dir = flip_direction(lon_dir)
        lon = str(lon_num) + lon_dir

    return ev.LatLon(lat, lon)

a = myLatLon('43.2N', '359.1W')
b = myLatLon('44.0N', '358.4W')
print(f' a : {a} b : {b}')

def factorial(n: int) -> int:
    """Compute a factorial.

    :param n: The number to factorialize
    :return: the factorial of n
    """
    # check validity of n:
    if not isinstance(n, int) or n < 0:
        raise ValueError('parameter n must be a non-negative integer.')

    f = 1
    for x in range(1, n + 1):
        f *= x
    return f


try:
    answer = factorial(-428465436541345)
except ValueError as e:
    pass