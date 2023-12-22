import os
from typing import Union

class TLDBDiskSearch:
  def __init__(self):
    self.seg_location = os.path.join(os.getcwd(), "var", "bin")

  def search_single(self, timestamp: float):
    target = self._min_target(timestamp)

    if not target:
      return None
  
    try:
      with open(os.path.join(self.seg_location, target), "r") as seg_file:
        while True:
          seg_file.readline() # skip the first line
          parsed = seg_file.readline().split("|")
          if float(parsed[0]) == timestamp:
            return [*parsed[1:-1], float(parsed[-1])]
          
    except EOFError:
      return None 

  def search_many(self, start: float, end: float):
    items = []
    pass

  def _min_target(self, timestamp: float) -> Union[None, str]:
    segfolder = sorted(os.listdir(self.seg_location))[::-1]

    for seg in segfolder:
      with open(os.path.join(self.seg_location, seg), "r") as f:
        genesis = float(f.readline())

      if (genesis <= timestamp):
        return seg
      
    return None