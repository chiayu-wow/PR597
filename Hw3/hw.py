from datetime import datetime

Origin_in_Tropical = 0
Stayed_In_Tropical = 0

count = 0## count how many storms data in all hurdat2 files

date_format = "%Y%m%d %H%M"
year = {}

def DetermineCategory(n):
    if n >= 64 and n <= 82:
        return "Cat1"
    elif n >= 83 and n <= 95:
        return "Cat2"
    elif n >= 96 and n <= 112:
        return "Cat3"
    elif n >= 113 and n <= 136:
        return "Cat4"
    elif n >= 137:
        return "Cat5"
    else:
        return "None"

def processdata(filepath: str, yearDict):
    storms = {}  ## stored all storms data  in atlantic
    cur_Time = None
    isInsideTropical = False
    global count
    global Origin_in_Tropical
    global Stayed_In_Tropical
    with open(filepath, 'r') as file:
        cur_storm = ""
        for line in file:
            # Process each line
            tmp = line.split(',')
            for i, data in enumerate(tmp):
                tmp[i] = data.strip()
            ## encounter to a new storm
            if len(tmp) <= 4:
                ## if it originates in the tropics
                if isInsideTropical:
                    Stayed_In_Tropical += 1
                isInsideTropical = False

                ## track total number of hurricane
                count += 1
                storms[tmp[0]] = {}

                ##stored storm's name
                if tmp[1] != 'UNNAMED':
                    storms[tmp[0]]['name'] = tmp[1]
                ##intialize all attribute for current storm
                cur_storm = tmp[0]
                storms[cur_storm]['duration'] = 0
                storms[cur_storm]['landfalls'] = 0
                storms[cur_storm]['ID'] = tmp[0]
                cur_Time = None

                year = tmp[0][4:]
                if year not in yearDict:
                    yearDict[year] = {}
                    yearDict[year]['count'] = 0
                    yearDict[year]['Cat1'] = 0
                    yearDict[year]['Cat2'] = 0
                    yearDict[year]['Cat3'] = 0
                    yearDict[year]['Cat4'] = 0
                    yearDict[year]['Cat5'] = 0
                yearDict[year]['count'] += 1
            else:
                ## check if the first data of this storm is in tropics
                if cur_Time is None:
                    if float(tmp[4][:-1]) <= 23.436:
                        Origin_in_Tropical += 1
                        isInsideTropical = True
                else:
                    ## check any of data of current storm is outside of tropics
                    if float(tmp[4][:-1]) > 23.436:
                        isInsideTropical = False

                ## track the Maximum sustained wind
                if 'max_wind' not in storms[cur_storm]:
                    storms[cur_storm].setdefault("max_wind", 0)
                storms[cur_storm]['max_wind'] = max(int(tmp[6]), storms[cur_storm]['max_wind'])

                ## track the duration (in hours)
                if cur_Time is None:
                    cur_Time = tmp[0] + " " + tmp[1]
                else:
                    prev_Time = cur_Time
                    cur_Time = tmp[0] + " " + tmp[1]

                    current_datetime = datetime.strptime(cur_Time, date_format)
                    previous_datetime = datetime.strptime(prev_Time, date_format)

                    time_difference = (current_datetime - previous_datetime).total_seconds() / 3600.0
                    storms[cur_storm]['duration'] += time_difference

                ##check the LandFall
                if tmp[2] == 'L':
                    if int(tmp[6]) >= 64:
                        storms[cur_storm]['landfalls'] += 1

                ## Determine each landfall's category
                if DetermineCategory(int(tmp[6])) != "None" and tmp[2] == "L":
                    yearDict[year][DetermineCategory(int(tmp[6]))] += 1

    if isInsideTropical:
        Stayed_In_Tropical += 1
    print(count)
    return storms

def outputData(inputData, Region):
    # Open file in append mode
    with open('output.txt', 'a') as file:
        # Write header
        file.write(f'{Region}\n')
        file.write(f'{"ID":<15}{"Name":<20}{"Duration":<25}{"Landfalls":<15}{"MaxWind":<10}\n')

        # Write each storm's data
        for key, value in inputData.items():
            # Calculate days and hours from duration
            duration_hours = value.get('duration', 0)
            days = duration_hours // 24
            hours = duration_hours % 24
            time = f'{days} days {hours} hours'

            # Handle missing 'name' gracefully
            name = value.get('name', '')  # Default to an empty string if 'name' is missing

            # Format each row's data to align under the headers
            file.write(f"{key:<15}{name:<20}{time:<25}{str(value['landfalls']):<15}{str(value['max_wind']):<10}\n")

def outputDataByYear(yearDict):
    # Define column widths
    width_year = 6
    width_storms = 8
    width_cat = 6

    # Open file for writing
    with open('outputByYear.txt', 'w') as file:
        # Write header
        header = (
            f'{"Year".ljust(width_year)}'
            f'{"Storms".ljust(width_storms)}'
            f'{"Cat1".ljust(width_cat)}'
            f'{"Cat2".ljust(width_cat)}'
            f'{"Cat3".ljust(width_cat)}'
            f'{"Cat4".ljust(width_cat)}'
            f'{"Cat5".ljust(width_cat)}\n'
        )
        file.write(header)

        # Write each line of data
        for key, value in yearDict.items():
            line = (
                f'{str(key).ljust(width_year)}'
                f'{str(value["count"]).ljust(width_storms)}'
                f'{str(value["Cat1"]).ljust(width_cat)}'
                f'{str(value["Cat2"]).ljust(width_cat)}'
                f'{str(value["Cat3"]).ljust(width_cat)}'
                f'{str(value["Cat4"]).ljust(width_cat)}'
                f'{str(value["Cat5"]).ljust(width_cat)}\n'
            )
            file.write(line)

storms_atlantic = processdata("hurdat2_atlantic.txt", year)
storms_pacific = processdata("hurdat2_pacific.txt", year)

outputData(storms_atlantic, "Atlantic")
outputData(storms_pacific, "Pacific")

outputDataByYear(year)

print(f'{round(Origin_in_Tropical/count*100,2)}% of all storms ORIGINATE within the Tropics')
print(f'{round(Stayed_In_Tropical/count*100,2)}% of all storms STAYED ENTIRELY within the Tropics')