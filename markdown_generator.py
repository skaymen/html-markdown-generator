import requests
import csv
from pprint import pprint

url = "https://waterservices.usgs.gov/nwis/site?format=rdb&stateCd=mo&outputDataTypeCd=iv,dv&siteType=ST&siteStatus=active&hasDataTypeCd=iv,dv"

req = requests.get(url)

# Discard preamble from response
data = req.text[req.text.rindex('#') + 1:]
data = data[data.index('\n') + 1:]
# the first line of data is now the column headers

# turn data into list by splitting on \n
data = data.split('\n')

# discard 2nd line
data = [data[0]] + data[2:]

# print(len(data))
fields = data[0].split('\t')
data_nice = []
for line in data[1:]:
    line = line.split('\t')
    line_dict = dict(zip(fields, line))
    data_nice.append(line_dict)

# print(len(data_nice))
# pprint(data_nice[0])

lst = []

# create a list of lists with relevant data
for datum in data_nice:
    if 'station_nm' in datum.keys():
        temp = [datum['station_nm'], datum['site_no'], datum['huc_cd']]
    lst.append(temp)

# function to print the data as an html table
def markdown_table(arr):
    print('Name and location | Site number | Hydrologic unit code')
    print('--- | --- | ---')
    for sublist in arr:
        print(' | '.join(sublist))

markdown_table(lst)