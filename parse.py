import csv
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook


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
row_to_month = {}
month_to_row = {}

for idx, row in enumerate(exchange_rates):
  if idx == 0:
    continue
  for col, val in enumerate(row):
    row_to_month[idx] = row[0]
    month_to_row[row[0]] = idx
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
  if len(er_idx & cpi_idx) < 12:
    print("no intersection:", country)
  else:
    filter_country_final.append(country)

country_out = open('unit_root_countries.csv', 'wb')
country_writer = csv.writer(country_out)
for country in filter_country_final:
  country_writer.writerow([country])


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


row_start = month_to_row["1960M01"]
row_end = month_to_row["2018M12"]

bad_country = []
for i in range(row_start, row_end + 1):
  row = [row_to_month[i]]
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

common_row = set(row_to_month.keys())
for oecd_country in oecd_countries:
  if oecd_country in oecd_exceptions:
    continue
  cpi_indices = cpi_dict[oecd_country].keys()
  er_indices = er_dict[oecd_country].keys()
  common_idx = set(cpi_indices) & set(er_indices)
  # print(len(common_idx), len(cpi_indices), len(er_indices))
  common_row = common_row & common_idx
  common_row_l = list(common_idx)
  common_row_l.sort()
  # print(oecd_country, row_to_month[common_row_l[0]], row_to_month[common_row_l[-1]])
common_row_list = list(common_row)
common_row_list.sort()
common_mon = [row_to_month[x] for x in common_row_list]

# print(common_mon[0], common_mon[-1])
oecd_row_start = common_row_list[0]
oecd_row_end = common_row_list[-1]
print(row_to_month[oecd_row_start], row_to_month[oecd_row_end])

for oecd_country in oecd_countries:
  if oecd_country == "United States":
    continue
  if oecd_country in oecd_exceptions:
    continue
  for i in range(oecd_row_start, oecd_row_end + 1):
    row = [row_to_month[i]]
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


# generate oecd real exchange rate
rer_dict = {}

for oecd_country in oecd_countries:
  if oecd_country == "United States":
    continue
  if oecd_country in oecd_exceptions:
    continue
  rer_dict[oecd_country] = {}
  for i in range(oecd_row_start, oecd_row_end + 1):
    er = er_dict[oecd_country][i].replace(",", "")
    pt = cpi_dict[oecd_country][i].replace(",", "")
    pt_star = cpi_dict["United States"][i].replace(",", "")
    rer_dict[oecd_country][i] = float(er) / float(pt) * float(pt_star)
  rate = float(100) / rer_dict[oecd_country][oecd_row_end];
  for i in range(oecd_row_start, oecd_row_end + 1):
    rer_dict[oecd_country][i] *= rate


rer_all_out = open('./rer/all_countries.csv', 'wb')
rer_all_writer = csv.writer(rer_all_out)
rer_all_row_0 = ["DATE"]
for country in oecd_countries:
  if country == "United States":
    continue
  if country in oecd_exceptions:
    continue
  rer_all_row_0.append(country)
rer_all_writer.writerow(rer_all_row_0)

for i in range(oecd_row_start, oecd_row_end + 1):
  line = [row_to_month[i]]
  for country in oecd_countries:
    if country == "United States":
      continue
    if country in oecd_exceptions:
      continue
    line.append(rer_dict[country][i])
  rer_all_writer.writerow(line)


for country in oecd_countries:
  if country == "United States":
    continue
  if country in oecd_exceptions:
    continue
  rer_out = open('./rer/per_country/' + parse_country_name(country) + '.csv', 'wb')
  rer_writer = csv.writer(rer_out)
  rer_row_0 = ["DATE", country]
  rer_writer.writerow(rer_row_0)
  for i in range(oecd_row_start, oecd_row_end + 1):
    line = [row_to_month[i], rer_dict[country][i]]
    rer_writer.writerow(line)
  rer_out.close()

row_start = month_to_row["1960M01"]
row_end = month_to_row["2018M12"]
data_count = {}
for row in row_to_month.keys():
  if row < row_start:
    continue
  if row > row_end:
    continue
  data_count[row] = 0
  for country in common_countries:
    has_er = er_dict.get(country) and er_dict[country].get(row) and er_dict[country][row] and er_dict[country][row] != "..."
    has_cpi = cpi_dict.get(country) and cpi_dict[country].get(row) and cpi_dict[country][row] and cpi_dict[country][row] != "..."
    if has_er and has_cpi:
      data_count[row] += 1

month_count_out = open('month_count.csv', 'wb')
month_count_writer = csv.writer(month_count_out)
for row in row_to_month.keys():
  if row < row_start:
    continue
  if row > row_end:
    continue
  line = [row_to_month[row], data_count[row]]
  month_count_writer.writerow(line)
month_count_out.close()

# plot real exchange rate
rer_countries_ = list(csv.reader(open("trade_countries.csv")))
rer_countries = [ y for x in rer_countries_ for y in x]
rer_countries.sort()

def analyze_rer(country):
  er_month = er_dict[country].keys()
  cpi_month = cpi_dict[country].keys()
  common_month = list(set(er_month) & set(cpi_month))
  rer_out = open('./rer/trade_country/' + parse_country_name(country) + '.csv', 'wb')
  rer_writer = csv.writer(rer_out)
  line = ["Date", "Date", "Nominal Exchange Rate", "Real Exchange Rate"]
  rer_writer.writerow(line)
  month_0 = common_month[0]
  ratio = float(cpi_dict[country][month_0].replace(',', '')) / float(cpi_dict["United States"][month_0].replace(',', ''))
  for month in common_month:
    line = [row_to_month[month], '', er_dict[country][month], float(er_dict[country][month].replace(',', '')) / float(cpi_dict[country][month].replace(',', '')) * float(cpi_dict["United States"][month].replace(',', ''))  * ratio]
    rer_writer.writerow(line)
  rer_out.close()

for country in rer_countries:
  analyze_rer(country)
