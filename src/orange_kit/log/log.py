from enum import Enum


def void_print(*args, sep='', end=''):
  pass


class DebugLog:

  def __init__(self, enable : bool):
    if enable is True:
      self.out = print
    else:
      self.out = void_print

  def __call__(self,*args, sep=' ', end='\n'):
    # todo 使用包装器在生产环境替换未空函数
    self.out(*args, sep=sep, end=end)


  def list(self,list_data):
    # todo 使用包装器在生产环境替换未空函数
    if len(list_data) == 0:
      self.out("[]")
    else:
      for d in list_data:
        self.out(d)


  def print_split(self):
    self.out("==========================================")


  def dict(self,dict_data: dict):
    for k, v in dict_data.items():
      self.out(k, v)

class InfoLog:
  def __call__(self, *args, sep=' ', end='\n'):
    # todo 使用包装器在生产环境替换未空函数
    print(*args, sep=sep, end=end)

  @staticmethod
  def list(list_data):
    # todo 使用包装器在生产环境替换未空函数
    if len(list_data) == 0:
      print("[]")
    else:
      for d in list_data:
        print(d)

  @staticmethod
  def split_line():
    print("==========================================")

  @staticmethod
  def dict(dict_data: dict):
    for k, v in dict_data.items():
      print(k, v)

# todo 初始化配置, 关闭所有debug 信息

class OrangeLog:
  def __init__(self,name):
    self.debug = DebugLog(False)
    self.info = InfoLog()
    self.name = name

  def enable_debug_log(self):
    self.debug = DebugLog(True)







