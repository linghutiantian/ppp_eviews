import csv
import re

countries_original = list(csv.reader(open("unit_root_countries.csv")))

def parse_country_name(name):
  name = re.sub('[^0-9a-zA-Z]+', '_', name)
  return name.upper()


def gen_uroot(country, out, name, path):
  line = "freeze(FRZ_" + name + country + ") " + name + country + ".uroot(lag=1)\r\n"
  out.write(line)
  line = "FRZ_" + name + country + ".save(t=csv) \\\\192.168.0.67\\nas\\workspace\\ppp\\" + path + "\\" + country + "_ADF.csv\r\n"
  out.write(line)
  line = "FRZ_" + name + country + ".save(t=pdf) \\\\192.168.0.67\\nas\\workspace\\ppp\\" + path + "\\" + country + "_ADF.pdf\r\n"
  out.write(line)

def gen_per_country(country, out):
  line = "genr ST_" + country + " = log(" + country + "_ER)\r\n"
  out.write(line)
  line = "genr PDIFF_" + country + " = log(" + country + "_CPI) - PT_UNITED_STATES\r\n"
  out.write(line)
  line = "equation EQ_" + country + ".ls ST_" + country + " c PDIFF_" + country + "\r\n"
  out.write(line)
  line = "EQ_" + country + ".makeresids RES_" + country + "\r\n"
  out.write(line)
  gen_uroot(country, out, "ST_", "stt_result")
  gen_uroot(country, out, "PDIFF_", "pdf_result")
  gen_uroot(country, out, "RES_", "res_result")




exception = ["anguilla", "aruba", "bahamas_the", "djibouti", "ecuador", "el_salvador", "panama", "sint_maarten", "timor_leste_dem_rep_of"]


countries = [parse_country_name(x) for x in countries_original[0]]
print(countries, len(countries))


out = open("coi_script.txt", "w")

line = "genr PT_UNITED_STATES = log(UNITED_STATES_CPI)\r\n"
out.write(line)

for country in countries:
  if country == "UNITED_STATES":
    continue
  if country.lower() in exception:
    continue
  gen_per_country(country, out)

out.close()
