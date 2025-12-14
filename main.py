import NightSim
import matplotlib.pyplot as plt
import numpy as np

def mo_to_hour(mo, ani):
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

total_sim = 100000
bonnie_ai = 0
chica_ai = 0
print(mo_to_hour(36, "b"))

MO = [i for i in range(1, 108)]
bonnie_mo = []
chica_mo = []
for i in range(1, 108):
    bonnie_mo.append(round(mo_to_hour(i, "b"), 2))
    chica_mo.append(round(mo_to_hour(i, "c"), 2))

bonnie_data = [0 for i in range(1, 108)]
bonnie_first_visits = [0 for i in range(1, 108)]

chica_data = [0 for i in range(1, 108)]
chica_first_visits = [0 for i in range(1, 108)]

bonnie_time_all_ai = dict(enumerate([[] for i in range(21)]))
chica_time_all_ai = dict(enumerate([[] for i in range(21)]))

for i in range(21):
    for _ in range(total_sim):
        x = NightSim.NightSim(i, i)
        visits = x.simulate()

        bonnie_time_all_ai[i].append(len(visits[0]))
        chica_time_all_ai[i].append(len(visits[1]))
'''
plt.figure(figsize=(10, 6))
plt.figtext(0.644, 0.85, "# of Sims: " + str(total_sim), size=14)
plt.xlabel("AI Value", size=16)
plt.ylabel("MOs Spent At Door", size=16)
plt.title("Chica's Time At Door For An AI Value", size=20)
plt.boxplot(chica_time_all_ai.values(), tick_labels=chica_time_all_ai.keys(), showmeans=True)
for key in chica_time_all_ai:
    print("Average Time Spent At Door For AI Of " + str(key) + ":", sum(chica_time_all_ai[key]) / len(chica_time_all_ai[key]))
    print("Medium Time Spent At Door For AI Of " + str(key) + ":", np.median(chica_time_all_ai[key]))

'''
plt.figure(figsize=(10, 6))
plt.figtext(0.644, 0.85, "# of Sims: " + str(total_sim), size=14)
plt.xlabel("AI Value", size=16)
plt.ylabel("MOs Spent At Door", size=16)
plt.title("Bonnie's Time At Door For An AI Value", size=20)
plt.boxplot(bonnie_time_all_ai.values(), tick_labels=bonnie_time_all_ai.keys(), showmeans=True)
for key in bonnie_time_all_ai:
    print("Average Time Spent At Door For AI Of " + str(key) + ":", sum(bonnie_time_all_ai[key]) / len(bonnie_time_all_ai[key]))
    print("Medium Time Spent At Door For AI Of " + str(key) + ":", np.median(bonnie_time_all_ai[key]))

##############################
### SINGLE NIGHT SIM CODE  ###
##############################

'''
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
######################################
### FIRST VISIT DISTRIBUTION CODE  ###
######################################
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

'''
for i in range(len(bonnie_data)):
    bonnie_data[i] /= total_sim
    chica_data[i] /= total_sim

plt.figure(figsize=(10, 6))
plt.figtext(0.144, 0.85, "# of Sims: " + str(total_sim), size=14)
plt.figtext(0.13,0.8, "Bonnie's AI: " + str(bonnie_ai), size=14)
plt.xlabel("Night Hour (0 = 12AM)", size=16)
plt.ylabel("Relative Frequency", size=16)
plt.ylim(0, max(bonnie_data)*1.15)
plt.title("Bonnie's MOs Spent At Door", size=20)
plt.bar(bonnie_mo, bonnie_data, width=0.04)

plt.figure(figsize=(10, 6))
plt.figtext(0.131, 0.85, "# of Sims: " + str(total_sim), size=14)
plt.figtext(0.13,0.8, "Chica's AI: " + str(chica_ai), size=14)
plt.xlabel("Night Hour (0 = 12AM)", size=16)
plt.ylabel("Relative Frequency", size=16)
plt.ylim(0, max(chica_data)*1.15)
plt.title("Chica's MOs Spent At Door", size=20)
plt.bar(chica_mo, chica_data, width=0.04)
'''

###############################
### TIME DISTRIBUTION CODE  ###
###############################
'''
bonnie_door_time = [i for i in range(max(bonnie_door_time_raw) + 1)]
bonnie_door_time_count = [0 for i in range(max(bonnie_door_time_raw) + 1)]

for time in bonnie_door_time_raw:
    bonnie_door_time_count[time] += 1

for i in range(len(bonnie_door_time_count)):
    bonnie_door_time_count[i] = bonnie_door_time_count[i] / total_sim

plt.figure(figsize=(10, 6))

plt.figtext(0.144, 0.85, "# of Sims: " + str(total_sim), size=14)
plt.figtext(0.13,0.8, "Bonnie's AI: " + str(bonnie_ai), size=14)
plt.xlabel("MOs Spent At Door", size=16)
plt.ylabel("Relative Frequency", size=16)
plt.ylim(-1, max(bonnie_door_time_raw)*1.15)
plt.title("Bonnie's Total MOs Spent At The Door", size=20)

plt.figtext(0.144, 0.85, "# of Sims: " + str(total_sim), size=14)
plt.figtext(0.13,0.8, "Bonnie's AI: " + str(bonnie_ai), size=14)
plt.xlabel("MOs Spent At Door", size=16)
plt.ylabel("AI Value", size=16)
plt.title("Bonnie's Total MOs Spent At The Door", size=20)
plt.boxplot(bonnie_door_time_raw, vert=False)
plt.bar(bonnie_door_time, bonnie_door_time_count, width=0.5)
'''

plt.show()