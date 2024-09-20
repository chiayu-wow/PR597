from pygeodesy.sphericalTrigonometry import LatLon
from datetime import datetime
from geographiclib.geodesic import Geodesic
import csv

def normalizeLongitude(lon: str) -> int:
    """
    Normalizes a longitude value, ensuring it falls within the [-180, 180] degree range.
    The input should be in degrees with a suffix indicating the hemisphere ('E' for east or 'W' for west).

    :param lon: A string representing the longitude value, where the last character
                    indicates the hemisphere ('E' or 'W')
    :return: The normalized longitude as a float, adjusted to be within the range of
                 [-180, 180] degrees, with negative values representing the western hemisphere.
    """
    hemisphere = lon[-1:]
    lon = float(lon[:-1])
    # Normalize longitude to be within [-180, 180] range
    while lon < -180:
            lon += 360
    while lon > 180:
            lon -= 360

    # Adjust for the western hemisphere
    if hemisphere == 'W':
            lon = -lon
    return int(lon)

def calculateDist(lat1 : float, lon1 :float, lat2 :float, lon2:float) -> float:
    """
    Args:
        lat1 (float): Latitude of the first point in decimal degrees.
        lon1 (float): Longitude of the first point in decimal degrees.
        lat2 (float): Latitude of the second point in decimal degrees.
        lon2 (float): Longitude of the second point in decimal degrees.

    Returns:
        float: The distance between the two points in nautical miles.
    """
    if abs(lon2 - lon1) > 1:
        return 60
    if abs(lat2 - lat1) > 1:
        return 60
    point1 = LatLon(lat1, lon1)
    point2 = LatLon(lat2, lon2)
    return point1.distanceTo(point2)/1852

def calculateAzimuth(lat1 : float, lon1 : float, lat2 : float, lon2 : float) -> int:
    """
    Calculate the azimuth (bearing) from one geographical point to another in degrees.

    Args:
          lat1 (float): Latitude of the first point in decimal degrees.
          lon1 (float): Longitude of the first point in decimal degrees.
          lat2 (float): Latitude of the second point in decimal degrees.
          lon2 (float): Longitude of the second point in decimal degrees.

    Returns:
          int: The azimuth from the first point to the second, normalized to a range
          of 0° to 360° and rounded to the nearest integer.
    """
    geod = Geodesic.WGS84
    result = geod.Inverse(lat1, lon1, lat2, lon2)
    azimuth = result['azi1']  # Azimuth from the first point to the second point

    # Convert azimuth to 0° to 360° range if it's negative
    normalized = azimuth % 360
    if normalized < 0:
       normalized += 360
    return round(normalized)

