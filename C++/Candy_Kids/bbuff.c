#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <pthread.h>
#include <semaphore.h>

#include "bbuff.h"

int counter;
int Val;
void* buffer[BUFFER_SIZE];

sem_t full;
sem_t empty;
sem_t mutex;

void bbuff_init(void)
{
	sem_init(&mutex, 0, 1);
	sem_init(&full, 0, 0);
	sem_init(&empty, 0, BUFFER_SIZE);
	counter = 0;

	return;
}

void bbuff_blocking_insert(void* item)
{
	sem_wait(&empty);
	sem_wait(&mutex);

	buffer[counter] = item;
	counter++;
	//counter = counter % BUFFER_SIZE;
	
	//sem_getvalue(&empty, &Val);
	//printf("emptyVal: %d\n", Val);

	sem_post(&mutex);
	sem_post(&full);
	
	return;
}

void* bbuff_blocking_extract(void)
{
	sem_wait(&full);
	sem_wait(&mutex);

	counter--;
	//counter = counter % BUFFER_SIZE;
	void *candy_ptr = buffer[counter];
	//buffer[counter-1] = NULL;

	//sem_getvalue(&empty, &Val);
	//printf("emptyVal: %d\n", Val);

	sem_post(&mutex);
	sem_post(&empty);

	return candy_ptr;
}

_Bool bbuff_is_empty(void)
{
	sem_wait(&mutex);

	if (counter > 0) 
	{ 
		sem_post(&mutex);
		return false;
	}

	sem_post(&mutex);

	return true;
}