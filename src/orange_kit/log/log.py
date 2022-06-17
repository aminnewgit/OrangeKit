

class DebugLog:

  def __call__(self,*args, sep=' ', end='\n'):
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
  def __init__(self):
    self.debug = DebugLog()




