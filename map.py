import json

with open('data/Microsoft.json', 'r', encoding='utf8') as f:
    a = json.load(f)

# print(a)
tmpMap = {}
for crs in a['crsList']:
    tmpMap[crs['key']]=crs['props']['crs_id']

print(tmpMap)

a['map']=tmpMap

with open('data/Microsoft_.json', 'w', encoding='utf8') as f:
    json.dump(a,f)



# from copy import copy

# with open('data/SKKU.json', 'r', encoding='utf8') as f:
#     a = json.load(f)

# tmpCps = copy(a['cps'])
# tmpMap = {}
# for crs in a['crsList']:
#     if crs['key']:
#         tmpMap[crs['key']]=crs['props']['crs_id']
#         # print(tmpCps.pop(int(crs['key'])))

# for crs in a['crsList']:
#     if not crs['key']:
#         for i in range(len(tmpCps)):
#             if str(i) not in tmpMap:
#                 tmpMap[str(i)]=crs['props']['crs_id']
#                 crs['key']=str(i)
#                 crs['props']['keyFromParent']=i
#                 crs['props']['cp']=tmpCps[i]
#                 break
# print(tmpMap)


# a['map']=tmpMap

# with open('data/SKKU_.json', 'w', encoding='utf8') as f:
#     json.dump(a,f)
