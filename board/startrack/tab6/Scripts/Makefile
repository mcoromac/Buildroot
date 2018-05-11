OBJS=fingerprint.o
PROG=fingerprint
LIBSF=-lfprint

all:	fingerprint

HelloWorld:	$(OBJS)
	$(CC) -o $(LDFLAGS) $(PROG) $(OBJS) $(LIBSF) --verbose

$(OBJS): %.o:	%.c
	$(CC) $(CFLAGS) -c -o $@ $< 
