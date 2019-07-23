import csv
import re

exception = ["Moldova", "Guadeloupe", "Zimbabwe"]

debug = False

exchange_rates = list(csv.reader(open("exchange_rates.csv")))
cpis = list(csv.reader(open("cpi.csv")))
common_countries_ = list(csv.reader(open("all_countries.csv")))
common_countries = [ y for x in common_countries_ for y in x]

exchange_rate_countries = exchange_rates[0][1:]
cpi_countries = cpis[0][1:]

exchange_rate_col_indices = [0]
cpi_col_indices = []

er_idx_to_country = {}
cpi_idx_to_country = {}

er_country_to_idx = {}
cpi_country_to_idx = {}

# Don't forget to add 1 to get the real index!!
for idx, val in enumerate(exchange_rate_countries):
  if val in common_countries:
    # exchange_rate_col_indices.append(idx + 1)
    er_idx_to_country[idx + 1] = val
    er_country_to_idx[val] = idx + 1
if debug:
  print("num er_idx: ", len(exchange_rate_col_indices));

for idx, val in enumerate(cpi_countries):
  if val in common_countries:
    # cpi_col_indices.append(idx + 1)
    cpi_idx_to_country[idx + 1] = val
    cpi_country_to_idx[val] = idx + 1

def parse_country_name(name):
  name = re.sub('[^0-9a-zA-Z]+', '_', name)
  return name.upper()


er_dict = {}
cpi_dict = {}
rol_to_month = {}
month_to_rol = {}

for idx, row in enumerate(exchange_rates):
  if idx == 0:
    continue
  for col, val in enumerate(row):
    rol_to_month[idx] = row[0]
    month_to_rol[row[0]] = idx
    if val == "...":
      continue
    if er_idx_to_country.get(col):
      country = er_idx_to_country[col]
      if not er_dict.get(country):
        er_dict[country] = {}
      if val == "0" or val == "-":
        val = ""
      er_dict[country][idx] = val

for idx, row in enumerate(cpis):
  if idx == 0:
    continue
  for col, val in enumerate(row):
    if not val:
      continue
    if cpi_idx_to_country.get(col):
      country = cpi_idx_to_country[col]
      if not cpi_dict.get(country):
        cpi_dict[country] = {}
      cpi_dict[country][idx] = val

threshold = 0
er_filter_country = []
cpi_filter_country = []

for country in er_dict:
  if len(er_dict[country]) > threshold:
    er_filter_country.append(country)

for country in cpi_dict:
  if len(cpi_dict[country]) > threshold:
    cpi_filter_country.append(country)

filter_country_set = set(er_filter_country) & set(cpi_filter_country)
for i in exception:
  filter_country_set.remove(i)
filter_country = list(filter_country_set)
filter_country.sort()

filter_country_final = []
for country in filter_country:
  er_idx = set(er_dict[country].keys())
  cpi_idx = set(cpi_dict[country].keys())
  if len(er_idx & cpi_idx) < 10:
    print("no intersection:", country)
  else:
    filter_country_final.append(country)

country_out = open('unit_root_countries.csv', 'wb')
country_writer = csv.writer(country_out)
country_writer.writerow(filter_country_final)


# china = "China, P.R.: Mainland"
# print(len(er_dict[china]), len(cpi_dict[china]))
# print(filter_country, len(filter_country))

# final_table = []
out = open('final_unit_root_data_2.csv', 'wb')
writer = csv.writer(out)
# 
# for row in final_table:
#   writer.writerow(row)

row_0 = ["DATE"]
for country in filter_country_final:
  row_0.append(parse_country_name(country) + "_ER")
for country in filter_country_final:
  row_0.append(parse_country_name(country) + "_CPI")
writer.writerow(row_0)


row_start = month_to_rol["1960M01"]
row_end = month_to_rol["2018M12"]

bad_country = []
for i in range(row_start, row_end + 1):
  row = [rol_to_month[i]]
  for country in filter_country_final:
    if i not in er_dict[country]:
      row.append("")
      bad_country.append(country + "_ER")
    else:
      row.append(er_dict[country][i])
  for country in filter_country_final:
    if i not in cpi_dict[country]:
      row.append("")
      bad_country.append(country + "_CPI")
    else:
      row.append(cpi_dict[country][i])
  writer.writerow(row)

# if len(bad_country):
#   print set(bad_country)


oecd_countries_ = list(csv.reader(open("oecd.csv")))
oecd_countries = [ y for x in oecd_countries_ for y in x]
oecd_countries.sort()

oecd_string = ""
for oecd_country in oecd_countries:
  oecd_string += (oecd_country + ", ")
  if not er_dict.get(oecd_country):
    print(oecd_country)
print(oecd_string)

panal_out = open('final_panal_data.csv', 'wb')
panal_writer = csv.writer(panal_out)

panal_row_0 = ["DATE", "COUNTRY", "CPI", "CPI_US", "ER"]
panal_writer.writerow(panal_row_0)

oecd_exceptions = ["Estonia", "Slovak Republic"]

common_rol = set(rol_to_month.keys())
for oecd_country in oecd_countries:
  if oecd_country in oecd_exceptions:
    continue
  cpi_indices = cpi_dict[oecd_country].keys()
  er_indices = er_dict[oecd_country].keys()
  common_idx = set(cpi_indices) & set(er_indices)
  # print(len(common_idx), len(cpi_indices), len(er_indices))
  common_rol = common_rol & common_idx
  common_rol_l = list(common_idx)
  common_rol_l.sort()
  # print(oecd_country, rol_to_month[common_rol_l[0]], rol_to_month[common_rol_l[-1]])
common_rol_list = list(common_rol)
common_rol_list.sort()
common_mon = [rol_to_month[x] for x in common_rol_list]

# print(common_mon[0], common_mon[-1])
oecd_row_start = common_rol_list[0]
oecd_row_end = common_rol_list[-1]
print(rol_to_month[oecd_row_start], rol_to_month[oecd_row_end])

for oecd_country in oecd_countries:
  if oecd_country == "United States":
    continue
  if oecd_country in oecd_exceptions:
    continue
  for i in range(oecd_row_start, oecd_row_end + 1):
    row = [rol_to_month[i]]
    row.append(parse_country_name(oecd_country))
    if i in cpi_dict[oecd_country]:
      row.append(cpi_dict[oecd_country][i])
    else:
      row.append("")


    if i in cpi_dict["United States"]:
      row.append(cpi_dict["United States"][i])
    else:
      row.append("")

    if i in er_dict[oecd_country]:
      row.append(er_dict[oecd_country][i])
    else:
      row.append("")

    panal_writer.writerow(row)

