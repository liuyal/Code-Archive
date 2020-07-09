## This is a simple Makefile with lost of comments 
## Check Unix Programming Tools handout for more info.

# Define what compiler to use and the flags.
CC=cc
CXX=CC
CCFLAGS= -g -std=c99 -Wall  -D_POSIX_C_SOURCE=200809L

all: build_shell test

# Compile all .c files into .o files
# % matches all (like * in a command)
# $< is the source file (.c file)

%.o : %.c
	$(CC) -c $(CCFLAGS) $<


# Build shell if necessary
build_shell: shell.o
	$(CC) -o shell shell.o


test: build_shell
	./shell


clean:
	rm -f core *.o shell