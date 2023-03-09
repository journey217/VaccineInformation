import bottle
import json
import data
import os.path
import csv

def load_data():
  csv_file = 'saved_data.csv'
  if not os.path.isfile(csv_file):
    url = 'https://data.cdc.gov/resource/unsk-b7fc.json?$limit=50000&$where=location!=%27US%27'
    info = data.json_loader(url)
    heads = ['date','location','administered_janssen','administered_moderna','administered_pfizer','administered_unk_manuf','series_complete_pop_pct']
    data.save_data(heads, info, 'saved_data.csv')

load_data()

def RecentDate(filename):
  acc = ""
  with open(filename) as f:
    reader = csv.reader(f)
    header = next(reader)
    MostRecent = next(reader)
    length = 1
    acc = MostRecent[0]
  return acc

def NPS(LoD):
  acc = []
  for dic in LoD:
    acc.append(dic['series_complete_pop_pct'])
  return acc

def percentList(filename):
  acc = []
  with open(filename) as f:
    reader = csv.reader(f)
    for line in reader:
      acc.append(line[6])
  return acc

def makeDict(filename):
  acc1 = []
  with open(filename) as f:
    reader = csv.reader(f)
    for line in reader:
      acc = {"date": 1, "location": 1,"administered_janssen": 1,"administered_moderna": 1,"administered_pfizer": 1,"administered_unk_manuf": 1,"series_complete_pop_pct": 1}
      acc['date'] = line[0]
      acc['location'] = line[1]
      acc['administered_janssen'] = line[2]
      acc['administered_moderna'] = line[3]
      acc['administered_pfizer'] = line[4]
      acc['administered_unk_manuf'] = line[5]
      acc['series_complete_pop_pct'] = line[6]
      acc1.append(acc)
  return acc1

def VaccineTotals(LoD):
  janssen = 0
  moderna = 0
  pfizer = 0
  unk_manuf = 0
  for dic in LoD:
    janssen = janssen + int(dic['administered_janssen'])
    moderna = moderna + int(dic['administered_moderna'])
    pfizer = pfizer + int(dic['administered_pfizer'])
    unk_manuf = unk_manuf + int(dic['administered_unk_manuf'])
  total = [janssen, moderna, pfizer, unk_manuf]
  return total

def SortDic(Dic):
  return Dic['date']

import processing

MostRecentDate = RecentDate('saved_data.csv')
DictList = makeDict("saved_data.csv")
#PercenList = data.percentList("saved_data.csv")
CopyMatchList = processing.copy_matching(DictList, "date", MostRecentDate)
StatesList = list(processing.init_dictionary(CopyMatchList, 'location').keys())
PercenList = NPS(CopyMatchList)
BarDict = dict(zip(StatesList, PercenList))
VacNames = ['Janssen', 'Moderna', 'Pfizer', 'Unknown']
VacTot = VaccineTotals(CopyMatchList)
PieDict = dict(zip(VacTot, VacNames))

#print(VaccineTotals(CopyMatchList))
#print(data.makeDict("saved_data.csv"))
#print(processing.max_value(DictList, "date"))
#print(data.percentList("saved_data.csv"))
#print(processing.init_dictionary(DictList, 'location'))
#print(processing.copy_matching(DictList, "date", "2021-11-29T00:00:00.000"))
#print((StatesList))
#print((PercenList))
#print(data.NPS(CopyMatchList))
#print(data.RecentDate('saved_data.csv'))
#print(dict(zip(StatesList, PercenList)))
#print(CopyMatchList)
#print(PieDict)
#print(DictList)

@bottle.route("/")
def index():
  return bottle.static_file("server.html", root=".")

@bottle.route("/script.js")
def index2():
  return bottle.static_file("script.js", root=".")

@bottle.route("/bar")
def barData():
  barBlob = json.dumps(BarDict)
  return barBlob

@bottle.route("/pie")
def pieData():
  pieBlob = json.dumps(PieDict)
  return pieBlob

@bottle.post("/line")
def Loc():
  LocContent = bottle.request.body.read().decode()
  LocContent = json.loads(LocContent)
  LocList = processing.copy_matching(DictList, 'location', LocContent)
  LocList.sort(key= SortDic)
  NewLocList = processing.init_dictionary(LocList, 'date')
  return json.dumps(NewLocList)


bottle.run(host="0.0.0.0", port=8080, debug = True)