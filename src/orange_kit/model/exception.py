

class FieldValidationError(BaseException):
  """
  字段验证异常
  """
  def __init__(self,msg):
    self.msg = msg
