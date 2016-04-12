#!/usr/bin/env python

import yaml
import json
from pprint import pprint as pp

json_list = None
with open("objects.json") as f:
  json_list = json.load(f)
print "JSON"
pp(json_list)

yaml_list = None
with open("objects.yml") as f:
  yaml_list = yaml.load(f)
print "YAML"
pp(yaml_list)

exit(0)
