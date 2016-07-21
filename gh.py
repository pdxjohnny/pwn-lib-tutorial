import gdb
import time

gdb.execute("layout asm")
gdb.execute("focus cmd")

gdb.execute("b *input+24")
gdb.execute("b *main+77")

gdb.execute("r < payload")

gdb.execute("x/20x $rsp")
gdb.execute("c")

# End of main
gdb.execute("x/20x $rsp")

time.sleep(1)

gdb.execute("s")

gdb.execute("x/20x $rsp")
