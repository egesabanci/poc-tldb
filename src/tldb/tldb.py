import os
from typing import Union, List, Any

from ..wal.wal import TLDBWAL
from ..mem.memtable import TLDBMemTable
from ..disk.search import TLDBDiskSearch

from ..parser.parser import TLDBParser
from ..parser.transformer import TLDBParserTransformer

from ..parser.enums import Operation

class TLDB:
  def __init__(self, wal_capacity: float, memtable_capacity: float):
    self.WAL = TLDBWAL(capacity = wal_capacity)
    self.mem = TLDBMemTable(capacity = memtable_capacity)
    self._disk = TLDBDiskSearch() 

    with open(os.path.join(os.getcwd(), "src", "parser", "tldb.grammar.lark"), "r") as f:
      grammar = f.read()

    self._parser = TLDBParser().parser(grammar)
    self._transformer = TLDBParserTransformer()

  def _query_transformer(self, query_str: str):
    tree = self._parser.parse(query_str)
    return self._transformer.transform(tree)

  def query(self, query: str) -> Union[None, List[Any]]:
    op, transformed = self._query_transformer(query)

    match op:
      case Operation.INSERT:
        self._insert(transformed)
        return None

      case Operation.FETCHONE:
        ts = transformed[0]
        return self._fetch_one(ts)
      
      case Operation.FETCH:
        start, end = transformed
        return self._fetch(start, end)
      
      case _:
        raise Exception("Operation is not recognized")
        
  def _insert(self, log: str):
    self.WAL.row(log)
    self.mem.cache(log)

  def _fetch(self, start: float, end: float):
    logs = self.mem.get_many(start, end)
    if logs:
      return logs

    # TODO: implement disk search for fetch many
    pass

  def _fetch_one(self, timestamp: float):
    log = self.mem.get(timestamp)
    if log:
      return log
    
    disk_search = self._disk.search_single(timestamp)
    if disk_search:
      return disk_search
    
    return None