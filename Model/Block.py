import datetime as date
import hashlib as hasher

class Block:
  """Block object contains data """
  def __init__(self, index, timestamp, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block() # Hashes for the block

  def hash_block(self):
    """Creates the hash for the block."""
    sha = hasher.sha256() # SHA = Secure Hash Algorithm
    sha.update((str(self.index) +
               str(self.timestamp) +
               str(self.data) +
               str(self.previous_hash)).encode())
    return sha.hexdigest()

  def returnAsDict(self):
      return {
          "Index": self.index,
          "Time Stamp": self.timestamp,
          "Data": self.data,
          "Previous Hash": self.previous_hash,
          "Hash": self.hash
      }
