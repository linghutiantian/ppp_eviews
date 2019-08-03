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

workbook = Workbook('coi_output' + '.xlsx', {'strings_to_numbers':True})
worksheet = workbook.add_worksheet()

cell_format1 = workbook.add_format()
cell_format1.set_font_color('red')
cell_format2 = workbook.add_format()
cell_format2.set_bg_color('green')

row = 0
worksheet.write(row, 0, 'Country')
worksheet.write(row, 1, 'ST')
worksheet.write(row, 2, 'PDIFF')
worksheet.write(row, 3, 'RESID')
worksheet.write(row, 4, 'RESULT')
row = row + 1

country_dict = {}
p_name = ["1%", "5%", "10%"]

def read_folder(path, name):
  for csv_file in glob.glob(os.path.join('./' + path + '/', '*.csv')):
    country = file_to_name(csv_file)
    adf = list(csv.reader(open(csv_file)))
    t = adf[6][3]
    p = [adf[7][3], adf[8][3], adf[9][3]]
    val = "NS"
    for i in range(3):
      if float(t) <= float(p[i]):
        val = p_name[i]
        break
    if not country in country_dict:
      country_dict[country] = {}
    country_dict[country][name] = val


read_folder("stt_result", "ST")
read_folder("pdf_result", "PDIFF")
read_folder("res_result", "RES")


countries = list(country_dict.keys())
countries.sort()

tests = ["ST", "PDIFF", "RES"]

for country in countries:
  worksheet.write(row, 0, country)
  col = 1
  for test in tests:
    val = country_dict[country][test]
    cell_format = cell_format2
    if val == "NS":
      cell_format = cell_format1
    elif test == "RES":
      print(country)
    worksheet.write(row, col, val, cell_format)
    col = col + 1
  if country_dict[country]["ST"] == "NS" and country_dict[country]["PDIFF"] == "NS" and country_dict[country]["RES"] != "NS":
     worksheet.write(row, col, "PPP", cell_format2)
  row = row + 1


workbook.close()
