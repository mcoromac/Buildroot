OBJS=fingerprint.o
PROG=fingerprint
LIBSF=-lfprint
BUILDROOT_HOME=/home/mariano/buildroot
INCLUDES = -I$(BUILDROOT_HOME)/output/target/usr/include
LIBS = -L$(BUILDROOT_HOME)/output/target/lib
all:	fingerprint

fingerprint:	$(OBJS)
	$(CC) -o $(LDFLAGS) $(PROG) $(OBJS) $(LIBSF) --verbose

$(OBJS): %.o:	%.c
	$(CC) $(CFLAGS) -c -o $@ $< 
