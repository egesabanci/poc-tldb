import os
from typing import List, Union

class TLDBMemTable:
  def __init__(self):
    self.wal_location = os.path.join(os.getcwd(), "var", "tl.wal")
    self.segfolder_location = os.path.join(os.getcwd(), "var", "bin")
    self.logs = []

    # restore in-memory cache on crash recovery
    self._restore()

  def cache(self, log: str) -> None:
    self.logs.append(tuple(log.split("|")))

  # TODO: implement fetch
  def fetch(self, start: int, end: int) -> Union[List[tuple], None]:
    pass
  
  # TODO: implement range search on segmented disk files
  def _range(self, start: int, end: int) -> Union[List[tuple], None]:
    pass

  # TODO: implement single timestamp fetch
  def fetch_one(self, timestamp: int) -> tuple:
    pass

  # TODO: implement single timestamp search on segmented disk files
  def _single(self, timestamp: int) -> tuple:
    pass

  def _restore(self):
    recover: bool = self.logs == [] \
      and os.path.getsize(self.wal_location) != 0 

    if recover:
      with open(self.wal_location, "r") as f:
        lines = f.readlines()[2:]
        map(lambda log: self.logs.append((log.split("|"))), lines)