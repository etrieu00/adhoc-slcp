import csv
with open('plans.csv','r') as planscsv, \
     open('zips.csv','r') as zipscsv, \
     open('slcsp.csv','r') as slcspcsv, \
     open('out.csv', 'w') as out:
    # Remove headers
    _ ,*plans = csv.reader(planscsv,delimiter=',')
    _ ,*zips = csv.reader(zipscsv,delimiter=',')
    _ ,*slcsp= csv.reader(slcspcsv,delimiter=',')
    selectedZipCodes = dict()
    silverPlansForEachArea = dict()
    filteredSilvers = dict()
    zipsAndRatesForAll = dict()
    # Get all the zip codes I need to find
    zipCodes = [row[0] for row in slcsp]
    # Get all the zip codes I am interested and include all the states along with the rate area
    for row in zips:
        if row[0] in zipCodes:
            # Needs to be a set to remove the duplicates
            selectedZipCodes.setdefault(row[0],set()).add(row[1] + '-' + row[4])
    # Make a list of rates for all areas that belong together
    for row in [row for row in plans if row[2] == 'Silver']:
        silverPlansForEachArea.setdefault(row[1] + '-' + row[4],[]).append(row[3])
    # Filter out and get all the second lowest prices
    for key, value in silverPlansForEachArea.items():
        if len(value) >=2:
            filteredSilvers[key] = sorted(value)[1]
        elif len(value) == 1:
            filteredSilvers[key] = value[0]
    # Get all the rates for each zip code
    for key, row in selectedZipCodes.items():
        for values in row:
            zipsAndRatesForAll.setdefault(key,[]).append(filteredSilvers.get(values))
    # Only write the rates for zip codes that have one rate and ignore the empty and ambiguous
    for key, items in zipsAndRatesForAll.items():
        if(None in items or len(items) >= 2):
            out.write(key + ',\n')
        else:
            out.write(key + ',' + items[0] + '\n')