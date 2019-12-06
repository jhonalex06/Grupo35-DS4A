import json

with open('/home/shade/person.json') as f:
    geojson = json.loads(f.read())

print (geojson.keys)