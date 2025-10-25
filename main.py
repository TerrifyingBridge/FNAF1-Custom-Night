import NightSim

total_sim = 10000
first_op = []

for _ in range(total_sim):
    x = NightSim.NightSim(22, 20)
    temp = x.simulate()

    if (len(temp[0]) == 0):
        first_op.append(108)
    else:
        first_op.append(temp[0][0])

print(first_op)
print(sum(first_op) / len(first_op))