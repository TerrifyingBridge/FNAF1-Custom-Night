import NightSim
import matplotlib.pyplot as plt
import numpy as np

total_sim = 1000000
bonnie_data = []
bonnie_first_visits = []
chica_data = []
chica_first_visits = []
bonnie_ai = 1
chica_ai = 0

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

for _ in range(total_sim):
    x = NightSim.NightSim(bonnie_ai, chica_ai)
    visits = x.simulate()
    '''
    for time in visits[0]:
        bonnie_data.append(time)
    for time in visits[1]:
        chica_data.append(time)
    '''
    if (len(visits[0]) > 0):
        bonnie_first_visits.append(visits[0][0])
    if (len(visits[1]) > 0):
        chica_first_visits.append(visits[1][0])


MO = np.arange(1, 108, 1)
bonnie_first_dist = np.zeros(len(MO))
for i in range(len(bonnie_first_visits)):
    bonnie_first_dist[bonnie_first_visits[i] - 1] += 1
plt.bar(MO, bonnie_first_dist)


################################
### VISIT DISTRIBUTION CODE  ###
################################

'''
bonnie_clean_data = np.zeros(len(my_bars))
for time in bonnie_data:
    bonnie_clean_data[time - 1] += 1
bonnie_clean_data = bonnie_clean_data / total_sim

plt.figure(figsize=(10, 6))
plt.figtext(0.144, 0.85, "# of Sims: " + str(total_sim), size=14)
plt.figtext(0.13,0.8, "Bonnie's AI: " + str(bonnie_ai), size=14)
plt.xlabel("Bonnie's MO", size=16)
plt.ylabel("Relative Frequency", size=16)
plt.ylim(0, max(bonnie_clean_data)*1.15)
plt.title("Bonnie's MOs Spent At Door", size=20)
plt.bar(my_bars, bonnie_clean_data)
plt.show()


my_bars = np.arange(1, 108, 1)
print(my_bars)

chica_clean_data = np.zeros(len(my_bars))
for time in chica_data:
    chica_clean_data[time - 1] += 1

chica_clean_data = chica_clean_data / total_sim

plt.figure(figsize=(10, 6))
plt.figtext(0.144, 0.85, "# of Sims: " + str(total_sim), size=14)
plt.figtext(0.13,0.8, "Chica's AI: " + str(chica_ai), size=14)
plt.xlabel("Chica's MO", size=16)
plt.ylabel("Relative Frequency", size=16)
plt.ylim(0, max(chica_clean_data)*1.15)
plt.title("Chica's MOs Spent At Door", size=20)
plt.bar(my_bars, chica_clean_data)
'''
plt.show()