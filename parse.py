import os
from struct import unpack
from json import dumps

def debug(*msg):
  if os.environ.get("DEBUG") == "1":
    print("DEBUG | ", *msg)

def bytes_to_number(bs):
  x = 0
  l = len(bs)
  debug("Read length", l)
  for i in range(l, 0, -1):
    ii = i - 1
    x += bs[ii] << ii
  return x

SUBTYPE_LOOKUP = [
    "generic",
    "function",
    "binary (old)",
    "uuid (old)",
    "uuid",
    "md5",
    "encrypted value",
    "user defined"
    ]

bson_file = open("test.bson", "rb") 
Indent = 0

def output(*msg):
  global Indent
  # debug("INDENT", Indent)
  print(( " " * ( Indent * 2 ) ) + " ".join(map(lambda x: str(x), msg)))

debug("Reading BSON size")

def read(n):
  t = bson_file.read(n)
  debug("READ", bson_file.tell() - n, n, t)
  if t == b"":
    debug("Early EXIT")
    quit()
  return t

def readByte():
  try:
    return read(1)[0]
  except:
    debug("READ ERROR")
    exit(0)

def readInt32():
  return unpack("i", read(4))[0]

def readInt64():
  return unpack("q", read(8))[0]

def readUInt64():
  return unpack("Q", read(8))[0]

def readDouble():
  return unpack("d", read(8))[0]

def readDecimal():
  return unpack("d", read(16))[0]

def readNullTermString():
  buff = []
  while 1:
    c = readByte()
    if c > 0:
      buff.append(c)
    else:
      return "".join(map(chr, buff))

def parseCString():
  debug("Parse C String")
  return readNullTermString()

def parseEName():
  debug("Parse Element Name")
  return parseCString()

def parseDocument(inner=False):
  debug("Parse Document")
  document_size = readInt32()
  e_list = {}
  
  start = bson_file.tell() if inner else 0
  while ((bson_file.tell() - start) < document_size):
    element = parseElement()
    if element:
      debug("Captured element", element)
      e_list[element["k"]] = {
        "value": element["v"],
        "type": element["t"]
      }
    else:
      debug("EMERGENCY BREAK")
      return e_list

  if bson_file.tell() < document_size:
    readByte()
  return e_list

def parseString():
  readInt32()
  return readNullTermString()

def parseBinary():
  leng = readInt32()
  sub_type = SUBTYPE_LOOKUP[readByte()]
  value = read(leng)

  return {
    leng: leng, 
    type: sub_type, 
    value: value
  }

def parseRegex():
  body = parseCString()
  flags = parseCString()

  return {
    body: body,
    flags: flags
  }

def parseElement():
  v_type = readByte()
  debug("Type", v_type)
  key = parseEName()
  debug("Key", key)
  value = None
  
  if v_type == 0x0: return None
  elif v_type == 0x1: value = readDouble()
  elif v_type == 0x2: value = parseString()
  elif v_type == 0x3: value = parseDocument(True)
  elif v_type == 0x4: value = parseDocument(True)
  elif v_type == 0x5: value = parseBinary()
  # if v_type == 6: DEPRICATED
  elif v_type == 0x7: value = read(12)
  elif v_type == 0x8: value = readByte() == 1
  elif v_type == 0x9: value = readInt64()
  # if v_type == 0xa: value = None
  elif v_type == 0xb: value = parseRegex()
  # if v_type == 0xc: DEPRICATED
  elif v_type == 0xd: value: parseString()
  # if v_type == 0xe: DEPRICATED
  # if v_type == 0xf: DEPRICATED
  elif v_type == 0x10: value = readInt32()
  elif v_type == 0x11: value = readUInt64()
  elif v_type == 0x12: value = readInt64()
  elif v_type == 0x13: value = readDecimal()
  elif v_type == 0xff: value = "min key"
  elif v_type == 0x7f: value = "max key"

  return {
      "k": key,
      "v": value,
      "t": v_type
    }

doc = parseDocument()
print(dumps(doc))
