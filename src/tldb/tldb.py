import os

from ..wal.wal import TLDBWAL
from ..mem.memtable import TLDBMemTable

from ..parser.parser import TLDBParser
from ..parser.transformer import TLDBParserTransformer

from ..parser.enums import Operation

class TLDB:
  def __init__(self, wal_capacity: int):
    self.WAL = TLDBWAL(capacity = wal_capacity)
    self.mem = TLDBMemTable()

    with open(os.path.join(os.getcwd(), "parser", "tldb.grammar.lark", "r")) as f:
      grammar = f.read()

    self._parser = TLDBParser().parser(grammar)
    self._transformer = TLDBParserTransformer()

  def _query_transformer(self, query_str: str):
    tree = self._parser.parse(query_str)
    return self._transformer.transform(tree)

  def query(self, query: str):
    op, log = self._query_transformer(query)
    match op:
      case Operation.INSERT.value:
        self.insert(log)

  def _insert(self, log: str):
    self.WAL.row(log)
    self.mem.cache(log)

  def _fetch(self, start: int, end: int):
    logs = self.mem.get_many(start, end)
    if logs:
      return logs

    # TODO: implement disk search for fetch many
    pass

  def _fetch_one(self, timestamp: int):
    log = self.mem.get(timestamp)
    if log:
      return log
    
    # TODO: implement disk search for fetch one
    pass