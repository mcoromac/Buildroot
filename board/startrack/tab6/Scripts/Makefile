OBJS=fingerprint.o
PROG=fingerprint
LIBSF=-lfprint
all:	fingerprint

fingerprint:	$(OBJS)
	$(CC) -o $(LDFLAGS) $(PROG) $(OBJS) $(LIBSF) --verbose

$(OBJS): %.o:	%.c
	$(CC) $(CFLAGS) -c -o $@ $< 
