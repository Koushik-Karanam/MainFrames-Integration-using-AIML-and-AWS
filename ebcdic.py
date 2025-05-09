

HighestPositive = "7fffffffffffffffffff"

def unpack(bytes: bytearray, type: str, rem_lv: bool):
    #
    # Formats ebcdic text, zoned, big endian binary or decinal data into unpacked/string ascii data.
    #
    # Parameters:
    #  - bytes (bytearray): The content to be extracted
    #  - type  (str)......: 
    #   - ch : text                 | pic  x
    #   - zd : zoned                | pic  9
    #   - zd+: signed zoned         | pic s9
    #   - bi : binary               | pic  9 comp
    #   - bi+: signed binary        | pic s9 comp
    #   - pd : packed-decimal       | pic  9 comp-3
    #   - pd+: signed packed-decimal| pic s9 comp-3
    #
    # Returns:
    #  - ascii string
    #
    # Test sample:
    #  import struct
    #  ori = 9223372036854775807
    #  print(ori, unpack(struct.pack(">q",ori),"bi+"))
    #  ori = ori * -1
    #  print(ori, unpack(struct.pack(">q",ori),"bi+"))
    #  print(unpack(bytearray.fromhex("f0f0f1c1"), "zd+"))
    #
    # Input examples:
    # - 8 bytes comp-signed   struct q: -9,223,372,036,854,775,808 through +9,223,372,036,854,775,807
    # - 8 bytes comp-unsigned struct Q: 0 through 18,446,744,073,709,551,615
    # - 4 bytes comp-signed   struct i: -2147483648 through +2147483647
    # - 4 bytes comp-unsigned struct I: 0 through +4294967295
    # - 2 bytes comp-signed   struct h: -32768 through +32767
    # - 2 bytes comp-unsigned struct H: 0 through +65535
    
    if type.lower() == "ch" or type.lower() == "zd":               
        return bytes.decode('cp037').replace('\x00', '').rstrip() if rem_lv == True else bytes.decode('cp037')
    elif type.lower() == "pd" or type.lower() == "pd+":        
        return ("" if bytes.hex()[-1:] != "d" and bytes.hex()[-1:] != "b" else "-") + bytes.hex()[:-1]
    elif type.lower() == "bi" or (type.lower() == "bi+" and bytes.hex() <= HighestPositive[:len(bytes)*2]): 
        a = int("0x" + bytes.hex(), 0)
        return str(a)
    elif type.lower() == "bi+":
        return str(int("0x" + bytes.hex(), 0) - int("0x" + len(bytes) * 2 * "f", 0) -1)
    elif type.lower() == "zd+":
        return ("" if bytes.hex()[-2:-1] != "d" else "-") + bytes[:-1].decode('cp037') + bytes.hex()[-1:]
    else:
        print("---------------------------\nLength & Type not supported\nLength: ",len(bytes),"\nType..: " ,type)
        exit()