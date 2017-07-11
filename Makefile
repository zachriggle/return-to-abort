all: demo

CFLAGS += -fno-stack-protector -O2 -D_FORTIFY_SOURCE=0

clean:
	rm -f demo *.s

demo: demo.safe.s
	gcc -o $@ $^

%.s: %.c
	gcc $(CFLAGS) -S -o $@ $^

%.safe.s: %.s safecall.awk
	awk -f safecall.awk $< > $@
	diff $< $@ || true

.PRECIOUS: %.s %.safe.s
.PHONY: clean all
