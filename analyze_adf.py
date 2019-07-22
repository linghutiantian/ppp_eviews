import os
import re
import glob
import csv
from xlsxwriter.workbook import Workbook

common_countries_ = list(csv.reader(open("all_countries.csv")))
common_countries = [ y for x in common_countries_ for y in x]

file_name_to_country = {}
ppp_countries = []

def parse_country_name(name):
  name = re.sub('[^0-9a-zA-Z]+', '_', name)
  return name.upper()

for val in common_countries:
  file_name_to_country[parse_country_name(val).lower()] = val

def file_to_name(file):
  country = file[13:-8]
  return file_name_to_country[country]

workbook = Workbook('adf_output' + '.xlsx', {'strings_to_numbers':True})
worksheet = workbook.add_worksheet()

cell_format1 = workbook.add_format()
cell_format1.set_font_color('red')
cell_format2 = workbook.add_format()
cell_format2.set_bg_color('green')

row = 0
worksheet.write(row, 0, 'Country')
worksheet.write(row, 1, 'T stat')
worksheet.write(row, 2, '1%')
worksheet.write(row, 3, '5%')
worksheet.write(row, 4, '10%')
worksheet.write(row, 5, 'PPP')
row = row + 1

total = 0
ppp_count = 0
ppp_dist = [0, 0, 0]

for csv_file in glob.glob(os.path.join('./adf_result/', '*.csv')):
  adf = list(csv.reader(open(csv_file)))
  t = adf[6][3]
  p = [adf[7][3], adf[8][3], adf[9][3]]
  ppp = False
  worksheet.write(row, 0, file_to_name(csv_file))
  worksheet.write(row, 1, t)
  cell_format = cell_format1
  for i in range(3):
    if float(t) <= float(p[i]):
      ppp = True
      cell_format = cell_format2
      ppp_dist[i] = ppp_dist[i] + 1
    worksheet.write(row, 2 + i, p[i], cell_format)
  if ppp:
    ppp_count = ppp_count + 1
    ppp_countries.append(file_to_name(csv_file))
  worksheet.write(row, 5, ppp, cell_format)
  row = row + 1
  total = total + 1
print(total, ppp_count, ppp_dist)
ppp_countries.sort()
ppp_countries_str = ""
for i in ppp_countries:
  ppp_countries_str += (i + ", ")
print(ppp_countries_str)




workbook.close()
