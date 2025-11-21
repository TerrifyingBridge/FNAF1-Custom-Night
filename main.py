import csv

import NightSim

total_sim = 1000000
data = []

for _ in range(total_sim):
    x = NightSim.NightSim(6, 0)
    visits = x.simulate()

    temp_row = []

    for i in range(107):
        if (i + 1 in visits[0]):
            temp_row.append(1)
        else:
            temp_row.append(0)
    data.append(temp_row)

with open("csv_files/bonnie_visits_6.csv", "w", newline="") as csvfile:
    header = []
    for i in range(1, 108):
        header.append(i)

    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(data)