import json

with open('data/Postech.json', 'r', encoding='utf8') as f:
    a = json.load(f)

# print(a)
tmpMap = {}
for crs in a['crsList']:
    tmpMap[crs['key']]=crs['props']['crs_id']

print(tmpMap)

a['map']=tmpMap

with open('data/Postech_.json', 'w', encoding='utf8') as f:
    json.dump(a,f)
