def create_effectiveness_dict()->dict[str, dict[str, float]]:
    effectiveness = {}
    with open('data\\effectiveness_chart.csv') as file:
        defenders = file.readline().strip('\n').split(',')
        defenders.pop(0)
        line = file.readline()
        while line != '':
            line = line.strip('\n').split(',')
            attacker = line.pop(0)
            for n in range(len(line)): line[n] = float(line[n])
            effectiveness[attacker] = {defender:dmg for defender, dmg in zip(defenders,line)}
            line = file.readline()
    return effectiveness