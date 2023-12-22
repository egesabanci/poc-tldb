import os
import sys

class TLDBMemTable:
  def __init__(self, capacity: float):
    self.wal_location = os.path.join(os.getcwd(), "var", "tl.wal")
    self.segfolder_location = os.path.join(os.getcwd(), "var", "bin")
    self.logs = dict()
    self.capacity = capacity * 1_048_576

    # restore in-memory cache on crash recovery
    self._restore()

  def cache(self, log: str) -> None:
    # if capacity is full - clears memtable
    if sys.getsizeof(self.logs) > self.capacity:
      self.logs = dict()

    parsed = tuple(log.split("|"))
    timestamp = float(parsed[0])
    row = tuple(parsed[1:])

    self.logs[timestamp] = row
    return None

  def get(self, timestamp: int):
    row = self.logs.get(timestamp)
    if row is not None:
      return [*row[0:-1], float(row[-1].replace("\n", ""))]

    return None
  
  def get_many(self, start: int, end: int):
    keys = list(self.logs.keys())
    min_, max_ = min(keys), max(keys)

    if start >= min_ and end <= max_:
      filtered_keys = filter(lambda x: x >= start and x <= end, keys)
      return list(map(lambda x: self.logs[x], filtered_keys))
    
    return None
  
  def _restore(self):
    recover: bool = len(self.logs.keys()) == 0 \
      and os.path.exists(self.wal_location) \
      and os.path.getsize(self.wal_location) != 0 
  
    if recover: 
      with open(self.wal_location, "r") as f:
        lines = f.readlines()[1:]
        for i in lines:
          parsed = i.split("|")
          self.logs[float(parsed[0])] = tuple(parsed[1:])