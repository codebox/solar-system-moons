import json

def update(planet):
    with open('data/new.csv', 'r') as f:
        for line in f.readlines():
            print(line)
            name,_1,_2,_3,incl,ecc = line.split(',')

            moons = [m for m in planet['moons'] if m['name'].replace(' ','') == name.replace(' ','')]
            if len(moons) == 0:
                print('missing from json', line)
            elif len(moons) > 1:
                print('multiple matches')
            else:
                m = moons[0]
                m['inclination'] = incl
                m['eccentricity'] = ecc.strip()


with open('data/moon-data.json', 'r') as f:
    data = json.load(f)

for planet in data:
    if planet['planet'] == 'Neptune':
        update(planet)


with open('data/moon-data.json', 'w') as f:
    f.write(json.dumps(data, indent=4))
