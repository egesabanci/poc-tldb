from time import time
from lark import Transformer
from typing import List, Union

from enums import Operation

class TLDBParserTransformer(Transformer):
  def query(self, parsed: list) -> List[Operation, Union[str, None]]:
    """Converts query into desired format for WAL file

    Cases:
      INSERT OP -> INSERT SENDER RECIPIENT AMOUNT TIMESTAMP 
    """
    match parsed[0].children[0]:
      case Operation.INSERT.value:
        ts: str = str(int(time()))
        operation, sender, recipient, amount = parsed[0].children 
        return [Operation.INSERT, f"{operation}|{sender}|{recipient}|{amount}|{ts}\n"]
        
  def SENDER(self, token) -> str:
    return str(token)
  
  def RECIPIENT(self, token) -> str:
    return str(token)
  
  def AMOUNT(self, token) -> float:
    return float(token)
  
  def insert_operation(self, _) -> str:
    return "insert"
