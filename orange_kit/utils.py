import datetime
import os

def line_to_hump(string):
  upper = False
  new_str = ''
  for char in string:
    if upper is True:
      new_str += char.upper()
      upper = False
    elif char == '_':
      upper = True
    else:
      new_str += char
  return new_str

def get_now():
  return datetime.datetime.now()


def write_json_file(path, data):
  from .json import json_dumps
  data = json_dumps(data).encode('utf-8')
  with open(path, 'wb') as f:
    f.write(data)


def read_json_file(path):
 from .json import json_loads
 if os.path.exists(path) is False:
    return None
 with open(path, 'r', encoding='utf-8') as f:
   data = f.read()
 return json_loads(data)

