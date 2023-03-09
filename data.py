import json
import csv
import urllib.request

def dic_list_gen(LoS, LoL):
  acc = []
  length = len(LoS)
  for string in LoL:
    acc1 = {}
    for item in range(length):
      acc1.update({LoS[item]: string[item]})
    acc.append(acc1)  
  return acc

def read_values(filename):
  acc = []
  with open(filename) as f:
    reader = csv.reader(f)
    next(reader)
    for line in reader:
      acc.append(line)
  return acc

def make_lists(LoS, LoD):
  acc = []
  for d in LoD:
    acc1 = []
    acc2 = dict()
    acc3 = list((i, d.get(i)) for i in LoS)
    for i in acc3:
      acc2.setdefault(i[0], i[1])
    for key, value in acc2.items():
      if key in LoS:
        acc1.append(value)
    acc.append(acc1)
  return acc

def write_values(filename, LoL):
  with open(filename, "a") as f:
    writer = csv.writer(f)
    for lists in LoL:
      writer.writerow(lists)

def json_loader(url):
  response = urllib.request.urlopen(url)
  content = response.read().decode()
  ans = json.loads(content)
  return ans

def make_values_numeric(LoS, aDict):
  for string in LoS:
    if string in aDict.keys():
      aDict[string] = float(aDict.get(string))
  return aDict

def save_data(LoS, LoD, filename):
  with open(filename, "w") as f:
    writer = csv.writer(f)
    writer.writerow(LoS)
    for dic in LoD:
      acc = []
      for key in LoS:
        if key in dic:
          acc.append(dic[key])
      writer.writerow(acc)

def load_data(filename):
  acc = []
  with open(filename) as f:
    reader = csv.reader(f)
    headerLine= next(reader)
    print(headerLine)
    for line in reader:
      acc1 = {}
      for num in range(len(headerLine)):
        acc1[headerLine[num]] = line[num]
      acc.append(acc1)
  return acc