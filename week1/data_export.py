#!/usr/bin/env python

import json
import yaml

my_list = ["whatever","whenever"]
my_list.append({})

my_list[-1]['I like to eat'] = ["apples","bananas"]
my_list[-1]['I like to oat'] = ["opples","bononos"]

with open("objects.yml","w") as f:
  f.write(yaml.dump(my_list,default_flow_style=False))
f.close()

with open("objects.json","w") as f:
  json.dump(my_list,f)
f.close()
