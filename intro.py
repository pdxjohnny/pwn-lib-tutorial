from pwn import *

context.clear(arch='i386')
c = constants
assembly =  'read:'      + shellcraft.read(c.STDIN_FILENO, 'esp', 1024)
assembly += 'ret\n'

# Let's provide some simple gadgets:

assembly += 'add_esp: add esp, 0x10; ret\n'

# And perhaps a nice "write" function.

assembly += 'write: enter 0,0\n'
assembly += '    mov ebx, [ebp+4+4]\n'
assembly += '    mov ecx, [ebp+4+8]\n'
assembly += '    mov edx, [ebp+4+12]\n'
assembly += shellcraft.write('ebx', 'ecx', 'edx')
assembly += '    leave\n'
assembly += '    ret\n'
assembly += 'flag: .asciz "The flag"\n'

# And a way to exit cleanly.

assembly += 'exit: ' + shellcraft.exit(0)
binary   = ELF.from_assembly(assembly)

# Finally, let's build our ROP stack

rop = ROP(binary)
rop.write(c.STDOUT_FILENO, binary.symbols['flag'], 8)
rop.exit()
print rop.dump()
'''
0x0000:       0x10000012 write(STDOUT_FILENO, 268435494, 8)
0x0004:       0x1000000e <adjust: add esp, 0x10; ret>
0x0008:              0x1 arg0
0x000c:       0x10000026 flag
0x0010:              0x8 arg2
0x0014:           'faaa' <pad>
0x0018:       0x1000002f exit()
0x001c:           'haaa' <pad>
'''

# The raw data from the ROP stack is available via str.

raw_rop = str(rop)
print enhex(raw_rop)
'''
120000100e000010010000002600001008000000666161612f00001068616161
'''

# Let's try it out!

p = process(binary.path)
p.send(raw_rop)
print p.recvall(timeout=5)
'''
The flag
'''
