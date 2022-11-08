from io import FileIO
import struct

def get_weights(doc_id : int, weights : FileIO) -> float: 
   offset = doc_id*8
   weights.seek(offset)
   return struct.unpack("=d", weights.read(8))[0]