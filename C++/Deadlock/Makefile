CC = gcc
CFLAGS = -Wall -g -std=c99 -Werror -pthread -lrt -D_POSIX_C_SOURCE=199309L
TARGET = locking
OBJS = main.o klock.o


all: clean $(TARGET) run

%.o : %.c
	$(CC) -c $(CFLAGS) $<

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $@

run:
	valgrind --leak-check=full --show-leak-kinds=all --num-callers=20 ./locking

clean:
	rm -f $(TARGET)
	rm -f $(OBJS)
