import numpy as np
from datetime import datetime
import re
import json

header = r'''---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---
{% include_relative updates.markdown %}

# Leader board

|S.No | Name | Experience | Practice | Game | Trials | Total |
|-|-|-|-|-|-|-|
'''

data = {}

def read_index():
  global data
  fp = open('team.json', 'r')
  data = json.load(fp)
  data['Date'] = datetime.strptime(data['Date'], '%d-%m-%Y')
  fp.close()


def read_daily_data():
  filename = 'attendance.txt'
  fp = open(filename, 'r')
  lines = fp.readlines()
  fp.close()
  index = 0

  while index < len(lines):
    findsession = re.match("session:", lines[index])
    session_name = lines[index].split()[-1].split()[-1]
    if findsession:
      index += 1
      date = datetime.strptime(lines[index].strip(), '%d-%m-%Y')
      datelast = data['Date']
      if date > datelast:
        index += 1
        line = lines[index]
        names = []
        while (line.strip() != '*'):
          name = re.findall('[A-Z,a-z]+', line)[-1].title()
          names.append(name)
          index += 1
          if not (index < len(lines)):break
          line = lines[index]

        add_to_database(session_name, names)

    index += 1


def add_to_database(session_name, names):
  if len(names) == 0: return

  for name in names:
    for key in data.keys():
      if re.match(name, key.title()):
        if session_name == 'practice':
          print('Adding 2 points to ', key)
          data[key]['Practice'] += 2
        elif session_name == 'game':
          print('Adding 1 points to ', key)
          data[key]['Game'] += 1


def get_total_score():
  totals = []
  for name in data.keys():
    if name == 'Date': continue
    experience = int(data[name]['Experience'])
    practice = int(data[name]['Practice'])
    game = int(data[name]['Game'])
    trial = int(data[name]['Trial'])
    totals.append(experience + practice + game + trial)

  totals = np.array(totals)
  return totals


def write_new_data():
  global data
  towrite = ''
  totals = get_total_score()

  sortedid = reversed(np.argsort(totals))
  keys = data.keys()
  keys = [k for k in keys if not k == 'Date']
  sno = 1

  for id in sortedid:
    name = keys[id]
    experience = data[name]['Experience']
    practice = data[name]['Practice']
    game = data[name]['Game']
    trial = data[name]['Trial']
    towrite += '|%s | %s | %d | %d | %d | %d | %d |\n'%(sno,name.title(),experience,practice,game,trial,totals[id])
    sno += 1

  fp = open('index.markdown', 'w')
  date = datetime.strftime(datetime.today(), "%d-%m-%Y")
  data['Date'] = date
  fp.write(header)
  fp.write(towrite)
  fp.write("\n\nlast update %s"%date)
  fp.close()

  json.dump(data, open('team.json', 'w'), indent = 1)


if __name__ == '__main__':
  read_index()
  read_daily_data()
  write_new_data()