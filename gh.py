import gdb
import time

gdb.execute("layout asm")
gdb.execute("focus cmd")

gdb.execute("b *input+24")
gdb.execute("b *main+77")

gdb.execute("r < payload")

gdb.execute("x/40x $rsp")
gdb.execute("c")

# End of main
gdb.execute("x/40x $rsp")

time.sleep(1)

gdb.execute("si")

time.sleep(5)

gdb.execute("s")
