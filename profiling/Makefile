TARGET  := watcher 
SRCS    := watcher.c
OBJS    := ${SRCS:.c=.o} 
DEPS    := ${SRCS:.c=.dep} 
XDEPS   := $(wildcard ${DEPS}) 

CCFLAGS = -std=gnu99 -O2 -Wall -Werror -ggdb 
LDFLAGS = 
LIBS    = 

.PHONY: all clean distclean 
all: ${TARGET} 

ifneq (${XDEPS},) 
include ${XDEPS} 
endif 

install: watcher
	install watcher /fsopt-watcher
	install initramfs-script /usr/share/initramfs-tools/scripts/init-bottom/fsopt
	install initramfs-hook /usr/share/initramfs-tools/hooks/fsopt

${TARGET}: ${OBJS} 
	${CC} ${LDFLAGS} -o $@ $^ ${LIBS} 

${OBJS}: %.o: %.c %.dep 
	${CC} ${CCFLAGS} -o $@ -c $< 

${DEPS}: %.dep: %.c Makefile 
	${CC} ${CCFLAGS} -MM $< > $@ 

clean:
	rm -f *~ *.o ${TARGET} ${DEPS}

distclean: clean
