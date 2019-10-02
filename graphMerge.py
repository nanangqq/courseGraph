import json
import os
import pandas as pd
from pprint import pprint 

datapath = './src/data/'
uList = os.listdir(datapath)
rawGraph = {}
for u in uList:
    with open(datapath+u,'r',encoding='utf8') as f:
        rawGraph[u.split('.')[0]]=json.load(f)

def printCourses(univFileName, uList=uList):
    cnt=0
    for u in uList:
        if u==univFileName:
            for crs in rawGraph[u.split('.')[0]]['crsList']:
                print((1,crs['props']['name']))
                # print(crs['props']['description'])
                # print(crs['props']['prerequisites'])
                cnt+=1
    print(cnt)

# printCourses('MIT.json')

with open('./src/merge/graphMerge.csv', 'r') as f:
    mergeMap = pd.read_csv(f)

# print(mergeMap)
# print(len(mergeMap))

crsList=[]
crsDict={}
cnt = 1
for row in mergeMap.itertuples():
    # print(type(row))
    if type(row[1]) is str:
        tmp = {'crs_id':'test'+str(cnt)}

        tmp['name'] = row[1]
        tmp['source'] = {'CMU':[],'Berkely':[]}
        if type(row[2]) is str:
            tmp['source']['CMU'].append(eval(row[2]))
        if type(row[3]) is str:
            tmp['source']['Berkely'].append(eval(row[3]))
        crsList.append(tmp)
        crsDict[tmp['crs_id']] = tmp
        cnt+=1
    else:
        if type(row[2]) is str:
            tmp['source']['CMU'].append(eval(row[2]))
        if type(row[3]) is str:
            tmp['source']['Berkely'].append(eval(row[3]))
# pprint(crsList)
# pprint(crsDict)

inverseMap = {'CMU':{}, 'Berkely':{}}
ordMap = {'CMU':{}, 'Berkely':{}}
for crs in crsList:
    for univ in crs['source']:
        for src in crs['source'][univ]:
            # print(src[0],src[1])
            inverseMap[univ][src[1]]=crs['crs_id']
        
        for u in rawGraph:
            if u==univ:
                for c in rawGraph[u]['crsList']:
                    ordMap[u][c['props']['crs_id']] = c['props']['name']
# pprint(inverseMap)
# pprint(ordMap)

# for crs in rawGraph['CMU']['crsList']:

#     print(crs['props']['name']) # prq뽑을 강좌 이름
#     print(crsDict[inverseMap['CMU'][crs['props']['name']]]) 

#     tmp = {}
#     for prq in crs['props']['prerequisites']:
#         if prq in ordMap['CMU']:
#             print(ordMap['CMU'][prq]) # 선수과목 원래 이름
#             print(inverseMap['CMU'][ordMap['CMU'][prq]]) # 선수과목 합성 코드
#             if inverseMap['CMU'][ordMap['CMU'][prq]] not in tmp:
#                 for src in crsDict[inverseMap['CMU'][crs['props']['name']]]['source']['CMU']:
#                     print(src)
#                     print(ordMap['CMU'][prq])
#                     if src[1]==crs['props']['name']:
#                         tmp[inverseMap['CMU'][ordMap['CMU'][prq]]] = src[0]
#             else:
#                 for src in crsDict[inverseMap['CMU'][crs['props']['name']]]['source']['CMU']:
#                     if src[1]==crs['props']['name']:
#                         tmp[inverseMap['CMU'][ordMap['CMU'][prq]]] += src[0]
#     crsDict[inverseMap['CMU'][crs['props']['name']]]['prerequisites'] = tmp

def mergePrq(univ, rawGraph=rawGraph, crsDict=crsDict, inverseMap=inverseMap, ordMap=ordMap):
    # print(univ)
    for crs in rawGraph[univ]['crsList']:
        crsTo = crs['props']['name'] # prq뽑을 강좌 이름

        if crsTo in inverseMap[univ]: 
            crsToObj = crsDict[inverseMap[univ][crsTo]] # inverseMap으로 기존 강좌 이름에 대한 합성 코드 뽑아서 crsDict 조회
            crsToPrqList = crs['props']['prerequisites']
            # print(crsToObj)

            if 'prerequisites' in crsToObj:
                tmp = crsToObj['prerequisites']
            else:
                tmp = {}
            for prq in crsToPrqList:
                if prq in ordMap[univ]:
                    prqCrsName = ordMap[univ][prq] # 선수과목 원래 이름
                    
                    if prqCrsName in inverseMap[univ]:
                        prqMergedId = inverseMap[univ][ordMap[univ][prq]] # 선수과목 합성 코드
                        # print(prqCrsName)
                        # print(prqMergedId)

                        for src in crsToObj['source'][univ]:
                            # print(src)
                            if src[1]==crsTo:
                                if prqMergedId not in tmp:
                                    tmp[prqMergedId] = src[0]
                                else:
                                    tmp[prqMergedId] += src[0]
                                # print(tmp)
                                # if prqCrsName not in tmp:
                                #     tmp[prqCrsName] = src[0]
                                # else:
                                #     tmp[prqCrsName] += src[0]
                                # print(tmp)

            crsToObj['prerequisites'] = tmp

mergePrq('Berkely')
mergePrq('CMU')

# pprint(crsDict)
# pprint(inverseMap)

