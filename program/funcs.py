def create_effectiveness_dict()->dict[str, dict[str, float]]:
    efectiveness = {}
    with open('data\\effectiveness_chart.csv') as file:
        defenders = file.readline().strip('\n').split(',').pop(0)
        while file.read
            if file.tell() == 0: continue
            else: 
                line_splitted = line.strip('\n').split(',')
