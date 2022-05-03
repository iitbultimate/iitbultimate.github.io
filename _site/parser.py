import numpy as np

header = r'''---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

# Leader board

|S.No | Name | Experience | Practice | Game | Trials | Total |
|-|-|-|-|-|-|-|
'''

data = []

def read_index():
  filename = "index.markdown"
  fp = open(filename, 'r')
  lines = fp.readlines()
  
  i = 0
  while (lines[i].strip() != '# Leader board'):
      i = i+1

  read_data(lines, i+4)

def read_data(lines, index):
  for i in range(index, len(lines)):
    print(lines[i])



read_index()
