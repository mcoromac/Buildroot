OBJS=HelloWorld.o
PROG=HelloWorld
LIBSF=-lfprint

all:	HelloWorld

HelloWorld:	$(OBJS)
	$(CC) -o $(LDFLAGS) $(PROG) $(OBJS) $(LIBSF) --verbose

$(OBJS): %.o:	%.c
	$(CC) $(CFLAGS) -c -o $@ $< 
