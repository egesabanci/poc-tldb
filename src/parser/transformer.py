from time import time
from lark import Transformer

from .enums import Operation

class TLDBParserTransformer(Transformer):
  def query(self, parsed: list):
    """
    Parse client query request and returns operation necessities
    
    Returns:
    - Union[Operation, Union[Operation, str]]
    """
    return parsed
  
  def SENDER(self, token) -> str:
    return str(token)
  
  def RECIPIENT(self, token) -> str:
    return str(token)
  
  def AMOUNT(self, token) -> float:
    return float(token)
  
  def TIMESTAMP(self, token) -> int:
    return int(token)
  
  def insert(self, token):
    ts: str = str(int(time()))
    sender, recipient, amount = token 
    return [Operation.INSERT, f"{ts}|{sender}|{recipient}|{amount}\n"]
    
  def range(self, token):
    return [Operation.FETCH, token]
  
  def single(self, token):
    return [Operation.FETCHONE, token]