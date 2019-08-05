import os
import re
import glob
import csv
from xlsxwriter.workbook import Workbook

common_countries_ = list(csv.reader(open("all_countries.csv")))
common_countries = [ y for x in common_countries_ for y in x]

file_name_to_country = {}
def parse_country_name(name):
  name = re.sub('[^0-9a-zA-Z]+', '_', name)
  return name.upper()

for val in common_countries:
  file_name_to_country[parse_country_name(val).lower()] = val

def file_to_name(file):
  country = file[13:-8]
  return file_name_to_country[country]

workbook = Workbook('adf_output_1' + '.xlsx', {'strings_to_numbers':True})
worksheet = workbook.add_worksheet()

cell_format1 = workbook.add_format()
cell_format1.set_align('right')


row = 0
col_offsets = [0, 4]
for i in range(2):
  col_offset = col_offsets[i]
  worksheet.write(row, col_offset + 0, '')
  worksheet.write(row, col_offset + 1, 'Obs')
  worksheet.write(row, col_offset + 2, 't-statistic')
  worksheet.write(row, col_offset + 3, '')
row = row + 1

offset = 0


csv_files = glob.glob(os.path.join('./adf_result/', '*.csv'))
csv_files.sort()
for csv_file in csv_files:
  col_offset = col_offsets[offset]
  adf = list(csv.reader(open(csv_file)))
  t = adf[6][3]
  p = [adf[7][3], adf[8][3], adf[9][3]]
  ppp = False
  # print(file_to_name(csv_file), row, col_offset)
  worksheet.write(row, 0 + col_offset, file_to_name(csv_file))
  star_list = ['***', '** ', '*  ']
  star = '   '
  for i in range(3):
    if float(t) <= float(p[i]):
      ppp = True
      star = star_list[i]
      print(file_to_name(csv_file))
      break
  worksheet.write_string(row, 2 + col_offset, t, cell_format1)
  worksheet.write_string(row, 3 + col_offset, star)
  # parse num of samples
  sample_line = adf[19][0]
  pattern = ': (\d+) after adjustments'
  a = re.search(pattern, sample_line)
  if not a:
    sample_line = adf[20][0]
    a = re.search(pattern, sample_line)
    if not a:
      sample_line = adf[21][0]
      a = re.search(pattern, sample_line)
  num_sample = a.group(1)
  worksheet.write(row, 1 + col_offset, num_sample)

  offset = 1 - offset
  if offset == 0:
    row = row + 1

workbook.close()
