CC = gcc
CFLAGS = -Wall -g -std=c99 -D_POSIX_C_SOURCE=199309L

TARGET = kallocation
OBJS = main.o kallocator.o list.o

all: clean $(TARGET) run

%.o : %.c
	$(CC) -c $(CFLAGS) $<

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $@

run:
	valgrind --leak-check=full --show-leak-kinds=all --num-callers=20 ./kallocation

clean:
	rm -f $(TARGET)
	rm -f $(OBJS)
