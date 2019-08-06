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
  country = file[21:-8]
  return file_name_to_country[country]

workbook = Workbook('coi_new_output' + '.xlsx', {'strings_to_numbers':False})
worksheet = workbook.add_worksheet()

cell_format_left = workbook.add_format()
cell_format_left.set_align('left')

cell_format_center = workbook.add_format()
cell_format_center.set_align('center')

row = 0
worksheet.write(row, 0, 'Country')
worksheet.write(row, 1, 'PT')
worksheet.write(row, 2, 'PT 1st')
worksheet.write(row, 3, 'ST')
worksheet.write(row, 4, 'ST 1st')
worksheet.write(row, 5, 'RES')
row = row + 1

country_dict = {}
p_name = ["1%", "5%", "10%"]
stars = ["***", "** ", "*  "]

def read_folder(path):
  for csv_file in glob.glob(os.path.join('./' + path + '/', '*.csv')):
    country = file_to_name(csv_file)
    name = csv_file[10:13]
    adf = list(csv.reader(open(csv_file)))
    t = adf[6][3]
    p = [adf[7][3], adf[8][3], adf[9][3]]
    star = "   "
    for i in range(3):
      if float(t) <= float(p[i]):
        val = p_name[i]
        star = stars[i]
        break
    if not country in country_dict:
      country_dict[country] = {}
    country_dict[country][name] = t + star


read_folder("coi_new")


countries = list(country_dict.keys())
countries.sort()

tests = ["ptt", "dpt", "stt", "dst", "res"] #, "rm1", "rm2", "rm3"]
need_star = ["dpt", "dst"]
no_star = ["ptt", "stt"]

skip_countries = []

for country in countries:
  worksheet.write(row, 0, country)
  if country in country_dict:
    col = 1
    skip = False
    for test in tests:
      if test in country_dict[country]:
        if skip:
          val = "-"
          worksheet.write_string(row, col, val, cell_format_center)
        else:
          val = country_dict[country][test]
          worksheet.write_string(row, col, val, cell_format_left)
          if test == "res" and "*" in val:
            print(country)
          if test in need_star and "*" not in val:
            skip = True
          if test in no_star and "*" in val:
            skip = True
          if skip:
            skip_countries.append(country)
      else:
        val = "-"
        worksheet.write_string(row, col, val, cell_format_center)
        skip = True
        skip_countries.append(country)
      col = col + 1
  row = row + 1

workbook.close()

workbook2 = Workbook('coi_new_model_output' + '.xlsx', {'strings_to_numbers':False})
worksheet2 = workbook2.add_worksheet()

row = 0
worksheet2.write(row, 0, 'Country')
worksheet2.write(row, 1, '3val res')
worksheet2.write(row, 2, 'model 1 res')
worksheet2.write(row, 3, 'model 2 res')
worksheet2.write(row, 4, 'model 3 res')
row = row + 1

yes_no = []
no_yes = []

tests = ["res", "rm1", "rm2", "rm3"]
for country in countries:
  if country in skip_countries:
    continue
  if country in country_dict:
    val = country
    worksheet2.write_string(row, 0, val, cell_format_left)
    col = 1
    three_val_adf = False
    for test in tests:
      val = "x"
      if test not in country_dict[country]:
        print("Bad!!!!!!", country, test)
      val = country_dict[country][test]
      if (test == "res") and "*" in val:
        three_val_adf = True
      if (test != "res") and three_val_adf == True and "*" not in val:
        yes_no.append(country)
      if (test != "res") and three_val_adf == False and "*" in val:
        no_yes.append(country)
      worksheet2.write_string(row, col, val, cell_format_center)
      col = col + 1
    row = row + 1

workbook2.close()

print len(list(set(yes_no)))
print len(list(set(no_yes)))


