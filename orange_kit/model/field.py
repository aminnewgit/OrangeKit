from orange_kit.model.exception import FieldValidationError
from orange_kit.model.type_converter import get_type_converter
from orange_kit.utils import line_to_hump

# todo 把名字形式转换器后期单独抽象到一个类, 或者 反倒反序列化时做, 可以配置的 用alias(别名) 作为描述


class VoField:
  """
  基础值类型
  """
  __slots__ = ('class_name', 'desc', "name",
               'index', 'camel_case', 'type',
               'default', 'type_converter',
               'get_value_from_dict_func')

  def __init__(self,desc,default=None):
    self.class_name = None
    self.desc = desc
    self.name = None
    self.index = None
    self.camel_case = None
    self.type = None
    self.default = default

    self.type_converter = None
    self.get_value_from_dict_func = None

  def init(self):
    self.camel_case = line_to_hump(self.name)  # 转驼峰
    self.set_type_converter()
    self.set_get_value_from_dict_func()

  def get_value(self, val):
    return self.type_converter(val,self)
  def get_value_from_dict(self, input_dict):
    val = self.get_value_from_dict_func(input_dict)
    return self.type_converter(val, self)

  # 获取类型转换器
  def set_type_converter(self):
    self.type_converter = get_type_converter(self.type)

  # 从字典获取值
  def set_get_value_from_dict_func(self):
    if self.camel_case == self.name:
      self.get_value_from_dict_func = self.__get_value_from_dict_direct__
    else:
      self.get_value_from_dict_func = self.__get_value_from_dict_with_camel_case__
  def __get_value_from_dict_with_camel_case__(self,input_dict):
    val = input_dict.get(self.name)
    if val is None:
      val = input_dict.get(self.camel_case, self.default)
    return val
  def __get_value_from_dict_direct__(self,input_dict):
    return input_dict.get(self.name, self.default)

  # 获取字段定义, 用于文档一类
  def get_field_define_dict(self):
    return {
      "name" : self.name,
      "camel_case" : self.camel_case,
      "type" : self.type.__name__,
      "desc": self.desc,
      "default" : self.default,
    }

  def __repr__(self):
    return f"VoField {self.name}"

# 传输对象字段
class DtoField:
  def __init__(self,require=False):
    self.require = require

  def verify_value(self, val):
    # todo 获取类型验证函数 比如 str require 就是不能为空, 字段可以加入规则list, 不支持async
    if val is None:
      if self.require is True:
        raise FieldValidationError(f'{self.name}是必填字段')

# 数据库字段
class SqlField:
  def __init__(self, not_null=False,db_map_json=False):
    self.db_map_json = db_map_json
    self.not_null: bool = not_null


