#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include "klock.h"

void init_lock(SmartLock* lock)
{
	pthread_mutex_init(&(lock->mutex), NULL);
	lock->uid = -1;
}

int lock(SmartLock* lock)
{
	long unsigned int uid = pthread_self();
	printf("%lu locking\n", uid);

	if (lock->uid == -1)
	{
		lock->uid = uid;
		pthread_mutex_lock(&(lock->mutex));
	}
	else
	{
		return 0;
	}

	return 1;
}

void unlock(SmartLock* lock)
{
	pthread_mutex_unlock(&(lock->mutex));
	lock->uid = -1;
}

/* Cleanup any dynamic allocated memory.*/
void cleanup()
{
	printf("clean\n");
}