def processData(path: str, population: int) -> dict:
        """
        Processes city data from a CSV file and counts hurricane hits and durations based on proximity to cities.

        The function reads city data from a CSV file, filters cities based on population, and tracks the number of
        times each city is hit by a hurricane, as well as the total duration of these hits. It does this by
        calculating the distance between hurricane data points and cities, checking if they fall within a
        specific radius based on the hurricane's strength and position.

        Args:
                path (str): The file path of the CSV file containing city data.
                population (int): The minimum population threshold for a city to be included in the processing.

        Returns:
                dict: A dictionary with city data, including latitude, longitude, country, ISO code, population,
                number of times hit by a hurricane ('hit'), and total hurricane duration in hours ('duration').
        """
        cityData = {}
        # Open the CSV file
        # Open and process CSV file efficiently
        with open(path, mode='r') as file:
                csvReader = csv.reader(file)
                next(csvReader)  # Skip header

                for line in csvReader:
                        if line[9] == '' or float(line[9]) < population or float(line[2]) < 0 or float(line[3]) > 0:
                                continue
                        newCity = (line[0], line[10])
                        if newCity not in cityData:
                                cityData[newCity] = {'lat': float(line[2]), 'lng': float(line[3]),
                                                     'country': line[4], 'iso2': line[5], 'adminName': line[7],
                                                     'pop': line[9], 'hit': 0, 'duration' : 0}

        def countHit(cityDict: dict, dataPath: str) -> None:
                """
                Counts the number of hurricane hits and total duration each city experiences based on hurricane proximity.

                This function reads hurricane track data, computes the distance between cities and hurricane points,
                and determines if a city falls within the impact radius of the hurricane. It tracks the number of hits
                and the cumulative time each city spends within the hurricane's range.

                Args:
                     cityDict (dict): Dictionary containing the city data processed in the outer function.
                                      The dictionary stores details such as latitude, longitude, country, population,
                                      number of hits ('hit'), and total duration ('duration') for each city.
                     dataPath (str): The file path of the hurricane data file to process.
                """
                with open(dataPath, mode='r') as file:
                        hitStartTime = {key: None for key in cityDict}
                        cityInRange = {key: False for key in cityDict}  # Track if each city is currently hit
                        check = set()
                        for line in file:

                                newRow = line.split(',')

                                if len(newRow) <= 4:
                                        hitStartTime = {key: None for key in cityDict}
                                        cityInRange = {key: False for key in cityDict}  # Reset the in-range flags
                                        check = set()
                                        continue

                                curLatitude, curLongitude = float(newRow[4][:-1]), normalizeLongitude(newRow[5])
                                curHurricaneTime = datetime.strptime(newRow[0]+ " " + newRow[1] , '%Y%m%d %H%M')  # Parse hurricane timestamp

                                # Filter by proximity to avoid unnecessary distance calculations
                                for key, item in cityDict.items():
                                        cityLatitude, cityLongitude = item['lat'], item['lng']

                                        distance = calculateDist(curLatitude,curLongitude,cityLatitude,cityLongitude)

                                        if distance > 50:
                                            continue

                                        radius = 40 if int(newRow[0][:4]) < 2004 else float(newRow[16 + determineQuadrant(calculateAzimuth(curLatitude, curLongitude, cityLatitude, cityLongitude))])
                                        radius = 40 if radius == -999 else radius

                                        if distance <= radius :
                                                if int(newRow[0][:4]) < 2004:
                                                    if float(newRow[6]) < 63 :
                                                        continue
                                                if not cityInRange[key]:
                                                        if key[1] not in check :
                                                                check.add(key[1])
                                                                item['hit'] += 1
                                                        cityInRange[key] = True
                                                        hitStartTime[key] = curHurricaneTime
                                                else :
                                                        # If already in range, update the duration for this city
                                                        hurricaneDuration = (curHurricaneTime - hitStartTime[key]).total_seconds() / 3600  # in hours
                                                        item['duration'] += hurricaneDuration
                                                        hitStartTime[key] = curHurricaneTime  # Update start time for next duration calculation
                                        else :
                                                if cityInRange[key]:
                                                        cityInRange[key] = False
                                                        hitStartTime[key] = None  # Reset start time as city is out of range

        countHit(cityData, 'hurdat2_pacific.txt')
        countHit(cityData, 'hurdat2_atlantic.txt')

        return cityData

def determineQuadrant(degree : int) -> int:
    """
    Determines the quadrant of a circle based on the given degree.

    Parameters:
         degree (int): The degree (angle) to determine the quadrant for. It should be in the range [0, 360).

    Returns:
         int: The quadrant number (0, 1, 2, or 3) corresponding to the given degree.
              If the degree is not in the valid range (0 <= degree < 360), the function will still return a value based on the provided logic.
   """
    if 0 < degree < 90 :
        return 0
    elif 90 < degree < 180 :
        return 1
    elif 180 < degree < 270 :
        return 2
    else:
        return 3

def outPutData (data : dict) -> None:
    """
    Writes city data to an output file in a tabular format.

   Parameters:
           data (dict): A dictionary where each key is a tuple containing the city ID and city name, and each value is
                        a dictionary containing the city attributes such as country, latitude, longitude, population,
                        and the number of hurricanes that have hit the city.

   Returns:
          None
   """
    with open('output.txt', 'w') as file:
                # Write header
                file.write(f'{"ID":<25}{"City Name":<35}{"Country Name":<25}{"Latitude":<10}{"Longitude":<10}{"population":<15}{"HitBy":<10}{"Duration":<15}\n')

                # Write each storm's data
                for key, value in data.items():
                        # Calculate days and hours from duration
                        cityid = key[1]
                        cityName = key[0]
                        countryName = value['country']
                        latitude = value['lat']
                        longitude = value['lng']
                        population = value['pop']
                        hitby = value['hit']
                        duration = round(value['duration'])

                        # Format each row's data to align under the headers
                        file.write(
                                f"{cityid:<25}{cityName:<35}{countryName:<25}{str(latitude):<10}{str(longitude):<10}{str(population):<15}{str(hitby):<10}{str(duration):<15}\n")

if __name__ == "__main__":

        result = processData('simplemaps_worldcities_basicv1.77/worldcities.csv',500000)
        sorted_data = dict(sorted(result.items(), key=lambda item: item[1]['hit'], reverse=True))
        outPutData(sorted_data)