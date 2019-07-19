import csv
with open('all_cpi.csv', 'rb') as f,  open('all_cpi_no_ref.csv', 'wb') as out:
    reader = csv.reader(f)
    writer = csv.writer(out)
    i = 0
    for row in reader:
        if 'V' in row[1] or i == 0:
            new_row = [row[0]] + row[2:]
            writer.writerow(new_row)
        i = i + 1
