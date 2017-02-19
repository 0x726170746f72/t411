import bencodepy as bencode

class Torrent:
  metadata = {}

  def __init__(self, data):
    try:
      self.metadata = bencode.decode(data)
    except Exception as e:
      raise Exception(str(e))


  def set_tracker(self, tracker):
    if b'announce' not in self.metadata:
      raise Exception('Le fichier torrent semble corrompu.')

    self.metadata[b'announce'] = tracker.encode('UTF-8')

  def set_comment(self, comment):
    self.metadata[b'comment'] = comment.encode('UTF-8')

  def set_author(self, author):
    self.metadata[b'created by'] = author.encode('UTF-8')

  def set_trackers_list(self, trackers):
    for i in range(len(trackers)):
      trackers[i] = trackers[i].encode('UTF-8')
    self.metadata[b'announce-list'] = trackers

  def length(self):
    if b'info' not in self.metadata:
      raise Exception('Le fichier torrent semble corrompu.')
    
    if b'piece length' not in self.metadata[b'info'] or b'pieces' not in self.metadata[b'info']:
      raise Exception('Le fichier torrent semble corrompu.')

    size = self.metadata[b'info'][b'piece length'] * len(self.metadata[b'info'][b'pieces'])//20
    return size

  def name(self):
    if b'info' not in self.metadata:
      raise Exception('Le fichier torrent semble corrompu.')
    if b'name' not in self.metadata[b'info']:
      raise Exception('Le fichier torrent semble corrompu.')
    return self.metadata[b'info'][b'name'].decode('UTF-8')

  def set_name(self, name):
    if b'info' not in self.metadata:
      raise Exception('Le fichier torrent semble corrompu.')
    if b'name' not in self.metadata['info']:
      raise Exception('Le fichier torrent semble corrompu.')
    self.metadata[b'info'][b'name'] = name.encode('UTF-8')

  def build(self):
    try:
      b = bencode.encode(self.metadata)
    except Exception as e:
      raise e
    return b

