from tonsdk.boc import Cell, begin_cell
from tonsdk.contract import Address
import bitarray


address = 'EQC6BWNl1j9r4y78pxYMQpBK2fRQUAsLfbhitIKSJ0ali_vN'
message = begin_cell()\
  .store_uint(15,32)\
  .store_address(Address(address))\
  .store_coins(10000)\
  .end_cell()

if __name__ == '__main__':
  array = message.bits.array
  # print(bin(int(array.hex(),16)))

  x = bitarray.bitarray()
  x.frombytes(array)

  print(x.to01())

  op_code = int(x[:32].to01(), 2)
  print(op_code)
  del x[:32]

  del x[:3]

  wc = int(x[:8].to01(), 2)
  del x[:8]

  hash_part = hex(int(x[:256].to01(),2))

  address = str(wc) + ':' + str(hash_part.split('0x')[1])

  print(address)
  print(Address(address).to_string(True,True,True))

  del x[:256]

  l = int(x[:4].to01(),2)
  del x[:4]
  
  amount = int(x[:l*8].to01(),2)
  print(amount)