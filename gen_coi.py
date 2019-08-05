import csv
import re

countries_original = list(csv.reader(open("unit_root_countries.csv")))

def parse_country_name(name):
  name = re.sub('[^0-9a-zA-Z]+', '_', name)
  return name.upper()


def gen_uroot(country, out, name, prefix, extra = ""):
  frz_name = "FRZ_" + name + country
  if extra != "":
    frz_name = "FRZD_" + frz_name
  line = "freeze(" + frz_name + ") " + name + country + ".uroot(" + extra + "lag=1)\r\n"
  out.write(line)
  line = frz_name + ".save(t=csv) \\\\192.168.0.67\\nas\\workspace\\ppp\\coi_new\\" + prefix + "_" + country + "_ADF.csv\r\n"
  out.write(line)
  line = frz_name + ".save(t=pdf) \\\\192.168.0.67\\nas\\workspace\\ppp\\coi_new\\" + prefix + "_" + country + "_ADF.pdf\r\n"
  out.write(line)

def gen_per_country(country, out):
  line = "genr ST_" + country + " = log(" + country + "_ER)\r\n"
  out.write(line)
  line = "genr PT_" + country + " = log(" + country + "_CPI)\r\n"
  out.write(line)
# 3 var
  line = "equation EQ_" + country + ".ls ST_" + country + " c PT_" + country + " PT_UNITED_STATES\r\n"
  out.write(line)
  line = "EQ_" + country + ".makeresids RES_" + country + "\r\n"
  out.write(line)
# model 1
  line = "equation EQ_" + country + "_MD1.ls ST_" + country + " c (PT_" + country + " - PT_UNITED_STATES)\r\n"
  out.write(line)
  line = "EQ_" + country + "_MD1.makeresids RES_MD1_" + country + "\r\n"
  out.write(line)
# model 2
  line = "equation EQ_" + country + "_MD2.ls (ST_" + country + " - PT_" + country + ") c PT_UNITED_STATES\r\n"
  out.write(line)
  line = "EQ_" + country + "_MD2.makeresids RES_MD2_" + country + "\r\n"
  out.write(line)
# model 3
  line = "equation EQ_" + country + "_MD3.ls (ST_" + country + " +  PT_UNITED_STATES) c PT_" + country + "\r\n"
  out.write(line)
  line = "EQ_" + country + "_MD3.makeresids RES_MD3_" + country + "\r\n"
  out.write(line)
# end
  gen_uroot(country, out, "ST_", "stt_result")
  gen_uroot(country, out, "PT_", "ptt_result")
  gen_uroot(country, out, "ST_", "dst_result", "dif=1, ")
  gen_uroot(country, out, "PT_", "dpt_result", "dif=1, ")
  gen_uroot(country, out, "RES_", "res_result")
  gen_uroot(country, out, "RES_MD1_", "rm1_result")
  gen_uroot(country, out, "RES_MD2_", "rm2_result")
  gen_uroot(country, out, "RES_MD3_", "rm3_result")




exception = ["anguilla", "aruba", "bahamas_the", "djibouti", "ecuador", "el_salvador", "panama", "sint_maarten", "timor_leste_dem_rep_of"]


countries = [parse_country_name(x) for y in countries_original for x in y]
print(countries, len(countries))


out = open("coi_script_new.txt", "w")

line = "setmaxerrs 1000\r\n"
out.write(line)

line = "genr PT_UNITED_STATES = log(UNITED_STATES_CPI)\r\n"
out.write(line)
gen_uroot("UNITED_STATES", out, "PT_", "ptt_result")
gen_uroot("UNITED_STATES", out, "PT_", "dpt_result", "dif=1, ")

for country in countries:
  if country == "UNITED_STATES":
    continue
  if country.lower() in exception:
    continue
  gen_per_country(country, out)

out.close()
