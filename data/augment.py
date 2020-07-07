import json

def update(planet):
    with open('data/new.csv', 'r') as f:
        for line in f.readlines():
            parts = line.split(',')
            print(line)
            name = parts[0]
            inclination = parts[5]
            longitudeOfAscendingNode = parts[6]
            argumentOfPeriapsis = parts[3]

            moons = [m for m in planet['moons'] if m['name'].replace(' ','') == name.replace(' ','')]
            if len(moons) == 0:
                print('######### missing from json', line)
            elif len(moons) > 1:
                print('######### multiple matches')
            else:
                m = moons[0]
                m['inclination'] = float(inclination)
                m['longitudeOfAscendingNode'] = float(longitudeOfAscendingNode)
                m['argumentOfPeriapsis'] = float(argumentOfPeriapsis)


with open('data/moon-data.json', 'r') as f:
    data = json.load(f)

for planet in data:
    if planet['planet'] == 'Jupiter':
        update(planet)

with open('data/moon-data.json', 'w') as f:
    f.write(json.dumps(data, indent=4))
