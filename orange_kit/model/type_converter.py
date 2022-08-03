
# ==============类型转换======================

# ==基本类型==
from types import GenericAlias

from .enum import BaseEnum
from .exception import FieldValidationError


def int_converter(val, field, ex_msg='值'):
  if type(val) is int: return val
  try:
    return int(val)
  except ValueError:
    msg = f'字段{field.name}的{ex_msg}必须是int类型'
    raise FieldValidationError(msg)

def str_converter(val, field, ex_msg='值'):
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
def enum_converter(val, field, ex_msg='值'):
  if isinstance(val, BaseEnum): return val
  try:
    return field.type[val]
  except KeyError:
    msg = f'字段{field.name}的{ex_msg}没有在枚举范围内'
    raise FieldValidationError(msg)

def vo_converter_factory(typ):
  def converter(val, field, ex_nsg='值'):
    return typ(val)
  return converter


# ==递归获取转换器==
def get_type_converter(typ):

  converter = base_type_converter_dict.get(typ)
  if converter is None:
    typ_typ = type(typ)

    from orange_kit.model import VoBase

    if typ_typ == GenericAlias:
      wrap_class = typ.__origin__
      factory = wrap_type_converter_factory_dict[wrap_class]
      if factory is not None:
        converter = factory(typ)
    elif issubclass(typ, BaseEnum):
      converter = enum_converter
    elif issubclass(typ, VoBase):
      converter = vo_converter_factory(typ)

  return converter



