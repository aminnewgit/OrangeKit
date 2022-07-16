from enum import Enum


class BaseEnum(Enum):

  def __repr__(self):
    return self.value

  def __str__(self):
    return self.value


class EnumValueInvalid(BaseException):
  def __init__(self,msg):
    self.msg = msg


