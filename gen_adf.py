import csv
import re

countries_original = list(csv.reader(open("unit_root_countries.csv")))

def parse_country_name(name):
  name = re.sub('[^0-9a-zA-Z]+', '_', name)
  return name.upper()


def gen_per_country(country, out):
  line = "genr ST_" + country + " = log(" + country + "_ER)\r\n"
  out.write(line)
  line = "genr PT_" + country + " = log(" + country + "_CPI)\r\n"
  out.write(line)
  line = "genr QT_" + country + " = ST_" + country + " - PT_" + country + " + PT_UNITED_STATES\r\n"
  out.write(line)
  line = "freeze(FRZ_" + country + ") QT_" + country + ".uroot(lag=1)\r\n"
  out.write(line)
  line = "FRZ_" + country + ".save(t=csv) \\\\192.168.0.67\\nas\\workspace\\ppp\\adf_result\\" + country + "_ADF.csv\r\n"
  # line = "FRZ_" + country + ".save(t=csv) \\\\Mac\\Home\\Desktop\\shazirangwojiandewenjianjia\\" + country + "_ADF.csv\r\n"
  out.write(line)
  line = "FRZ_" + country + ".save(t=pdf) \\\\192.168.0.67\\nas\\workspace\\ppp\\adf_result\\" + country + "_ADF.pdf\r\n"
  # line = "FRZ_" + country + ".save(t=pdf) \\\\Mac\\Home\\Desktop\\shazirangwojiandewenjianjia\\" + country + "_ADF.pdf\r\n"
  out.write(line)

countries = [parse_country_name(x) for x in countries_original[0]]
print(countries, len(countries))


out = open("eviews_script.txt", "w")

line = "genr PT_UNITED_STATES = log(UNITED_STATES_CPI)\r\n"
out.write(line)

for country in countries:
  if country == "UNITED_STATES":
    continue
  gen_per_country(country, out)

out.close()
