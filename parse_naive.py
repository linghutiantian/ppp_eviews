import csv
import re

debug = False

exchange_rates = list(csv.reader(open("exchange_rates.csv")))
cpis = list(csv.reader(open("cpi.csv")))
common_countries_ = list(csv.reader(open("all_countries.csv")))
common_countries = [ y for x in common_countries_ for y in x]

exchange_rate_countries = exchange_rates[0][1:]
cpi_countries = cpis[0][1:]

if debug:
  print("cpi countries: ", len(exchange_rate_countries), " cpi countries: ", len(cpi_countries), " all coutries: ", len(common_countries))
  print("intsection countries: ", len(set(exchange_rate_countries).intersection(set(cpi_countries))))

exchange_rate_col_indices = [0]
cpi_col_indices = []

# Don't forget to add 1 to get the real index!!
for idx, val in enumerate(exchange_rate_countries):
  if val in common_countries:
    exchange_rate_col_indices.append(idx + 1)
if debug:
  print("num er_idx: ", len(exchange_rate_col_indices));

for idx, val in enumerate(cpi_countries):
  if val in common_countries:
    cpi_col_indices.append(idx + 1)
if debug:
  print("num cpi_idx: ", len(cpi_col_indices));

def parse_country_name(name):
  name = re.sub('[^0-9a-zA-Z]+', '_', name)
  return name.upper()

if debug:
  print("num_row_er: ", len(exchange_rates), " num_row_cpi: ", len(cpis))

final_table = []

# Process country names first
final_table.append([])
for index in exchange_rate_col_indices:
  country = parse_country_name(exchange_rates[0][index])
  if index != 0:
    country += "_ER"
  final_table[0].append(country)

for index in cpi_col_indices:
  country = parse_country_name(cpis[0][index])
  country += "_CPI"
  final_table[0].append(country)

for row in exchange_rates[1:]:
  selected = [row[index] for index in exchange_rate_col_indices]
  final_table.append(selected)

rol_num = 0
for row in cpis[1:]:
  selected = [row[index] for index in cpi_col_indices]
  final_table[rol_num] += selected
  rol_num += 1

out = open('final_data_naive.csv', 'wb')
writer = csv.writer(out)

for row in final_table:
  writer.writerow(row)
