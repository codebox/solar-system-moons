import json

with open('data/moon-data.json', 'r') as f:
    data = json.load(f)

for planet in data:
    planet['moons'].sort(key=lambda p: p['orbit'])

with open('data/moon-data.json', 'w') as f:
    f.write(json.dumps(data, indent=4))
