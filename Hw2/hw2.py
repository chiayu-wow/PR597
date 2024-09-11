import  sys

# Dictionaries to store CO2 data
data_hawaii = {}  # Stores total CO2 levels for each year in Hawaii
data_alaska = {}  # Stores total CO2 levels for each year in Alaska

days_Alaska = {}  # Stores number of valid data entries for each year in Alaska
days_Hawaii = {}  # Stores number of valid data entries for each year in Hawaii

max_data_alaska = {}  # Stores maximum CO2 level for each year in Alaska
max_data_hawaii = {}  # Stores maximum CO2 level for each year in Hawaii

with open("co2_alaska.txt", "r") as file:
    for line in file:
        # Skip empty lines or comments
        if not line.strip() or line.startswith("#"):
            continue

        data = line.split()

        if data[1] not in data_alaska:
            data_alaska[data[1]] = 0
        if data[1] not in max_data_alaska:
            max_data_alaska[data[1]] = sys.float_info.min
        if data[1] not in days_Alaska:
            days_Alaska[data[1]] = 0

        if not data[16].startswith('*'):
          days_Alaska[data[1]] = days_Alaska[data[1]] + 1
          data_alaska[data[1]] += float((data[7]))
          max_data_alaska[data[1]] = max(max_data_alaska[data[1]], float(data[7]))


with open("co2_hawaii.txt", "r") as file:
    for line in file:
        # Skip empty lines or comments
        if not line.strip() or line.startswith("#"):
            continue

        data = line.split()

        if data[1] not in data_hawaii:
            data_hawaii[data[1]] = 0
        if data[1] not in max_data_hawaii:
            max_data_hawaii[data[1]] = sys.float_info.min
        if data[1] not in days_Hawaii:
            days_Hawaii[data[1]] = 0

        if not data[16].startswith('*'):
          days_Hawaii[data[1]] = days_Hawaii[data[1]] + 1
          data_hawaii[data[1]] += float((data[7]))
          max_data_hawaii[data[1]] = max(max_data_hawaii[data[1]], float(data[7]))

data = {'Alaska': {}, 'Hawaii':{}}




for key in data_alaska.keys():
    if days_Alaska[key] != 0:
        data['Alaska'][key] = { 'MEAN_LEVEL' : round(data_alaska[key]/days_Alaska[key], 2) ,'MAX_LEVEL': max_data_alaska[key]}
    else:
        data['Alaska'][key] = {'MEAN_LEVEL' : 0, 'MAX_LEVEL': 0}
    if days_Hawaii[key] != 0:
        data['Hawaii'][key] = {'MEAN_LEVEL' : round(data_hawaii[key]/days_Hawaii[key],2) ,'MAX_LEVEL': max_data_hawaii[key]}
    else:
        data['Hawaii'][key] = {'MEAN_LEVEL' : 0, 'MAX_LEVEL': 0}

with open("co2_summary.txt", "w") as file:
    # Write headers
    file.write(f'Alaska\t\t\t\t\t\t\t\t\tHawaii\n')
    file.write(f"Year\tMAX_LEVEL\tMEAN_LEVEL\t%CHANGE\t\tMAX_LEVEL\tMEAN_LEVEL\t%CHANGE\n")

    prev_mean_hawaii = None
    prev_mean_alaska = None
    count = 0
    for year in sorted(data['Alaska'].keys()):
        ### for Alaska
        mean_level = data['Alaska'][year]['MEAN_LEVEL']

        if data['Alaska'][year]['MAX_LEVEL'] == sys.float_info.min:
            max_level = 0
        else:
            max_level = data['Alaska'][year]['MAX_LEVEL']

        percent_change = "-----"  # Default value if no previous year
        if prev_mean_alaska is not None and mean_level != 0:
            percent_change = ((mean_level - prev_mean_alaska) / prev_mean_alaska) * 100
            percent_change = f"{percent_change:.2f}%"
        file.write(f"{year}\t\t{max_level:.2f}\t\t{mean_level:.2f}\t\t{percent_change}\t\t")

        if mean_level != 0:
            prev_mean_alaska = mean_level

        ##### for Hawaii
        mean_level_H = data['Hawaii'][year]['MEAN_LEVEL']

        if data['Alaska'][year]['MAX_LEVEL'] == sys.float_info.min:
            max_level_H = 0
        else:
            max_level_H = data['Hawaii'][year]['MAX_LEVEL']

        percent_change = "-----"
        if prev_mean_hawaii is not None and mean_level_H != 0:
            percent_change = ((mean_level_H - prev_mean_hawaii) / prev_mean_hawaii) * 100
            if percent_change != "-----":
                if float(percent_change) < 0:
                    count+=1
            percent_change = f"{percent_change:.2f}%"
        file.write(f"{max_level_H:.2f}\t\t{mean_level_H:.2f}\t\t{percent_change}\n")

        if mean_level_H != 0:
            prev_mean_hawaii = mean_level_H