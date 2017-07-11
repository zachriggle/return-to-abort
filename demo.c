#include <stdio.h>
#include <unistd.h>

#define RETURN_MAGIC 0xcafe02eb

void __stack_chk_fail();

#define safeReturn(...) \
    do {                                                                                    \
        if ( ((unsigned int*)__builtin_return_address(0) )[0] != RETURN_MAGIC ) {           \
            __stack_chk_fail();                                                             \
        }                                                                                   \
        return __VA_ARGS__ ;                                                                \
    } while (0)

void win() {
    execve("/bin/sh", 0, 0);
}

int main(int argc, char const *argv[])
{
    char stackbuffer[64];
    read(0, stackbuffer, 512);

    safeReturn(0);
}