output={
    "crsList":[],
    "merged":True,
    "view_size":[3900,2700],
    "cps":[[150,90],[450,90],[750,90],[1050,90],[1350,90],[1650,90],[1950,90],[2250,90],[2550,90],[2850,90],[3150,90],[3450,90],[3750,90],[150,270],[450,270],[750,270],[1050,270],[1350,270],[1650,270],[1950,270],[2250,270],[2550,270],[2850,270],[3150,270],[3450,270],[3750,270],[150,450],[450,450],[750,450],[1050,450],[1350,450],[1650,450],[1950,450],[2250,450],[2550,450],[2850,450],[3150,450],[3450,450],[3750,450],[150,630],[450,630],[750,630],[1050,630],[1350,630],[1650,630],[1950,630],[2250,630],[2550,630],[2850,630],[3150,630],[3450,630],[3750,630],[150,810],[450,810],[750,810],[1050,810],[1350,810],[1650,810],[1950,810],[2250,810],[2550,810],[2850,810],[3150,810],[3450,810],[3750,810],[150,990],[450,990],[750,990],[1050,990],[1350,990],[1650,990],[1950,990],[2250,990],[2550,990],[2850,990],[3150,990],[3450,990],[3750,990],[150,1170],[450,1170],[750,1170],[1050,1170],[1350,1170],[1650,1170],[1950,1170],[2250,1170],[2550,1170],[2850,1170],[3150,1170],[3450,1170],[3750,1170],[150,1350],[450,1350],[750,1350],[1050,1350],[1350,1350],[1650,1350],[1950,1350],[2250,1350],[2550,1350],[2850,1350],[3150,1350],[3450,1350],[3750,1350],[150,1530],[450,1530],[750,1530],[1050,1530],[1350,1530],[1650,1530],[1950,1530],[2250,1530],[2550,1530],[2850,1530],[3150,1530],[3450,1530],[3750,1530],[150,1710],[450,1710],[750,1710],[1050,1710],[1350,1710],[1650,1710],[1950,1710],[2250,1710],[2550,1710],[2850,1710],[3150,1710],[3450,1710],[3750,1710],[150,1890],[450,1890],[750,1890],[1050,1890],[1350,1890],[1650,1890],[1950,1890],[2250,1890],[2550,1890],[2850,1890],[3150,1890],[3450,1890],[3750,1890],[150,2070],[450,2070],[750,2070],[1050,2070],[1350,2070],[1650,2070],[1950,2070],[2250,2070],[2550,2070],[2850,2070],[3150,2070],[3450,2070],[3750,2070],[150,2250],[450,2250],[750,2250],[1050,2250],[1350,2250],[1650,2250],[1950,2250],[2250,2250],[2550,2250],[2850,2250],[3150,2250],[3450,2250],[3750,2250],[150,2430],[450,2430],[750,2430],[1050,2430],[1350,2430],[1650,2430],[1950,2430],[2250,2430],[2550,2430],[2850,2430],[3150,2430],[3450,2430],[3750,2430],[150,2610],[450,2610],[750,2610],[1050,2610],[1350,2610],[1650,2610],[1950,2610],[2250,2610],[2550,2610],[2850,2610],[3150,2610],[3450,2610],[3750,2610]]
    }

# pprint(crsList)
pprint(inverseMap)
pprint(ordMap)

cmuOriginMap = {"0":"11492","4":"15128","5":"99101","6":"16161","13":"85421","14":"11411","18":"15151","22":"15213","26":"11442","27":"11441","35":"21241","37":"15463","45":"15122","50":"16385","52":"16467","53":"05391","67":"15150","77":"15386","78":"16350","79":"15494","85":"15259","86":"15750","87":"15281","89":"21122","90":"15387","92":"16362","93":"15210","94":"15251","96":"07180","97":"10315","99":"36218","103":"85370","112":"15482","113":"36401","114":"16384","115":"21120","121":"85213","126":"36402","131":"85211","134":"85390","135":"10745","136":"10715","139":"10718","152":"10418","154":"80249","157":"85408","158":"85412","159":"10605","160":"10708","161":"10707","165":"10703","167":"15853","170":"76101","172":"15826","174":"36705","175":"10716","176":"10403","177":"15780","178":"10417","179":"11485","186":"36710","187":"36709","188":"36700","189":"05317","190":"36707","191":"10725","192":"17200"}
cmuKeyNameMap = {}
for crs in rawGraph['CMU']['crsList']:
    cmuKeyNameMap[crs['props']['name']]=crs['key']

pprint(cmuKeyNameMap)
keyMap={}
for crs in crsList:
    tmp={}
    if crs['name'] in inverseMap['CMU']:
        # print(crs['name'], cmuKeyNameMap[crs['name']])
        tmp['key']=cmuKeyNameMap[crs['name']]
        crs['cp']=output['cps'][int(cmuKeyNameMap[crs['name']])]
        tmp['props']=crs
        keyMap[cmuKeyNameMap[crs['name']]]=crs['crs_id']
    else:
        # print(crs['name'])
        for i in range(len(output['cps'])):
            key=str(i)
            if key not in cmuOriginMap:
                tmp['key']=key
                crs['cp']=output['cps'][i]
                tmp['props']=crs
                keyMap[key]=crs['crs_id']
                cmuOriginMap[key]=crs['crs_id']
                break
    output['crsList'].append(tmp)
output['map']=keyMap
pprint(output)

with open(datapath+'merged.json', 'w', encoding='utf8') as f:
    json.dump(output, f)