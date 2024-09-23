def consider_city_hit_by_quadrant(lat_0, lng_0, lat_1, lng_1, wind_speed, wind_quadrant):
    """
    Determines if a city is hit by a hurricane based on the wind quadrants and the city's location.

    :param lat_0: Latitude of the hurricane.
    :param lng_0: Longitude of the hurricane.
    :param lat_1: Latitude of the city.
    :param lng_1: Longitude of the city.
    :param wind_speed: The wind speed of the hurricane.
    :param wind_quadrant: The wind quadrant distances (nautical miles) in four directions.
    :returns: True if the city is hit by the hurricane, False otherwise.
    """
    # Calculate distance between the hurricane's eye and the city
    if abs(lat_1 - lat_0) >= 1:
        hurricane_city_distance = 111  # km, if latitude difference is 1 degree or more
    else:
        g = geod.Inverse(lat_0, lng_0, lat_1, lng_1)
        hurricane_city_distance = g['s12'] / 1000  # Convert to kilometers

    # Determine if city is hit based on wind speed and distance
    if -999 in wind_quadrant:  # missing data -> original way
        if wind_speed > 63 and hurricane_city_distance <= 40:
            return True
        else:
            return False
    else:
        if hurricane_city_distance == 111:
            return False
        else:
            # Determine the heading (azimuth) and the direction (quadrant)
            g = geod.Inverse(lat_0, lng_0, lat_1, lng_1)
            heading = g['azi1']
            direction = ""
            if 0 <= heading < 90:
                direction = "NE"
            elif 90 <= heading < 180:
                direction = "SE"
            elif -180 <= heading < -90:
                direction = "SW"
            elif -90 <= heading < 0:
                direction = "NW"

            # Calculate the quadrant's hurricane distance (minimum 20 nautical mile + wind quadrant distance)
            if direction == "NE":
                quadrant_hurricane_distance = 20 + wind_quadrant[0]  # nautical mile + nautical mile
            elif direction == "SE":
                quadrant_hurricane_distance = 20 + wind_quadrant[1]
            elif direction == "SW":
                quadrant_hurricane_distance = 20 + wind_quadrant[2]
            elif direction == "NW":
                quadrant_hurricane_distance = 20 + wind_quadrant[3]
            else:
                quadrant_hurricane_distance = 20  # Default

            # Compare hurricane's eye to city distance vs quadrant hurricane distance
            if wind_speed > 63 and (hurricane_city_distance * 1000 / 1852) <= quadrant_hurricane_distance:  # hit
                return True
            else:
                return False