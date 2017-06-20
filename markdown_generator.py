import requests
import time
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
        temp = [datum['station_nm'], datum['site_no'], datum['huc_cd'], ""]
        temp[3] = "[link](./Pages/" + temp[1] + ".html)"
    if temp not in lst:
        lst.append(temp)
        slug = temp[1] + ".md"
        with open(slug, "w") as f:
            f.write("Title: " + temp[1] + "\n")
            f.write("Date: " + time.strftime("%y-%m-%d %H:%M \n"))
            f.write("Category: DataPage\n")
            f.write("status: hidden\n")
            f.write("\n")
            f.write("Station name: " + temp[0] + "\n\n")
            f.write("Site number: " + temp[1] + "\n\n")
            f.write("Hydrologic unit code: " + temp[2] + "\n\n")


# function to print the data as an html table
with open("DataTable.md", "w") as f:
    f.write("Title: Stream Gage Table\n")
    f.write("Date: " + time.strftime("%y-%m-%d %H:%M \n"))
    f.write("Category: Data\n")
    f.write('| Name and location | Site number | Hydrologic unit code | More information |\n')
    f.write('| --- | --- | --- | --- |\n')
    for sublist in lst:
        f.write(' | '.join(sublist))
        f.write("\n")

