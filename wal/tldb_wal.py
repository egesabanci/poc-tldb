import os
from pathlib import Path

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
    self.location = Path(__file__).parent / self.filename

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

    with open(self.location, "ab") as f:
      f.write(bytes(log, "UTF-8"))
      f.flush()
      os.fsync(f.fileno())

    return None
    
  def _get_current_capacity(self) -> int:
    """Returns current WAL capacity in bytes"""
    return os.path.getsize(self.location)
  
  def _sweep_and_create(self) -> None:
    """Removes old WAL file to create new one after full capacity"""
    os.remove(self.location)
    return None