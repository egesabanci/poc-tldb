import os

class WAL:
  def __init__(self, capacity: int):
    """Initialize new WAL class

    Parameters:
    - capacity (int):  WAL capacity in MiB (soft-limit)

    Returns:
    - <class WAL>: self 
    """
    self.capacity = capacity * 1_048_576 # MiB in bytes
    self.filename = "tl.wal"
    self.savefolder = os.path.join(os.getcwd(), "var")
    self.segfolder_location = os.path.join(os.getcwd(), "var", "bin")
    self.location = os.path.join(self.savefolder, self.filename)

    if not os.path.exists(self.savefolder):
      os.makedirs(self.savefolder)

  def row(self, log: str, safe: bool = False) -> None:
    """
    Creates new log row in Write Ahead Log and fsync into disk
    
    Parameters:
    - log   (str)     : new row to insert
    - safe  (boolean) : checks if anything left in memory to fsync into disk

    Returns:
    - None
    """

    exists_and_full_capacity = os.path.exists(self.location) \
      and self._get_current_capacity() > self.capacity \
      and safe
    
    if exists_and_full_capacity:
      self._sweep_and_create()
      
    # write timestamp to first row for indexing range queries
    if not os.path.exists(self.location) or os.path.getsize(self.location) == 0:
      with open(self.location, "wb") as f:
        f.write(bytes(log.split("|")[0] + "\n", "UTF-8"))

    with open(self.location, "ab") as f:
      f.write(bytes(log, "UTF-8"))
      f.flush()
      os.fsync(f.fileno())

    return None
    
  def _get_current_capacity(self) -> int:
    """Returns current WAL capacity in bytes"""
    return os.path.getsize(self.location)
  
  def _sweep_and_create(self) -> None:
    """Creates new segmented disk file from current WAL and refresh"""
    if not os.path.exists(self.segfolder_location):
      os.makedirs(self.segfolder_location)

    segfolder = os.listdir(self.segfolder_location)
    last_segindex = 0 \
      if len(segfolder) == 0 \
      else sorted(list(map(lambda x: int(x.split(".")[0]), segfolder)))[-1]

    with open(self.location, "rb") as walf:
      wal_content = walf.read()

    target = os.path.join(self.segfolder_location, f"{last_segindex + 1:06d}.seg") 
    with open(target, "wb") as segf:
      segf.write(wal_content)
      segf.flush()
      os.fsync(segf.fileno())

    os.remove(self.location)
    return None