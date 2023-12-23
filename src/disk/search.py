import os
from typing import Union, List

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
    assert end > start, "Range start cannot be greater than range end"

    items = []
    segmentations = self._min_targets_many(start, end)
    
    for seg in segmentations:
      with open(os.path.join(self.seg_location, seg), "r") as f:
        f.readline() # skip first genesis line
        try:
          while True:
            line = f.readline()
            splitted = line.split("|")
            ts = float(splitted[0])
            if start <= ts <= end:
              items.append([ts, *splitted[1:-1], float(splitted[-1])])
        except:
          continue

    return items

  def _min_target(self, timestamp: float) -> Union[None, str]:
    segfolder = sorted(os.listdir(self.seg_location))[::-1]

    for seg in segfolder:
      with open(os.path.join(self.seg_location, seg), "r") as f:
        genesis = float(f.readline())

      if (genesis <= timestamp):
        return seg
      
    return None
  
  def _min_targets_many(self, start: float, end: float) -> Union[None, List[str]]:
    segfolder = sorted(os.listdir(self.seg_location))[::-1]
    seg_genesis = list()

    for seg in segfolder:
      with open(os.path.join(self.seg_location, seg), "r") as f:
        genesis = float(f.readline())

      seg_genesis.append((seg, genesis))

    start_seg = list(filter(lambda x: x[1] <= start, seg_genesis))
    end_seg = list(filter(lambda x: x[1] >= end, seg_genesis[::-1]))
    
    assert start_seg != [] and end_seg != [], \
      "Query failed: range cannot found"
 
    seg_folder_range = [
      int(start_seg[0][0].split(".")[0]),
      int(end_seg[0][0].split(".")[0])
    ] 
    
    folders = filter(lambda x: int(x.split(".")[0]) >= seg_folder_range[0] \
                     and int(x.split(".")[0]) < seg_folder_range[1], segfolder) 
    
    return list(folders)[::-1]