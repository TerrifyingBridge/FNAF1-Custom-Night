import NightSim
import matplotlib.pyplot as plt
import numpy as np

def mo_to_secs(mo, ani):
    if (ani == "b"):
        total_time = mo * 4.97
        if (total_time <= 90):
            return total_time / 90
        else:
            total_time -= 90
            return 1 + (total_time / 89)
    elif (ani == "c"):
        total_time = mo * 4.98
        if (total_time <= 90):
            return total_time / 90
        else:
            total_time -= 90
            return 1 + (total_time / 89)
    return None

total_sim = 1000000
bonnie_ai = 20
chica_ai = 20

MO = [i for i in range(1, 108)]
bonnie_mo = []
chica_mo = []
for i in range(1, 108):
    bonnie_mo.append(round(mo_to_secs(i, "b"), 2))
    chica_mo.append(round(mo_to_secs(i, "c"), 2))

bonnie_data = [0 for i in range(1, 108)]
bonnie_first_visits = [0 for i in range(1, 108)]
chica_data = [0 for i in range(1, 108)]
chica_first_visits = [0 for i in range(1, 108)]

for _ in range(total_sim):
    x = NightSim.NightSim(bonnie_ai, chica_ai)
    visits = x.simulate()

    for time in visits[0]:
        bonnie_data[time - 1] += 1
    for time in visits[1]:
        chica_data[time - 1] += 1

    if (len(visits[0]) > 0):
        bonnie_first_visits[visits[0][0] - 1] += 1
    if (len(visits[1]) > 0):
        chica_first_visits[visits[1][0] - 1] += 1

'''
for i in range(len(bonnie_first_visits)):
    bonnie_first_visits[i] /= total_sim
    chica_first_visits[i] /= total_sim


plt.figure(figsize=(10,6))
plt.figtext(0.131, 0.85, "# of Sims: " + str(total_sim), size=14)
plt.figtext(0.13,0.8, "Chica's AI: " + str(chica_ai), size=14)
plt.xlabel("Night Hour (0 = 12AM)", size=16)
plt.ylabel("Relative Frequency", size=16)
plt.ylim(0, max(chica_first_visits)*1.15)
plt.title("Chica's First Visit Distribution", size=20)
plt.bar(chica_mo, chica_first_visits, width=0.04)

plt.figtext(0.144, 0.85, "# of Sims: " + str(total_sim), size=14)
plt.figtext(0.13,0.8, "Bonnie's AI: " + str(bonnie_ai), size=14)
plt.xlabel("Night Hour (0 = 12AM)", size=16)
plt.ylabel("Relative Frequency", size=16)
plt.ylim(0, max(bonnie_first_visits)*1.15)
plt.title("Bonnie's First Visit Distribution", size=20)
plt.bar(bonnie_mo, bonnie_first_visits, width=0.04)
'''
################################
### VISIT DISTRIBUTION CODE  ###
################################


for i in range(len(bonnie_data)):
    bonnie_data[i] /= total_sim
    chica_data[i] /= total_sim
'''
plt.figure(figsize=(10, 6))
plt.figtext(0.144, 0.85, "# of Sims: " + str(total_sim), size=14)
plt.figtext(0.13,0.8, "Bonnie's AI: " + str(bonnie_ai), size=14)
plt.xlabel("Night Hour (0 = 12AM)", size=16)
plt.ylabel("Relative Frequency", size=16)
plt.ylim(0, max(bonnie_data)*1.15)
plt.title("Bonnie's MOs Spent At Door", size=20)
plt.bar(bonnie_mo, bonnie_data, width=0.04)

'''

plt.figure(figsize=(10, 6))
plt.figtext(0.131, 0.85, "# of Sims: " + str(total_sim), size=14)
plt.figtext(0.13,0.8, "Chica's AI: " + str(chica_ai), size=14)
plt.xlabel("Night Hour (0 = 12AM)", size=16)
plt.ylabel("Relative Frequency", size=16)
plt.ylim(0, max(chica_data)*1.15)
plt.title("Chica's MOs Spent At Door", size=20)
plt.bar(chica_mo, chica_data, width=0.04)

plt.show()