# Makefile for building multi-file application

# final executable to build:
TARGET= candykids
# .o files to link in (for all .c files)
OBJS = candykids.o bbuff.o stats.o

# Add support for pthread and real-time clock here:
CFLAGS = -g -std=c99 -Wall -Werror -D_POSIX_C_SOURCE=199309L -lrt -pthread 


# You should not need to change any of this:
CC_C = gcc

all: clean $(TARGET) run #valgrind

%.o : %.c
	$(CC) -c $(CFLAGS) $<

run:
	./candykids 1 1 10
	./candykids 1 10 10
	./candykids 2 2 5
	./candykids 10 1 10
	./candykids 20 20 15
	./candykids 1000 1000 10

	valgrind --leak-check=full --show-leak-kinds=all --num-callers=20 ./candykids 8 1 1
	valgrind --leak-check=full --show-leak-kinds=all --num-callers=20 ./candykids 10 1 10
	valgrind --leak-check=full --show-leak-kinds=all --num-callers=20 ./candykids 1 1 10

	./candykids -1 10 15

$(TARGET): $(OBJS)
	$(CC_C) $(CFLAGS) $(OBJS) -o $@

clean:
	rm -f $(TARGET)
	rm -f $(OBJS)

## This is a simple Makefile with lost of comments 
## Check Unix Programming Tools handout for more info.

# # Define what compiler to use and the flags.
# CC=cc
# CXX=CC
# CCFLAGS= -g -std=c99 -Wall -Werror


# #all: collatz fibonacci measureSystemCall c f m 

# all: candykids m 

# # Compile all .c files into .o files
# # % matches all (like * in a command)
# # $< is the source file (.c file)
# %.o : %.c
# 	$(CC) -c $(CCFLAGS) $<

# # Build fibonacci
# fibonacci: candykids.o
# 	$(CC) -pthread -o candykids candykids.o

# m: candykids
# 	./candykids 2 1 5
# 	./candykids 8 1 52

# clean:
# 	rm -f core *.o candykids
