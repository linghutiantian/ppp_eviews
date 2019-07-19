import csv
with open('all_exchange_rates.csv', 'rb') as f,  open('exchange_rate.csv', 'wb') as out:
    reader = csv.reader(f)
    writer = csv.writer(out)
    i = 0
    for row in reader:
        if 'M' in row[0] or i == 0:
            writer.writerow(row)
        i = i + 1
