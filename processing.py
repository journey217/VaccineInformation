import data

#DictList = data.makeDict("saved_data.csv")

def max_value(LoD, aKey):
  acc = "" 
  if len(LoD) == 0:
    return acc
  x = max(LoD, key=lambda x:x[aKey])
  c = x.get(aKey)
  return acc + c

#max_value(DictList, "date")

#init_dictionary

def init_dictionary(listOfDicts,aKey):
  newDict = {}
  for dicta in listOfDicts:
    if aKey in dicta:
      v = dicta[aKey]
      newDict[v] = dicta["series_complete_pop_pct"]
      #newDict[v] = 0
  return newDict

#sum_matches

def sum_matches(LoD, aKey, aValue, aKey2):
  ac = 0
  for dict in LoD:
    a = dict.get(aKey)
    tgt = dict.get(aKey2)
    if a == aValue:
      ac = ac + tgt
  return ac

#copy_matching

def copy_matching(lod,k,v):
  newList = []
  for dicta in lod:
    if (k,v) in dicta.items():
      newList.append(dicta)
  return newList