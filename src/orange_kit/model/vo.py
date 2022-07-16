from abc import ABCMeta
from types import GenericAlias


from .exception import FieldValidationError
from .enum import BaseEnum
from ..utils import line_to_hump


class VoField:
  desc:str

  __slots__ = (
    "desc","name",'db_map_json',
    'index','camel_case','type',
    'default','require','type_converter')

  def __init__(self,desc,db_map_json = False,default=None,require=False):
    self.desc = desc
    self.name = None
    self.db_map_json = db_map_json
    self.index = None
    self.camel_case = None
    self.type = None
    self.default = default
    self.require: bool = require
    self.type_converter = None

  def __repr__(self):
    return "VoField"


class __VoMetaclass(ABCMeta):
  def __new__(mcs, name, bases, namespace, **kwargs):
    if name != "VoBase":
      # print(name,namespace)
      an_dict = namespace.get("__annotations__")
      field_list = []
      field_dict = {}
      field_name_list = []
      if an_dict is not None:
        for index,(field_name,field_type) in enumerate(an_dict.items()):
          # 处理字段定义
          field = namespace.get(field_name)
          if field is None:
            field = VoField(field_name)
          field.name = field_name
          field.type = field_type
          field.index = index
          field.camel_case = line_to_hump(field_name)   # 转驼峰
          field.type_converter = get_type_converter(field_type)

          # 字段索引
          field_list.append(field)
          field_dict[field_name] = field
          field_name_list.append(field_name)

          # 给类 属性复制 属性名 方便快速引用
          namespace[field_name] = field_name

      namespace["__field_name_list__"] = tuple(field_name_list)
      namespace["__field_list__"] = tuple(field_list)
      namespace["__field_dict__"] = field_dict


    return super().__new__(mcs, name, bases, namespace, **kwargs)


class VoBase(metaclass=__VoMetaclass):
  """value object base class"""
  # todo 对继承的处理
  __field_name_list__: tuple
  __field_list__: tuple[VoField]
  __field_dict__: dict

  def get_camel_case_dict(self):
    data = self.__dict__
    out_dict = {}
    for field in self.__class__.__field_list__:
      out_dict[field.camel_case] = data.get(field.name)
    return out_dict

  def __init_by_camel_case__(self,data_dict):
    for field in self.__class__.__field_list__:
      val = data_dict.get(field.camel_case,field.default)
      self.__setattr__(field.name, val)


  def __repr__(self):
    return f"{self.__class__.__name__} {self.__dict__.__repr__()}"

  def __init__(self,data_dict=None):

    if data_dict is None :
      for field in self.__class__.__field_list__:
        self.__setattr__(field.name, field.default)
    else:
      for field in self.__class__.__field_list__:
        # 获取值
        val = data_dict.get(field.name)
        if val is None:
          val = data_dict.get(field.camel_case,field.default)

        # 转化值类型, 验证值类型
        if val is None:
          if field.require is True:
            msg = f'{field.name}是必填字段'
            raise FieldValidationError(msg)
        elif field.type_converter is not None:
          val = field.type_converter(val,field)
        self.__setattr__(field.name,val)


# ==============类型转换======================

# ==基本类型==

def int_converter(val,field,exMsg='值'):
  if type(val) is int: return val
  try:
    return int(val)
  except ValueError:
    msg = f'字段{field.name}的{exMsg}必须是int类型'
    raise FieldValidationError(msg)

def str_converter(val,field,exMsg='值'):
  if type(str) is str: return val
  return str(val)

base_type_converter_dict = {
  str:str_converter,
  int:int_converter,
  # todo float 小数类型转换
}


# ==包装类型==
def list_converter_factory(typ):
  element_class = typ.__args__[0]
  element_converter = get_type_converter(element_class)
  def converter(val, field, exMsg='值'):
    res = []
    for element_val in val:
      res.append(element_converter(element_val, field, '元素'))
    return res
  return converter

wrap_type_converter_factory_dict = {
  list: list_converter_factory
  # todo 处理dict 类型的数据
}


# ==封装类型== 转换器
def enum_converter(val,field,exMsg='值'):
  if isinstance(val, BaseEnum): return val
  try:
    return field.type[val]
  except KeyError:
    msg = f'字段{field.name}的{exMsg}没有在枚举范围内'
    raise FieldValidationError(msg)

def vo_converter_factory(typ):
  def converter(val,field,exMsg='值'):
    return typ(val)
  return converter


# ==递归获取转换器==
def get_type_converter(typ):
  converter = base_type_converter_dict.get(typ)
  if converter is None:
    typ_typ = type(typ)

    if typ_typ == GenericAlias:
      wrap_class = typ.__origin__
      factory = wrap_type_converter_factory_dict[wrap_class]
      if (factory is not None):
        converter = factory(typ)

    elif issubclass(typ, BaseEnum):
      converter = enum_converter
    elif issubclass(typ, VoBase):
      converter = vo_converter_factory(typ)

  return converter




#
# class Test:
#   a: dict[str,int] = [1,2,3]
#
#   def __init__(self,a):
#     self.a = a
#
#
#
# a_type = Test.__annotations__.get('a')
#
# print(type(a_type))
# print(a_type.__origin__)
# print(a_type.__args__)