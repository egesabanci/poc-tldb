import os
import sys
from typing import Any

class TLDBMemTable:
  def __init__(self, capacity: int):
    self.wal_location = os.path.join(os.getcwd(), "var", "tl.wal")
    self.segfolder_location = os.path.join(os.getcwd(), "var", "bin")
    self.logs = dict()
    self.capacity = capacity * 1_048_576

    # restore in-memory cache on crash recovery
    self._restore()

  def __getattribute__(self, __name: str) -> Any:
    if sys.getsizeof(self.logs) > self.capacity:
      self.logs = dict()

  def cache(self, log: str) -> None:
    parsed = tuple(log.split("|"))
    timestamp = int(parsed[0])
    row = tuple(parsed[1:])

    self.logs[timestamp] = row
    return None

  def get(self, timestamp: int):
    row = self.logs.get(timestamp)
    if row is not None:
      return f"{timestamp}|{'|'.join(row)}"

    return None
  
  def get_many(self, start: int, end: int):
    keys = list(self.logs.keys())
    min_, max_ = min(keys), max(keys)

    if start >= min_ and end <= max_:
      filtered_keys = filter(lambda x: x >= start and x <= end, keys)
      return list(map(lambda x: self.logs[x], filtered_keys))
    
    return None
  
  def _restore(self):
    recover: bool = self.logs == [] \
      and os.path.getsize(self.wal_location) != 0 

    if recover:
      with open(self.wal_location, "r") as f:
        lines = f.readlines()[2:]
        map(lambda log: self.logs.append((log.split("|"))), lines)