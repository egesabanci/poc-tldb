from time import time
from lark import Transformer
from typing import Union

from .enums import Operation

class TLDBParserTransformer(Transformer):
  def query(self, parsed: list) -> Union[Operation, Union[Operation, str]]:
    """
    Parse client query request and returns operation necessities
    
    Returns:
    - Union[Operation, Union[Operation, str]]
    """
    match parsed[0].children[0]:
      case Operation.INSERT.value:
        ts: str = str(int(time()))
        operation, sender, recipient, amount = parsed[0].children 
        return [Operation.INSERT, f"{operation}|{ts}|{sender}|{recipient}|{amount}\n"]
        
  def SENDER(self, token) -> str:
    return str(token)
  
  def RECIPIENT(self, token) -> str:
    return str(token)
  
  def AMOUNT(self, token) -> float:
    return float(token)
  
  def insert_operation(self, _) -> str:
    return "insert"
